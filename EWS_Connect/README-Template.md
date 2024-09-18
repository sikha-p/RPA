# A DLL to connect to Exchange Web Service(EWS) Server using client credentials


A DLL to connect to an EWS server using client credentials grant flow, read all/read/unread emails, filter out the emails that match the provided regex pattern with its subject, and move those emails to a specified target folder.

## Description

You can use this DLL inside the A360 Bot.Please find the exported bot from the same repository.
There are 3 functions inside the dll.

* ConnectWithBasicAuth
    * username
    * password
    * domain
    * exchangeVersion (eg: Exchange2010_SP2)
                      (https://learn.microsoft.com/en-us/dotnet/api/microsoft.exchange.webservices.data.exchangeversion?view=exchange-ews-api)

* ConnectWithClientCredentialsAuth
    * clientId
    * tenantId
    * clientSecret
    * username
    * exchangeVersion (eg: Exchange2010_SP2)
                      (https://learn.microsoft.com/en-us/dotnet/api/microsoft.exchange.webservices.data.exchangeversion?view=exchange-ews-api)


* GetEmails
    * filterCondition ( options : ALL/READ/UNREAD)
    * folderPath   (eg: Inbox/Test/Test2)
    * targetFolderForFilteredItems  (eg: Inbox/Test/Test2)
    * filterRegexPattern   (eg : [^\x00-\x7F] )


       If you pass the "filterRegexPattern" value as empty string it will run with the default regex configured inside the DLL. Please find the default regex below. This has been generated as per the characters specified in the following Automation Anywhere documenation https://docs.automationanywhere.com/bundle/enterprise-v2019/page/enterprise-cloud/topics/aae-client/bot-creator/commands/cloud-using-connect-action.html

[\x00-\x08\x0B\x0C\x0E-\x1F]|[\uD800-\uDBFF][\uDC00-\uDFFF]|[\uFDD0-\uFDEF]|[\uFFFE\uFFFF]|[\uD83F\uDFFE\uD83F\uDFFF]|[\uD87F\uDFFE\uD87F\uDFFF]|[\uD8BF\uDFFE\uD8BF\uDFFF]|[\uD8FF\uDFFE\uD8FF\uDFFF]|[\uD93F\uDFFE\uD93F\uDFFF]|[\uD97F\uDFFE\uD97F\uDFFF]|[\uD9BF\uDFFE\uD9BF\uDFFF]|[\uD9FF\uDFFE\uD9FF\uDFFF]|[\uDA3F\uDFFE\uDA3F\uDFFF]|[\uDA7F\uDFFE\uDA7F\uDFFF]|[\uDABF\uDFFE\uDABF\uDFFF]|[\uDAFF\uDFFE\uDAFF\uDFFF]|[\uDB3F\uDFFE\uDB3F\uDFFF]|[\uDB7F\uDFFE\uDB7F\uDFFF]|[\uDBBF\uDFFE\uDBBF\uDFFF]|[\uDBFF\uDFFE\uDBFF\uDFFF]

      
### Dependencies

* Mnt.Microsoft.Exchange.WebServices.Data.dll
* Microsoft.Identity.Client.dll
* Microsoft.IdentityModel.Abstractions.dll



![image](https://github.com/user-attachments/assets/5208eb4a-e90c-41dc-9fdc-df62d38368f2)


![image](https://github.com/user-attachments/assets/d45877ef-6fe9-435f-ad08-8cb768bebe74)


This A360 Bot will generate a log file in the following path "C:\ProgramData\AutomationAnywhere\BotRunner\Logs\EWSConnectAndMoveFilteredEmails.log". This can be used for the debugging purpose.


## Authors

Contributors names and contact info

ex. Sikha Poyyil 
