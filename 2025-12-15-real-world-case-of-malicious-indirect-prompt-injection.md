# 2025-12-15 (Monday): Real-World Example of Malicious Indirect Prompt Injection

## Authors:

- Beliz Kaleli, Shehroze Farooqi, Oleksii, Alex Starov

## Notes:

- We identified a real-world example of malicious indirect prompt injection.
- In this example, the actors attempted to bypass AI-based ad reviewers and promote scam products.
- This case uses multiple evasion techniques to hide its injected LLM prompts from security checks:
  - encoding
  - dynamic execution
  - obfuscation
  - semantic tricks
  - visually concealing

## URL For This Example:

- `hxxps[:]//reviewerpress[.]com/advertorial-maxvision-can/?lang=en`

## Details:

The image below shows parts of the HTML code returned by the above URL that notes some of the techniques to hide the injected LLM prompts.

![Image of parts of the HTML code that shows the indirect prompt injection hidden through various methods.](https://github-production-user-asset-6210df.s3.amazonaws.com/17553852/526702236-3caf8681-b665-461c-98bf-3fe3360fe572.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20251215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251215T180649Z&X-Amz-Expires=300&X-Amz-Signature=69a7d8890d2e91e57f05397ab86ae618556b0d312e6d0d031be49aac4ec7a1e1&X-Amz-SignedHeaders=host)

**Indirect prompt injection** occurs when an adversary embeds hidden or manipulated text within website content, with the intention that an LLM will later process this content. Instead of directly prompting, the attacker relies on the website to unknowingly pass the malicious text into the LLM’s input, causing the model to follow the attacker’s instructions.

To our knowledge, this is the first detection of a real-world example of a malicious indirect prompt injection designed <ins>**to bypass an AI-based product ad review system**</ins>.
