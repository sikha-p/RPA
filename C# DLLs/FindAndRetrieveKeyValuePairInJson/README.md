# Run PowerShell Script using DLL
This repository contains the DLL source code to run the Powershell script with input and output using DLL and the save the PowerShell script output to a bot variable.

Here is the DLL file name, 
RunPowershellScript.dll

**Note**: This DLL can be used in Automation Anywhere Bot to invoke a Powershell script and track the error messges properly.  When attempting to run the PowerShell script directly using Automation Anywhere's 'Run Program' command, it will be unable to track all the errors from the powershell script and debugging will be ineffective. To resolve this, you can use this DLL and execute the PowerShell script with the assistance of a DLL.
 


This DLL get the **PSHome** enviornment variable to run the Powershells script and start the process using the PSHome executable. Make sure your machine configured with the **PSHome** and **Path** environment variable.

![image](https://github.com/user-attachments/assets/0c19fbca-4f5c-43a4-be40-e44a0d8964c3)

Add an entry in the **Path** variable 

![image](https://github.com/user-attachments/assets/5b625595-3f74-475e-978b-d14cc4b269c7)

#### Typical Values for PSHome:
##### PowerShell 5.1 (Windows PowerShell)
```
C:\Windows\System32\WindowsPowerShell\v1.0
```

##### PPowerShell 7+ (Core Edition)
```
C:\Program Files\PowerShell\7
```
(If you're using a different version, replace 7 with the appropriate version number, e.g., 7.4.4.)


#### The DLL function "RunScript" has two input parameters
   
- **scriptFilePath**   ( string).
  -   The absolute file path of the PowerShell script
  -   eg: C:\\Users\u1\testScript.ps1
- **inputString**  (string).
  -  The input arguments to the PowerShell script are passed as a single string, with each argument separated by a delimiter ( semicolon ; as per the below given script). 
  -  eg: input1;input2;input3

You can provide the inputstring and the delimiter in the inputstring as per your Powershells script. 

Please find a sample code below.  
sampleScript.ps1

```

try{
    $allargs = $args[0].Split(";")
    $input1 = $allargs[0]
    $input2 = $allargs[1]
     # Concatenate input1 and input2
    $result = "$input1 $input2"

    # Output the concatenated result
    Write-Output $result
}
catch{
    #Handle error
    Write-Output "Error Details: $($_.Exception.Message)"
}
```
As per the above code the inputString variable to the DLL should be in the following format. Here the delimiter is semicolon.
input1;input2


**Note**: This repo contains the sample powershell script, sample A360 Bot that uses this DLL and the DLL source code. 
