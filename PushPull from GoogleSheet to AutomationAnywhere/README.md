# PushPull from GoogleSheet to AutomationAnywhere
- This Git repo will help you to understand how to PushPull data from GoogleSheet to Automation Anywhere

## What is CEF application?
The Chromium Embedded Framework (CEF) is an open-source software framework for embedding a Chromium web browser within another application.

- Sample CEF Application EXE : CEFApplication.exe
- CEF Application source code : CEFApplication.zip
## How to launch the CEF Application?
- Clone this Github repo and unzip CEFApplication.zip. Use below command to run the CEF Application using command prompt
-     Go to folder
-     > CEFApplication.exe --remote-debugging-port=9222

- Or
-     > CEFApplication.exe "<URL>" --remote-debugging-port=9222
-     eg : > CEFApplication.exe "www.google.com" --remote-debugging-port=9222
Note : We should launch the CEF Application in debug mode on a particular port (eg: 9222) to allow the DLL to interact with it. 

## How to automate CEF Application?
 You can use a DLL to automate the CEF Application.
 
- The DLL source code : CEFApplicationAutomation.zip
- The DLL is internally using "OpenQA.Selenium" .NET library to interact with the CEF Application.


Note : We are using Selenium webdriver to interact with the CEF Application. If the default webdriver doesn't support, please download the appropriate one from the below link and use it inside the DLL source code. 
https://chromedriver.storage.googleapis.com/index.html

Default webdriver :  

`using (IWebDriver driver = new ChromeDriver(options))`

Custom Webdriver :  
       
`using (IWebDriver driver = new ChromeDriver(@"C:\Users\Sikha.P\Downloads\chromedriver_win32 (2)", options))`

### Note
You can use Automation Anywhere DLL package to call the DLL function and automate the CEF application. The DLL function  "connectAndPerformAutomation" will connect with the CEF Application with is running in debug mode on port 9222 with "www.google.com" as URL. It will connect to CEF Application and type "Automation Anyhwere" on the search textbox.


 ` var element = driver.FindElement(By.XPath("//*[@id='APjFqb']"));
   element.SendKeys("Automation Anywhere");`
                
Feel free to edit the DLL source code as per your URL and requirement and build a DLL. 
