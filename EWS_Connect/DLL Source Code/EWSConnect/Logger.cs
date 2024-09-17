using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml;

namespace EWSConnect
{
    class Logger
    {
        public static void LogToFile(string line)
        {
            string logFile = "EWSConnectAndMoveFilteredEmails.log";
            string logFileFolderPath = getLogFolderPath();

            DateTime dateNow = DateTime.Now;
            //2022 - Mar - 23 Wed 09:09:50.623
            string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");

            if (!File.Exists(logFileFolderPath + logFile))
            {
                if (!Directory.Exists(logFileFolderPath))
                {
                    Directory.CreateDirectory(logFileFolderPath);
                }
                File.Create(logFileFolderPath + logFile).Dispose();

                using (TextWriter tw = new StreamWriter(logFileFolderPath + logFile, true))
                {
                    tw.WriteLine(now + ": " + line);
                }

            }
            else if (File.Exists(logFileFolderPath + logFile))
            {
                using (TextWriter tw = new StreamWriter(logFileFolderPath + logFile, true))
                {
                    tw.WriteLine(now + ": " + line);
                }
            }
        }

        public static string getLogFolderPath()
        {
            string AAInstallationPath = checkInstalled("Automation Anywhere Bot Agent");
            XmlDocument xml = new XmlDocument();
            string xmlFilePath = AAInstallationPath + @"config\nodemanager-logging.xml";
            xml.Load(xmlFilePath);
            //XmlNodeList nodelist = xml.SelectNodes("//Property[@name='logPath']");
            XmlNode node = xml.SelectSingleNode("//Property[@name='logPath']");
            string logpath = node.InnerText + "/";
            if (logpath.Contains("${env:PROGRAMDATA}"))
            {
                string pgrmDataEnv = Environment.GetEnvironmentVariable("PROGRAMDATA");
                logpath = logpath.Replace("${env:PROGRAMDATA}", pgrmDataEnv);
                logpath = logpath.Replace("\\", "/");
            }
            return logpath;
        }
        private static string checkInstalled(string findByName)
        {
            string displayName;
            string InstallPath;
            string registryKey = @"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall";

            //64 bits computer
            RegistryKey key64 = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Registry64);
            RegistryKey key = key64.OpenSubKey(registryKey);

            if (key != null)
            {
                foreach (RegistryKey subkey in key.GetSubKeyNames().Select(keyName => key.OpenSubKey(keyName)))
                {
                    displayName = subkey.GetValue("DisplayName") as string;
                    if (displayName != null && displayName.Contains(findByName))
                    {

                        InstallPath = subkey.GetValue("InstallLocation").ToString();

                        return InstallPath; //or displayName

                    }
                }
                key.Close();
            }

            return null;
        }
    }

}
