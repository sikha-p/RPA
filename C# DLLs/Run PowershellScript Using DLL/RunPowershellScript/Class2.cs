using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RunPowershellScript
{
    class Class2
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

                // Construct the path to the PowerShell executable
                string powershellExe = psHome;//System.IO.Path.Combine(psHome, "pwsh.exe");
                // Check if the PowerShell executable exists
                if (!System.IO.File.Exists(powershellExe))
                {
                    Console.WriteLine($"PowerShell executable not found at: {powershellExe}");
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
