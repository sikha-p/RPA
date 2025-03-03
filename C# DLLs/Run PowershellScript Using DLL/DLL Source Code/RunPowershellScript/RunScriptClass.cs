using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RunPowershellScript
{
    class RunScriptClass
    {
        public static string RunScript(string scriptFilePath, string inputString)
        {
            try
            {
                // Get the PSHome environment variable
                string psHome = Environment.GetEnvironmentVariable("PSHome");

                if (string.IsNullOrEmpty(psHome))
                {
                    Console.WriteLine("PSHome environment variable is not set.");
                    return "PSHome environment variable is not set.";
                }

                // Construct PowerShell executable path
                string powershellExe = Path.Combine(psHome, "pwsh.exe");

                // If pwsh.exe is missing, try Windows PowerShell
                if (!File.Exists(powershellExe))
                {
                    powershellExe = Path.Combine(psHome, "powershell.exe");
                    
                }

                //return powershellExe;
                // Final check if PowerShell executable exists
                if (!File.Exists(powershellExe))
                {
                    return $"PowerShell executable not found at: {powershellExe}";
                }

                // Define the PowerShell script to run
                string scriptPath = scriptFilePath;
                string scriptArgument = "\"" + inputString.Replace("\"", "\"\"") + "\"";
            

                // Create a new process to run PowerShell
                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = powershellExe,
                    Arguments = $"-ExecutionPolicy RemoteSigned -File \"{scriptPath}\" {scriptArgument}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };


                using (Process process = new Process { StartInfo = startInfo })
                {
                    // Start the process
                    process.Start();

                    // Read the output
                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();

                    // Wait for the process to exit
                    process.WaitForExit();

                    // Display the output


                    if (!string.IsNullOrEmpty(error))
                    {
                        Console.WriteLine("Error:");
                        return "Error Details :" + error;
                    }
                    else
                    {
                        return output;
                    }
                }
            }
            catch (Exception ex)
            {
                 return "Error Details :" + ex.Message + " " + ex.StackTrace.ToString();
            }

        }

      
    }
}
