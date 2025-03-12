# Bulk Enable/Disable Packages at the Control Room Level by Package Version

This repository provides a utility for Disabling or Enabling multiple Packages in the Control Room as bulk. Follow the steps below to utilize this utility effectively.

## Important Note
   - All bots using the specified package version will encounter errors. You need to manually go inside the bot select some other available package. 
   - This will impact scheduled and future runs of these bots, leading to preprocessing errors.
   - Please be aware of this before disabling package versions at the Control Room level.
   - ![image](https://github.com/user-attachments/assets/804fdf44-b659-43f0-915c-231e336693bb)


## Steps to Follow

1. **Import the ZIP File**
   - Import the file `Export.BulkDisableEnable-CRPackagesByVersion.sikha_creator.zip` into your control room.

2. **Modify Input File**
   - Open the **input.xlsx** file and navigate to the **Updates** sheet.
   - Fill in the packageNames and Package versions

   **Example:**
     ![image](https://github.com/user-attachments/assets/8b11bd8b-3b4f-448b-b765-7992f350c044)


3. **Run the BulkDisableEnable-CRPackagesByVersion Bot**
   - Next, run the `BulkDisableEnable-CRPackagesByVersion` bot to disable or enable the Control room package versions. 
   - Ensure you specify the `inputOutputFolder` containing the modified `input.xlsx` file.
   - Status value can be either **Enable** or **Disable**
   -    ![image](https://github.com/user-attachments/assets/d5db1284-9abe-4942-9cdc-25f63149667f)


6. **Review Update Status**
   - The bot will update the commands with the specified attribute values and create a `Post_update_report` sheet for you to review the update status.
   -    ![image](https://github.com/user-attachments/assets/cf7dd909-6dcc-4ac2-b7c4-ccbd3f2b1b87)

   - If you encounter an "Error" status for any package, please refer to the log file for more details.
   - A log file will be generated in the `inputOutputFolder`, named `bulkDisableCRPackagesByVersionLogs.log`.

## Note

Please make sure that the best practices are followed, and changes are done on development server before promoting to the production environment.




