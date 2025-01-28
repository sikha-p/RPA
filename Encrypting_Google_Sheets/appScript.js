function myFunction() {
  var scriptProperties = PropertiesService.getScriptProperties();
  var key = scriptProperties.getProperty('KEY');
  // Logger.log(key);
  
  // Access the Google Sheet and get the value from a specific cell (e.g., A1)
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var cellValue = String(sheet.getRange("A1").getValue());  // Change "A1" to the desired cell
  
  // Encrypt the cell value
  var encryptedMessage = CryptoJS.AES.encrypt(cellValue, key).toString();
  
  // Decrypt the encrypted value
  var decryptedMessage = CryptoJS.AES.decrypt(encryptedMessage, key).toString(CryptoJS.enc.Utf8);
  
  // Log the original value, encrypted message, and decrypted message
  console.log(cellValue);
  Logger.log("Encrypted: " + encryptedMessage);
  Logger.log("Decrypted: " + decryptedMessage);
  
  // Optionally, write the encrypted message back to another cell (e.g., B1)
  sheet.getRange("B1").setValue(encryptedMessage);
}
