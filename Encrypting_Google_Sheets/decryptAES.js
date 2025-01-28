function decryptAES() {
  
	var key = "enter_your_key");
	var encryptedStr = "U2FsdGVkX1+3CE87k2SwbSIK1JP4QFK1yOsk/E++bWM="; // Encrypted string

	var decryptedMessage = CryptoJS.AES.decrypt(encryptedStr, key).toString(CryptoJS.enc.Utf8);
	return decryptedMessage // Output: sample text
}
