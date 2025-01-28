# Encryption of Google Sheet Values

This repository provides a utility for encrypting values in a Google Sheet and decrypting them using a bot.

## Instructions

1. **Add the Script to Google Sheets**
   - In the App Script editor of your Google Sheet, copy and paste the code from the `appScript.js` file available in this repository.
   - This code utilizes a library to encode the values.
![image](https://github.com/user-attachments/assets/15c86361-9877-446f-bc8f-874f66a6c41b)


2. **Import the Required Library**
   - Visit the following URL to access the library:  
     [https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/aes.js](https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/aes.js)
   - Copy the entire code from this page.
   - In the App Script editor, create a new file in the **Files** section and paste the copied code into it.

3. **Use the 'crypto-js.js' file to decrypt the data, add your key correctly.

4. Use the 'crypto-js.js' in your javascript package on the control room.

![image](https://github.com/user-attachments/assets/50b023a8-8211-4889-ad7f-5a8c54d0d2bc)



## Additional Instructions

** To hide your key, set properties from the google sheets.

** Add the 'setProperties.js' to as an additional file in the app script.
