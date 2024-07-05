## Computation On Automation Anywhere Co-Pilot FORM

This Google chrome extension can help you to interact with the Automation Anywhere Co-pilot FORM elements. Can extract the values from the FORM elements & change the value of other FORM elements instantly. 

For example :

You have three text boxes on the co-pilot form: Ineligible Amount, Total Amount, and Approved Amount. The Total Amount has a default value and is a read-only field. The 'Approved Amount' needs to be calculated instantly when you enter the 'Ineligible Amount'.

![image](https://github.com/sikha-p/RPA/assets/84059776/ca843147-acca-43f0-92ad-9efd097bd460)



The calculation shown in the image below is performed using the extension.


![image](https://github.com/sikha-p/RPA/assets/84059776/956c2bbe-54d2-4909-86e9-34d37403116d)


### How to Configure and launch this extension? 
------------------------------------------------------------------------------
1. Clone git repo and get the "CalculateApprovedAmount" extension.
2. Open the folder and edit 'manifest.json' file
3. Change your Control Room URL in manifest.json
   "content_scripts": [
    {
      "matches": [ "https://<YOUR-CONTROL-ROOM-URL>/aari*" ],

2. Inspect your Co-pilot form(Open Co-pilot page -> Start your public process) and get the Js path of the text fields (Ineligible amount, Total Amount, approved amount)
3. Change the below lines in "content.js" accordingly

           const IneligibleAmountEle = document.querySelector("#elem-TextBox2 > div > input");
           const TotalAmountEle = document.querySelector("#elem-TextBox0 > div > input");
           const ApprovedAmountEle = document.querySelector("#elem-TextBox1 > div > input");

   Note :  Please try this chrome extension only after you check-in your Co-pilot process. Run the process and get the Js path of the fields.

5. How to load the extension to chrome browser? 
    i) Go to chrome://extensions/
    ii) Enable Developer mode
    iii) Click on "Load unpacked" and select the extension folder "CalculateApprovedAmount"
    iv) Once the extension is loaded you can see that in the extensions list
    v) Open Co-pilot page -> Start your public process
   v1) Edit "Ineligigble amount" value. 




![image](https://github.com/sikha-p/RPA/assets/84059776/6e9895f1-006e-45aa-a178-7687e3bcd598)

   



