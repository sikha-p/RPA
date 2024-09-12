# A DLL to connect to Exchange Web Service(EWS) Server using client credentials

A DLL to Connect to a EWS Server using client credentials grant flow and Read the Unread emails with content includes foriegn characters. 

## Description

This DLL can connect to EWS Server using client credentials grant flow and Read emails with content includes foriegn characters. You can use this inside the A360 Bot.
There are 2 functions inside the dll.

* Connect
    * clientId
    * tenantId
    * clientSecret
    * username
    * exchangeVersion (eg: Exchange2010_SP2)
                      (https://learn.microsoft.com/en-us/dotnet/api/microsoft.exchange.webservices.data.exchangeversion?view=exchange-ews-api)

* GetUnReadEmails
    * folderPath   (eg: Inbox/Test/Test2)
 
      
### Dependencies

* Microsoft.Exchange.WebServices.Data
* Microsoft.Identity.Clien
* Newtonsoft.Json


![image](https://github.com/user-attachments/assets/1ad002a7-66df-49d5-a5c9-c0bc97cc2dd6)

![image](https://github.com/user-attachments/assets/42efad93-8fd6-471f-b599-350e0883f153)


## Authors

Contributors names and contact info

ex. Sikha Poyyil 
