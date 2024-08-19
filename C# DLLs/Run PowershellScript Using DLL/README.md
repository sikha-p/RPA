# Run PowerShell Script using DLL
This repository contains the DLL source code to run the Powershell script using DLL

The main DLL has one dependant file
RunPowershellScript.dll


This DLL get the **PSHome** enviornment variable to run the Powershells script and start the process using the PSHome executable. Make sure your machine configured with the **PSHome** and **PSModulePath** environment variables.


#### The DLL function "RunScript" has two input parameters
   
- **scriptFilePath**   ( string).
  -   The absolute file path of the PowerShell script
  -   eg: C:\\Users\u1\testScript.ps1
- **inputString**  (string).
  -  The input arguments to the PowerShell script are passed as a single string, with each argument separated by a delimiter ( semicolon ; as per the below given script). 
  -  eg: ClientID;CertificatePassword;Tenant;next_parameter;

You can provide the inputstring and the delimiter in the inputstring as per your Powershells script. 

Please find a sample code below.  
connectToSharePointWithCert.ps1

```

try{
    $allargs = args[0].Split(";")
    $ClientId = $allargs[0]
    $CertificatePath = $allargs[1]
    $CertificatePassword =  $allargs[2]
    $CertificatePassword = ConvertTo-SecureString -AsPlainText $CertificatePassword -Force
    $Url = $allargs[3]
    $Tenant = $allargs[4]
    $file_path =$allargs[7]
    $foldername = $allargs[5]
    Connect-PnPOnline -ClientId $ClientId -CertificatePath $CertificatePath -CertificatePassword $CertificatePassword -Url $Url -Tenant $Tenant 
   Add-PnPFile -Folder "$Foldername" -Path $file_path
   Disconnect-PnPOnline 
}
catch{
    #Handle error
    Write-Output "Error Details: $($_.Exception.Message)"
}
```
As per the above code the inputString variable to the DLL should be in the following format. Here the delimiter is semicolon.
clientId;certificatePath;certificatePassword;url;Tenant;foldername;somevalue;filepath


**Note**: This DLL can be used in Automation Anywhere Bot to invoke a Powershell script and track the error messges properly.  When attempting to run the PowerShell script directly using Automation Anywhere's 'Run Program' command, it will be unable to track all the errors from the powershell script and debugging will be ineffective. To resolve this, you can use this DLL and execute the PowerShell script with the assistance of a DLL.
 

