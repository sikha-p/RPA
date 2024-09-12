using Microsoft.Exchange.WebServices.Data;
using Microsoft.Identity.Client;
using System;
using System.Data;
using System.Threading.Tasks;
using Newtonsoft.Json;
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

        public string Connect(string clientId, string tenantId, string clientSecret, string username, string exchangeVersion)
        {
            try
            {
                _tenantId = tenantId;
                _clientId = clientId;
                _clientSecret = clientSecret;
                _username = username;

                // Convert input string to ExchangeVersion enum
                if (!Enum.TryParse(exchangeVersion, out ExchangeVersion exchangeVersion_))
                {
                    Console.WriteLine("Invalid Exchange version specified.");
                    return "Invalid Exchange version specified.";
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
                return "Connected sucecssfully";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
          
           

        }

        public String GetUnReadEmails(string folderPath)
        {

            try
            {
                // Specify the email address to impersonate
                service.ImpersonatedUserId = new ImpersonatedUserId(ConnectingIdType.SmtpAddress, _username);
                DataTable dataTable = new DataTable();

                // Get the target folder by traversing the folder hierarchy
                Folder targetFolder = FindFolderByPath(folderPath);
                if (targetFolder == null)
                {
                    Console.WriteLine("Folder not found.");
                    return JsonConvert.SerializeObject(new DataTable());
                }

                // Search for unread emails in the target folder
                SearchFilter searchFilter = new SearchFilter.IsEqualTo(EmailMessageSchema.IsRead, false);
                ItemView view = new ItemView(10);
                FindItemsResults<Item> findResults = service.FindItems(targetFolder.Id, searchFilter, view);

                string[] emailItems = new string[0];

                foreach (Item item in findResults.Items)
                {
                    if (item is EmailMessage)
                    {
                        EmailMessage message = (EmailMessage)item;
                    }
                }
                // Create a DataTable with columns for email properties

                dataTable.Columns.Add("Subject", typeof(string));
                dataTable.Columns.Add("From", typeof(string));
                dataTable.Columns.Add("ReceivedTime", typeof(DateTime));

                // Populate the DataTable with email data
                foreach (Item item in findResults.Items)
                {
                    if (item is EmailMessage message)
                    {
                        DataRow row = dataTable.NewRow();
                        row["Subject"] = message.Subject;
                        row["From"] = message.From.Address;
                        row["ReceivedTime"] = message.DateTimeReceived;
                        dataTable.Rows.Add(row);
                    }
                }
                return JsonConvert.SerializeObject(dataTable);
            }
            catch(Exception ex)
            {
                return ex.Message;
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
    }
}
