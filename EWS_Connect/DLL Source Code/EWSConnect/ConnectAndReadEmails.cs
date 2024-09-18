using Microsoft.Exchange.WebServices.Data;
using Microsoft.Identity.Client;
using System;
using System.Data;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

namespace EWSConnect
{
    class ConnectAndReadEmails
    {
        public string _tenantId;
        public string _clientId;
        public string _clientSecret;
        public string _username;
        public string ewsUrl = "https://outlook.office365.com/EWS/Exchange.asmx";
        ExchangeService service;
        string foldernotfoundError = "";
        public string authType = "";

        public string ConnectWithBasicAuth(string username, string password,string domain,string exchangeVersion)
        {
            try
            {
                authType = "BASIC";
                _username = username;

                // Convert input string to ExchangeVersion enum
                if (!Enum.TryParse(exchangeVersion, out ExchangeVersion exchangeVersion_))
                {
                    Logger.LogToFile("ERROR: Invalid Exchange version specified.Please refer https://learn.microsoft.com/en-us/dotnet/api/microsoft.exchange.webservices.data.exchangeversion?view=exchange-ews-api");
                    return "ERROR: Invalid Exchange version specified.";
                }

               
                // Initialize the ExchangeService
                service = new ExchangeService(exchangeVersion_)
                {
                    Url = new Uri(ewsUrl),
                    Credentials = new WebCredentials(username, password, domain)
                };



                Logger.LogToFile("INFO: Connected successfully!");
                return "Connected sucecssfully " + Logger.getLogFolderPath();
            }
            catch (Exception ex)
            {
                Logger.LogToFile("ERROR: " + ex.Message);
                return "ERROR: " + ex.Message;
            }
        }

        public string ConnectWithClientCredentialsAuth(string clientId, string tenantId, string clientSecret, string username, string exchangeVersion)
        {
            try
            {
                authType = "CLIENT_CREDENTIALS";
                _tenantId = tenantId;
                _clientId = clientId;
                _clientSecret = clientSecret;
                _username = username;

                // Convert input string to ExchangeVersion enum
                if (!Enum.TryParse(exchangeVersion, out ExchangeVersion exchangeVersion_))
                {
                    Logger.LogToFile("ERROR: Invalid Exchange version specified.Please refer https://learn.microsoft.com/en-us/dotnet/api/microsoft.exchange.webservices.data.exchangeversion?view=exchange-ews-api");
                    return "ERROR: Invalid Exchange version specified.";
                }

                // Get OAuth2 token
                var authResult = GetToken(clientId, clientSecret, tenantId);
                // Convert input string to ExchangeVersion enum

                // Initialize the ExchangeService
                service = new ExchangeService(exchangeVersion_)
                {
                    Url = new Uri(ewsUrl),
                    Credentials = new OAuthCredentials(authResult.AccessToken)
                };
                Logger.LogToFile("INFO: Connected successfully!");
                return "Connected sucecssfully "+ Logger.getLogFolderPath();
            }
            catch (Exception ex)
            {
                Logger.LogToFile("ERROR: "+ ex.Message);
                return "ERROR: "+ex.Message;
            }
        }

        public String GetEmails(string filterCondition,string folderPath,string targetFolderForFilteredItems,string filterRegexPattern)
        {

            try
            {
                if(authType == "CLIENT_CREDENTIALS")
                {
                    // Specify the email address to impersonate
                    service.ImpersonatedUserId = new ImpersonatedUserId(ConnectingIdType.SmtpAddress, _username);


                }

                // Get the target folder by traversing the folder hierarchy
                Folder targetFolder = FindFolderByPath(folderPath);
                if (targetFolder == null)
                {
                    Logger.LogToFile("INFO: Folder not found. folder path: "+ folderPath);
                    return "ERROR: Folder not found.. folder path: " + folderPath;
                }
                SearchFilter searchFilter = null;
                // Search for unread emails in the target folder
                switch (filterCondition)
                {
                    case "READ":
                        searchFilter = new SearchFilter.IsEqualTo(EmailMessageSchema.IsRead, true);
                        break;
                    case "UNREAD":
                        searchFilter = new SearchFilter.IsEqualTo(EmailMessageSchema.IsRead, false);
                        break;
                    case "ALL":
                        break;

                }

                int pageSize = 100; // Set the page size to a larger number, e.g., 100
                ItemView view = new ItemView(pageSize);
                view.PropertySet = new PropertySet(BasePropertySet.IdOnly); // Adjust as needed
                view.Traversal = ItemTraversal.Shallow; // Adjust as needed
                FindItemsResults<Item> findResults;
                do
                {
                    findResults = service.FindItems(targetFolder.Id, searchFilter, view);
                    foreach (Item item in findResults.Items)    
                    {
                        // Process each item
                        if (item is EmailMessage message)
                        {
                            ItemId emailItemId = new ItemId(message.Id.UniqueId);
                            EmailMessage email = EmailMessage.Bind(service, emailItemId, new PropertySet(BasePropertySet.FirstClassProperties, EmailMessageSchema.Body));
                            string subject = email.Subject;
                            if (ContainsForeignCharacters(subject, filterRegexPattern))
                            {
                                Logger.LogToFile("INFO: Regex pattern matched.Subject contains foreign characters. subject: "+ subject + " , Mail ID: "+emailItemId);
                                Logger.LogToFile("INFO: Target folder to move mail item " + targetFolderForFilteredItems);
                                MoveMail(targetFolderForFilteredItems, emailItemId.ToString());
                            }
                            else
                            {
                                Logger.LogToFile("INFO: Subject doesn't contain foreign characters. subject: " + subject + " , Mail ID: " + emailItemId);
                            }

                        }
                    }

                    view.Offset += findResults.Items.Count;
                } while (findResults.MoreAvailable);
                if (foldernotfoundError != "")
                {
                    Logger.LogToFile(foldernotfoundError);
                    return foldernotfoundError;
                }
                else
                {
                    Logger.LogToFile("INFO: Completed");
                    return "Successfully moved items";
                }
                
            }
            catch(Exception ex)
            {
                Logger.LogToFile("ERROR: " + ex.Message);
                return "ERROR: "+ex.Message;
            }
          
          
        }

