"""
Extract IOCs from Unit42 Threat Intel text files into a normalized CSV file.
"""

import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

SOURCE_FEED = "Palo Alto Networks Unit42 Threat Intel"
FOLDER_PATH = Path('/Users/a0086597/Desktop/Python/IOC/Unit42-timely-threat-intel')
FILE_EXTENSIONS = r"exe|dll|ocx|sys|drv|cpl|xlsb|xlsm|xlsx|xls|docm|docx|doc|pptm|pptx|ppt|pdf|zip|rar|7z|gz|iso|img|dat|php|ps1|sh|bat|cmd|vbs|js|jse|wsf|hta|html|htm|txt|rtf|lnk|scr|msi|jar|apk|elf|bin"
IOC_PATTERNS = {
    "url": r"""\b(?:https?|hxxps?)(?:://|\[:\]//|\[://\])[^\s"'<>),]+""",
    "email": r"""\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]{1,63}(?:\.|\[\.\]))+[A-Za-z]{2,63}\b""",
    "ipv4": r"""\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.|\[\.\])){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b""",
    "sha512": r"""\b[a-fA-F0-9]{128}\b""",
    "sha256": r"""\b[a-fA-F0-9]{64}\b""",
    "sha1": r"""\b[a-fA-F0-9]{40}\b""",
    "md5": r"""\b[a-fA-F0-9]{32}\b""",
    "chrome_extension_id": r"""\b[a-p]{32}\b""",
    "windows_path": rf"""\b[A-Za-z]:\\[^\r\n:*?"<>|]+?\.(?:{FILE_EXTENSIONS})\b""",
    "filename": rf"""(?<![A-Za-z0-9._-])(?:[A-Za-z0-9][A-Za-z0-9._%()+\-\[\] ]{{0,200}}\.(?:{FILE_EXTENSIONS}))(?![A-Za-z0-9._-])""",
    "bitcoin_wallet": r"""\b(?:bc1[ac-hj-np-z02-9]{25,90}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b""",
    "ethereum_wallet": r"""\b0x[a-fA-F0-9]{40}\b""",
    "monero_wallet": r"""\b[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b""",
    "domain": rf"""\b(?:[A-Za-z0-9](?:[A-Za-z0-9-]{{0,61}}[A-Za-z0-9])?(?:\.|\[\.\]))+(?!(?:{FILE_EXTENSIONS})\b)[A-Za-z]{{2,63}}\b"""
}

class IOCParser:
    """
    Parser for threat intelligence text files.
    """
    def __init__(self) -> None:
        self.source_feed = SOURCE_FEED
        self.folder_path = FOLDER_PATH

    def _get_first_line(self, data:str) -> None | str:
        line = data.splitlines()[0].strip()
        if not line:
            return None
        return line

    def remove_sections(self, text: str) -> str:
        """
        Remove sections from the text based on section headers."""
        sections_to_skip = {"REFERENCE"}
        lines = text.splitlines()
        kept_lines = []
        skipping = False

        section_header_re = re.compile(r"^[A-Z][A-Z0-9 /()&._-]{1,}:$")

        for line in lines:
            stripped = line.strip()

            if section_header_re.match(stripped):
                section_name = stripped.rstrip(":").upper()
                skipping = section_name in sections_to_skip

                if skipping:
                    continue

            if not skipping:
                kept_lines.append(line)

        return "\n".join(kept_lines)

    def mask_spans(self, text: str, spans: list[tuple[int, int]]) -> str:
        """
        Mask the specified spans in the text with spaces."""
        chars = list(text)

        for start, end in spans:
            for i in range(start, end):
                chars[i] = " "

        return "".join(chars)

    def parse_data(self, data: str) -> dict[Any, set[str]]:
        """
        Parse a single threat intel file and return extracted information.
        """
        data = self.remove_sections(data)
        ioc_results = defaultdict(set)
        spans_to_mask_before_domain = []

        extraction_order = [
        "url",
        "email",
        "ipv4",
        "sha512",
        "sha256",
        "sha1",
        "md5",
        "bitcoin_wallet",
        "ethereum_wallet",
        "monero_wallet",
        "chrome_extension_id",
        "windows_path",
        "filename",
        ]

        for ioc_type in extraction_order:
            pattern = IOC_PATTERNS[ioc_type]
            regex = re.compile(pattern, flags=re.IGNORECASE)

            for match in regex.finditer(data):
                value = match.group(0).strip(" \t\r\n-.,;")

                if value:
                    ioc_results[ioc_type].add(value)
                    spans_to_mask_before_domain.append(match.span())

        domain_text = self.mask_spans(data, spans_to_mask_before_domain)

        domain_regex = re.compile(IOC_PATTERNS["domain"], flags=re.IGNORECASE)

        for match in domain_regex.finditer(domain_text):
            value = match.group(0).strip(" \t\r\n-.,;")

            if value:
                ioc_results["domain"].add(value)

        return dict(ioc_results)

    def generate_csv(self, parsed_iocs: dict[Any, set[str]], first_line: None | str) -> None:
        """
        Generate a CSV file from the parsed IOCs.
        """
        header = ["IOC_type", "Value", "Source_feed", "Confidence_Additional_info", "Last_modified_date"]
        last_modified_date = ""
        additional_info = ""
        if first_line:
            match = re.match(r"^\s*#*\s*(\d{4}-\d{2}-\d{2})\s*(?:\([^)]+\))?\s*(?:-|:)\s*(.+?)\s*$", first_line)
            if match:
                last_modified_date = match.group(1)
                additional_info = match.group(2)

        file_exists = Path("iocs_unit42.csv").exists()

        existing_rows = set()
        if file_exists:
            with open("iocs_unit42.csv", mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    existing_rows.add((row[0], row[1]))

        with open("iocs_unit42.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)

            for ioc_type, values in parsed_iocs.items():
                for value in values:
                    row = [ioc_type, value, self.source_feed, additional_info, last_modified_date]
                    row_key = (str(ioc_type), value)
                    if row_key not in existing_rows:
                        writer.writerow(row)
                        existing_rows.add(row_key)

    def read_files(self):
        """
        Yield all files from the configured folder path.
        """
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder does not exist: {self.folder_path}")

        if not self.folder_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.folder_path}")

        for file_path in self.folder_path.iterdir():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    data = file.read()
                    first_line = self._get_first_line(data)
                    parsed_iocs = self.parse_data(data=data)
                    self.generate_csv(parsed_iocs=parsed_iocs, first_line=first_line)

def main() -> None:
    """Main function"""
    parser = IOCParser()
    parser.read_files()

if __name__ == "__main__":
    main()
