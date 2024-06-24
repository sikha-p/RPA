# CEF Application Automation using DLL
- The folders contains the sample CEF Application and a C#.NET Console application to Invoke the sample CEF Application
- CEF Application EXE : CEFApplication.exe
- CEF Application source code : CEFApplication.zip

- Use below command to run the CEF Application using command prompt
-     Go to folder
-     > CEFApplication.exe --remote-debugging-port=9222

- Or
-     > CEFApplication.exe "<URL>" --remote-debugging-port=9222
-     eg : > CEFApplication.exe "www.google.com" --remote-debugging-port=9222

- The DLL source code : CEFApplicationAutomation.zip
- The DLL is internally using "OpenQA.Selenium" .NET library to interact with the CEF Application.