        public static AuthenticationResult GetToken(string clientId, string clientSecret, string tenantId)
        {
            return GetTokenAsync(clientId, clientSecret, tenantId).GetAwaiter().GetResult();
        }


        public static async Task<AuthenticationResult> GetTokenAsync(string clientId,string clientSecret,string tenantId)
        {
            IConfidentialClientApplication app = ConfidentialClientApplicationBuilder.Create(clientId)
                .WithClientSecret(clientSecret)
                .WithAuthority(new Uri($"https://login.microsoftonline.com/{tenantId}"))
                .Build();

            string[] scopes = new string[] { "https://outlook.office365.com/.default" };

            return await app.AcquireTokenForClient(scopes).ExecuteAsync();
        }

        private Folder FindFolderByPath(string folderPath)
        {
            string prefix = "Inbox/";

            if (folderPath.StartsWith(prefix))
            {
                folderPath = folderPath.Substring(prefix.Length);
            }
            string[] pathSegments = folderPath.Split('/');
            Folder folder = null;
            FolderView folderView = new FolderView(100);

            foreach (string segment in pathSegments)
            {
                FindFoldersResults findResults;

                if (folder == null)
                {
                    // Search in the root of the inbox
                    findResults = service.FindFolders(WellKnownFolderName.Inbox, new SearchFilter.IsEqualTo(FolderSchema.DisplayName, segment), folderView);
                }
                else
                {
                    // Search within the current folder
                    findResults = service.FindFolders(folder.Id, new SearchFilter.IsEqualTo(FolderSchema.DisplayName, segment), folderView);
                }

                // Check if any folders were found
                if (findResults.Folders.Count > 0)
                {
                    // Get the first folder found
                    folder = findResults.Folders[0];
                }
                else
                {
                    // Folder not found
                    return null;
                }
            }

            return folder;
        }

        static bool ContainsForeignCharacters(string input, string pattern)
        {
            // Regex pattern to match specified ranges of characters
            if (pattern == "")
            {
                pattern = @"[\x00-\x08\x0B\x0C\x0E-\x1F]|[\uD800-\uDBFF][\uDC00-\uDFFF]|[\uFDD0-\uFDEF]|[\uFFFE\uFFFF]|[\uD83F\uDFFE\uD83F\uDFFF]|[\uD87F\uDFFE\uD87F\uDFFF]|[\uD8BF\uDFFE\uD8BF\uDFFF]|[\uD8FF\uDFFE\uD8FF\uDFFF]|[\uD93F\uDFFE\uD93F\uDFFF]|[\uD97F\uDFFE\uD97F\uDFFF]|[\uD9BF\uDFFE\uD9BF\uDFFF]|[\uD9FF\uDFFE\uD9FF\uDFFF]|[\uDA3F\uDFFE\uDA3F\uDFFF]|[\uDA7F\uDFFE\uDA7F\uDFFF]|[\uDABF\uDFFE\uDABF\uDFFF]|[\uDAFF\uDFFE\uDAFF\uDFFF]|[\uDB3F\uDFFE\uDB3F\uDFFF]|[\uDB7F\uDFFE\uDB7F\uDFFF]|[\uDBBF\uDFFE\uDBBF\uDFFF]|[\uDBFF\uDFFE\uDBFF\uDFFF]";

            }
            Logger.LogToFile("INFO: Regex pattern" + pattern);
            Regex regex = new Regex(pattern);

            return regex.IsMatch(input);
        }

      

        public string MoveMail(string targetFolderPath, string emailID)
        {
            try
            {
                Folder targetFolder = FindFolderByPath(targetFolderPath);
                if (targetFolder == null)
                {
                    Logger.LogToFile("ERROR: Folder not found. folder path: "+ targetFolderPath);
                    foldernotfoundError= "ERROR: Target folder not found.folder path: "+ targetFolderPath;
                    return "Folder not found.";
                }
                //FolderId targetFolderId = new FolderId(WellKnownFolderName.Inbox); // Replace with the target folder ID
                EmailMessage email = EmailMessage.Bind(service, emailID, new PropertySet(BasePropertySet.FirstClassProperties, EmailMessageSchema.Body));

                // Move the email to the target folder
                email.Move(targetFolder.Id);
                Logger.LogToFile("INFO: Mail moved successfully to "+targetFolderPath+" Mail ID: "+ emailID);
                return "Mail moved successfully ";
            }
            catch (Exception ex)
            {
                Logger.LogToFile("ERROR: " + ex.Message);
                return "ERROR: " +ex.Message;
            }
        }


    }
}
