# Oracle EBS application Operations using C# Class Library

This is a customized solution for a partcular page in Oracle EBS application. This project provides a C# class library that can help you to automate interactions with Oracle E-Business Suite application. Oracle EBS is a comprehensive suite of integrated business applications used by organizations worldwide for managing various business processes.

## Description

This is a customized solution for Payable invoices page in Oracle EBS application. By utilizing this library, you can perform mainly 2 operations within your Oracle EBS environment
* Scroll the Table scrollbar to the right most end 
* Extract the content from the Prompt message if exist.

By referring to this source code you can create your own solutions as per the requirement for any Oracle page.


## Key Features
* Scroll the Table scrollbar to the right most end  (Payable invoices table)
* Extract the content from the Prompt message if exist (Payabale invoices page prompts)

### Dependencies

* 1. WindowsAccessBridgeInterop.dll
* 2. Newtonsoft.Json.dll

### Executing program

* Open the source code solution(.sln) file in Visual Studio IDE 
* Build the project 
* Start
* Above step will create a DLL in Debug/Release - bin folder 
* Get the DLL and use it inside your Automation Anywhere Bot using DLL package 

### Functions in Class library
* 1. ConfigureLog(string logFolder, string logLevel)
** logFolder (eg : C\:user1\logs)
** logLevel eg : DEBUG/INFO/TRACE as per your requirement
* 2. getScrollBarClickCoordinates()
** This will return the co-ordinates(in the following order X,Y) of the scroll bar where we can click to move it to the right side. 
* 3. getPopUpDetails(Boolean returnCoordinates)
** Pass  "returnCoordinates" as true if want to return the pop up window coordinates. default value false.
** sample outputs : 
Note : It is mandatory to call "ConfigureLog" function before calling the other two DLL functions.  

## Author

Contributors names and contact info

ex. Sikha Poyyil 
Partner Solution Desk(PSD)
Automation Anywhere

## Version History

* 0.1
    * Initial Release

