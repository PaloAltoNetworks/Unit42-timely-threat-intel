### DEADBOLT RANSOMWARE

New wave of attacks observed likely starting 2022-05-13

REFERENCE:

- https://twitter.com/Unit42_Intel/status/1526240822668275714

---
### Lock screen diff summary


* Updated CSS
* Update ransom page title
* Inbuilt SHA-256 implementation within the Javascript, as opposed to the previous use of the standard "SubtleCrypto" implementation. This was likely done to speed up the process of key verification and/or ensure the key verification works on browsers that don't have the "SubtleCrypto" API available.
* Same master key used as the previous wave of QNAP attacks, based on the SHA-256 value that is checked.

---
### New inbuilt SHA-256 implementation

```
var SHA256 = "undefined" != typeof exports ? exports : {}; !function (t) { var r = [1116352408, 1899447441, -1245643825, -373957723, 961987163, 1508970993, -1841331548, -1424204075, -670586216, 310598401, 607225278, 1426881987, 1925078388, -2132889090, -1680079193, -1046744716, -459576895, -272742522, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, -1740746414, -1473132947, -1341970488, -1084653625, -958395405, -710438585, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, -2117940946, -1838011259, -1564481375, -1474664885, -1035236496, -949202525, -778901479, -694614492, -200395387, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, -2067236844, -1933114872, -1866530822, -1538233109, -1090935817, -965641998], i = { sha256: 1 }; t.createHash = function (t) { if (t && !i[t] && !i[t.toLowerCase()]) throw new Error("Digest method not supported"); return new n }; var n = function () { function t() { this.A = 1779033703, this.B = -1150833019, this.C = 1013904242, this.D = -1521486534, this.E = 1359893119, this.F = -1694144372, this.G = 528734635, this.H = 1541459225, this.t = 0, this.i = 0, (!s || e >= 8e3) && (s = new ArrayBuffer(8e3), e = 0), this.h = new Uint8Array(s, e, 80), this.o = new Int32Array(s, e, 20), e += 80 } return t.prototype.update = function (t) { if ("string" == typeof t) return this.u(t); if (null == t) throw new TypeError("Invalid type: " + typeof t); var r = t.byteOffset, i = t.byteLength, n = i / 64 | 0, s = 0; if (n && !(3 & r) && !(this.t % 64)) { for (var h = new Int32Array(t.buffer, r, 16 * n); n--;)this.v(h, s >> 2), s += 64; this.t += s } if (1 !== t.BYTES_PER_ELEMENT && t.buffer) { var e = new Uint8Array(t.buffer, r + s, i - s); return this.p(e) } return s === i ? this : this.p(t, s) }, t.prototype.p = function (t, r) { var i = this.h, n = this.o, s = t.length; for (r |= 0; r < s;) { for (var h = this.t % 64, e = h; r < s && e < 64;)i[e++] = t[r++]; e >= 64 && this.v(n), this.t += e - h } return this }, t.prototype.u = function (t) { for (var r = this.h, i = this.o, n = t.length, s = this.i, h = 0; h < n;) { for (var e = this.t % 64, f = e; h < n && f < 64;) { var o = 0 | t.charCodeAt(h++); o < 128 ? r[f++] = o : o < 2048 ? (r[f++] = 192 | o >>> 6, r[f++] = 128 | 63 & o) : o < 55296 || o > 57343 ? (r[f++] = 224 | o >>> 12, r[f++] = 128 | o >>> 6 & 63, r[f++] = 128 | 63 & o) : s ? (o = ((1023 & s) << 10) + (1023 & o) + 65536, r[f++] = 240 | o >>> 18, r[f++] = 128 | o >>> 12 & 63, r[f++] = 128 | o >>> 6 & 63, r[f++] = 128 | 63 & o, s = 0) : s = o } f >= 64 && (this.v(i), i[0] = i[16]), this.t += f - e } return this.i = s, this }, t.prototype.v = function (t, i) { var n = this, s = n.A, e = n.B, f = n.C, A = n.D, p = n.E, d = n.F, I = n.G, U = n.H, l = 0; for (i |= 0; l < 16;)h[l++] = o(t[i++]); for (l = 16; l < 64; l++)h[l] = y(h[l - 2]) + h[l - 7] + w(h[l - 15]) + h[l - 16] | 0; for (l = 0; l < 64; l++) { var x = U + v(p) + u(p, d, I) + r[l] + h[l] | 0, g = c(s) + a(s, e, f) | 0; U = I, I = d, d = p, p = A + x | 0, A = f, f = e, e = s, s = x + g | 0 } this.A = s + this.A | 0, this.B = e + this.B | 0, this.C = f + this.C | 0, this.D = A + this.D | 0, this.E = p + this.E | 0, this.F = d + this.F | 0, this.G = I + this.G | 0, this.H = U + this.H | 0 }, t.prototype.digest = function (t) { var r = this.h, i = this.o, n = this.t % 64 | 0; for (r[n++] = 128; 3 & n;)r[n++] = 0; if ((n >>= 2) > 14) { for (; n < 16;)i[n++] = 0; n = 0, this.v(i) } for (; n < 16;)i[n++] = 0; var s = 8 * this.t, h = (4294967295 & s) >>> 0, e = (s - h) / 4294967296; return e && (i[14] = o(e)), h && (i[15] = o(h)), this.v(i), "hex" === t ? this.I() : this.U() }, t.prototype.I = function () { var t = this, r = t.A, i = t.B, n = t.C, s = t.D, h = t.E, e = t.F, o = t.G, u = t.H; return f(r) + f(i) + f(n) + f(s) + f(h) + f(e) + f(o) + f(u) }, t.prototype.U = function () { var t = this, r = t.A, i = t.B, n = t.C, s = t.D, h = t.E, e = t.F, f = t.G, u = t.H, a = t.h, c = t.o; return c[0] = o(r), c[1] = o(i), c[2] = o(n), c[3] = o(s), c[4] = o(h), c[5] = o(e), c[6] = o(f), c[7] = o(u), a.slice(0, 32) }, t }(); t.Hash = n; var s, h = new Int32Array(64), e = 0, f = function (t) { return (t + 4294967296).toString(16).substr(-8) }, o = 254 === new Uint8Array(new Uint16Array([65279]).buffer)[0] ? function (t) { return t } : function (t) { return t << 24 & 4278190080 | t << 8 & 16711680 | t >> 8 & 65280 | t >> 24 & 255 }, u = function (t, r, i) { return i ^ t & (r ^ i) }, a = function (t, r, i) { return t & r | i & (t | r) }, c = function (t) { return (t >>> 2 | t << 30) ^ (t >>> 13 | t << 19) ^ (t >>> 22 | t << 10) }, v = function (t) { return (t >>> 6 | t << 26) ^ (t >>> 11 | t << 21) ^ (t >>> 25 | t << 7) }, w = function (t) { return (t >>> 7 | t << 25) ^ (t >>> 18 | t << 14) ^ t >>> 3 }, y = function (t) { return (t >>> 17 | t << 15) ^ (t >>> 19 | t << 13) ^ t >>> 10 } }(SHA256);
```
---
### Javascript diff (Old vs New)
```
function $(id) { 					      |	function $(id) {
  return document.getElementById(id);				  return document.getElementById(id);
}								}

async function sha256_hex_bytes(v) {			      |	function sha256_hex_bytes(v) {
  var typedArray = new Uint8Array(v.match(/[\da-f]{2}/gi).map	  var typedArray = new Uint8Array(v.match(/[\da-f]{2}/gi).map
    return parseInt(h, 16)					    return parseInt(h, 16)
  }))								  }))
  const hashBuffer = await crypto.subtle.digest('SHA-256', ty |	  return SHA256.createHash().update(typedArray).digest("hex")
  const hashArray = Array.from(new Uint8Array(hashBuffer));   <
  return hashArray.map(b => b.toString(16).padStart(2, '0')). <
}								}

function valid_key_format(v) {					function valid_key_format(v) {
  return v.match(/^[0-9a-f]{32}$/) !== null;			  return v.match(/^[0-9a-f]{32}$/) !== null;
}								}

function check_key_format() {					function check_key_format() {
  v = $('keyinput').value;					  v = $('keyinput').value;
  valid = valid_key_format(v);					  valid = valid_key_format(v);
  $('keysubmit').disabled = !valid;				  $('keysubmit').disabled = !valid;
  if (v.length > 0 && !valid) {					  if (v.length > 0 && !valid) {
    $('key_info').innerHTML = '<font color="red">the entered  |	    $('key_info').innerHTML = '<font style="color:yellow;">th
  } else {							  } else {
    $('key_info').innerHTML = '';			      |	    $('key_info').innerHTML = '&nbsp;';
  }								  }
  console.log(valid_key_format(v));			      |
  if (valid) {							  if (valid) {
    check_key();						    check_key();
  } else {						      <
    $('keysubmit').style.display = 'none';		      <
  }								  }
}								}

function form_valid() {						function form_valid() {
  return $('keysubmit').style.display !== 'none';	      |	  return !$('keysubmit').disabled;
}								}

function check_key() {						function check_key() {
  sha256_hex_bytes($('keyinput').value).then(r => {	      |	  r = sha256_hex_bytes($('keyinput').value)
    if (r === "1b2a3b5a92f47cbfd9f718412e941e04ac5f379bd14b95 |	  if (r === "bc4474b9e131ad126927ec743c6c4e5b6abda53810ef0d46
      $('key_info').innerHTML = '<font color="green">correct  |	    $('key_info').innerHTML = '<font class="statusok">correct
      $('keysubmit').style.display = 'inline';		      |	    //$('keysubmit').style.display = 'inline';
      $('keysubmit').disabled = false;			      |	    $('keysubmit').disabled = false;
    } else if (r == "93f21756aeeb5a9547cc62dea8d58581b0da4f23 |	  } else if (r == "93f21756aeeb5a9547cc62dea8d58581b0da4f2328
      $('key_info').innerHTML = '<font color="green">correct  |	    $('key_info').innerHTML = '<font class="statusok">correct
      $('keysubmit').style.display = 'inline';		      |	    //$('keysubmit').style.display = 'inline';
      $('keysubmit').disabled = false;			      |	    $('keysubmit').disabled = false;
    } else {						      |	  } else {
      $('key_info').innerHTML = '<font color="red">invalid de |	    $('key_info').innerHTML = '<font class="statusbad">invali
      $('keysubmit').style.display = 'none';		      |	    //$('keysubmit').style.display = 'none';
      $('keysubmit').disabled = true;			      |	    $('keysubmit').disabled = true;
    }							      |	  }
  })							      <
}								}

function update_status() {					function update_status() {
  var req = new XMLHttpRequest();				  var req = new XMLHttpRequest();
  req.addEventListener("load", (r) => {				  req.addEventListener("load", (r) => {
      try {						      |	    try {
        var s = JSON.parse(req.responseText);		      |	      var s = JSON.parse(req.responseText);
        switch(s.status) {				      |	      switch (s.status) {
        case "not_running":					        case "not_running":
          $("key").style.display = 'block';			          $("key").style.display = 'block';
          $("status").style.display = 'none';			          $("status").style.display = 'none';
        break;						      |	          break;

        case "running":						        case "running":
          $("key").style.display = 'none';			          $("key").style.display = 'none';
          $("status").innerHTML = 'decryption in progress (pr	          $("status").innerHTML = 'decryption in progress (pr
          $("status").style.display = 'block';			          $("status").style.display = 'block';
        break;						      |	          break;

        case "finished":					        case "finished":
          $("key").style.display = 'none';			          $("key").style.display = 'none';
          $("status").innerHTML = 'decryption successfully fi	          $("status").innerHTML = 'decryption successfully fi
          $("status").style.display = 'block';			          $("status").style.display = 'block';
        break;						      |	          break;
        }						      <
      } catch(e) {					      <
        window.location.reload();			      <
      }								      }
							      >	    } catch (e) {
							      >	      $("key").style.display = 'block';
							      >	      $("status").style.display = 'none';
							      >	      window.location.reload();
							      >	    }
  });								  });
  req.open("POST", "/index.html");				  req.open("POST", "/index.html");
							      >	  req.setRequestHeader("Content-Type", "application/x-www-for
  req.send("action=status");					  req.send("action=status");
}								}

function do_decrypt() {						function do_decrypt() {
  if (!form_valid()) {						  if (!form_valid()) {
    return false;						    return false;
  }								  }

  $("keyinput").disabled = true;				  $("keyinput").disabled = true;
  $("keysubmit").disabled = true;				  $("keysubmit").disabled = true;

  var req = new XMLHttpRequest();				  var req = new XMLHttpRequest();
  req.open("POST", "/index.html");				  req.open("POST", "/index.html");
							      >	  req.setRequestHeader("Content-Type", "application/x-www-for
  req.send("action=decrypt&key=" + $("keyinput").value);	  req.send("action=decrypt&key=" + $("keyinput").value);

  return false;							  return false;
}								}
							      <
window.setInterval(update_status, 2000);			window.setInterval(update_status, 2000);
```
