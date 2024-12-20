# PushPull from GoogleSheet to AutomationAnywhere
- This Git repo will help you to understand how to PushPull data from GoogleSheet to Automation Anywhere

## How to Pull data from GoogleSheet to Automation Anywhere
- You can use GoogleSheet Automation Anywhere Command to connect with Google Sheet using Client ID and Secret. And Open the Google SpreadSheet using the SpreadSheet ID from the and put it in the command. Retrieve the GoogleSheet Data using GoogleSheet: Get multiple cells command and Save the output to a DataTable Variable.

![image](https://github.com/user-attachments/assets/bc0dc3a2-d880-4881-90f3-5d340ea9dbce)


## How to Push data from GoogleSheet to Automation Anywhere WLM Queue based on the GoogleSheet events
- You can define triggers through Google Apps Script, which is a JavaScript-based language for extending Google Sheets and other Google Workspace apps.

Here's how you can define triggers and perform operations when those triggers occur:

1. Open Google Sheets and Script Editor
Open the Google Sheets document.
Go to Extensions > Apps Script to open the script editor.
2. Writing the Trigger Functions

 ![image](https://github.com/user-attachments/assets/602e3c56-277d-40ee-9cf6-fd40cd6e102d)

 ![image](https://github.com/user-attachments/assets/d72e5179-bd80-4b71-acbf-d73b113c40ff)


Here is a sample script 
![image](https://github.com/user-attachments/assets/2ba0ef83-f252-455c-a1c3-277164376850)

Attached OnEdit() function with Edit event and, we are calling Automation Anywhere WLM Add workitems to the Queue API inside. This will add the workitems to the queue with the modified data when ever the Edit event get trigered. 

Note: Please find the GoogleScript for adding workitems to the queue from the repo "GoogleScript.txt" file







