# Bulk Bot Command Updater

This repository provides a utility for updating multiple command attribute values in bots within a specified folder. Follow the steps below to utilize the Bulk Bot Command Updater effectively.

## Steps to Follow

1. **Import the ZIP File**
   - Import the file `Export.BulkBotCommandUpdater.sikha_creator.zip` into your control room.

2. **Modify Input File**
   - Open the `Input.xlsx` file and navigate to the "updates" sheet.
   - Fill in the required commands and attributes.

   **Example:**
   ![image](https://github.com/user-attachments/assets/61b50e53-0331-4fd8-8c50-4a37841175bd)


3. **Retrieve Command Information**
   - To obtain the Command name, Package name, Attribute name, and Attribute value:
     1. Create a new bot and drag and drop the command listed in the "BulkBotCommandUpdater" input Excel file.
     2. Fill in the required details with placeholder data.
     3. Inspect the page by pressing `F12` and navigate to the Network tab.
     4. Search for the API endpoint:
        ```
        <CR_URL>/v2/repository/files/<Bot_id>/content?hasErrors=false
        ```
     5. Check the request payload and the `nodes` object; you will find the command name, package name, and attribute name there.
     6.   ![image](https://github.com/user-attachments/assets/8190475f-10bc-4b82-b779-0b52532e30a0)


4. **Generate Pre-Update Report**
   - Execute the `BulkBotCommandUpdater-Report` bot to generate a report of the bots in the specified folder, which includes the given commands.

   - This Utility will work on the Public folder.Please provide your Public folder ID as the input.  So no need to check out the bots before running this Utility bots. Keep all your bots in the public folder and give the public folder ID. Refer the image given below for the public folder ID sample
   -    ![image](https://github.com/user-attachments/assets/873bd31b-f348-47ec-839e-f2b2509216fb)


   - This will add two additional sheets to the `Input.xlsx` file: "Bot_IDs" and "Pre-update-report".

5. **Run the Bulk Updater**
   - Next, run the `BulkBotCommandUpdater` bot to update the commands and attributes within the bots.
   - Ensure you specify the folder containing the updated `Input.xlsx` file (which now has three sheets).

6. **Review Update Status**
   - The bot will update the commands with the specified attribute values and create a `Post_update_report` sheet for you to review the update status.
   - A log file will be generated in the `inputOutputFolder`, named `botCommandMassUpdater.log`.

## Note

Please make sure that the best practices are followed, and changes are done on development server before promoting to the production environment.




