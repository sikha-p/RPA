using System;
using System.IO;

namespace OracleEBSOperations
{
    class Log
    {
        public static string logFolder_;
        public static string loggerLevel_;
        public static string logFile_ = "OracleEBSOperationsDLL.log";
        public static void Configure(string logFolder, string loggerLevel)
        {
            logFolder_ = logFolder;
            loggerLevel_ = loggerLevel;
           

            if (!File.Exists(logFolder_ + logFile_))
            {
                if (!Directory.Exists(logFolder_))
                {
                    Directory.CreateDirectory(logFolder_);
                }
                File.Create(logFolder_ + logFile_).Dispose();
            }
        }
        public static void Debug(String message)
        {

            if(loggerLevel_.ToLower() == "debug")
            {
                DateTime dateNow = DateTime.Now;
                string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " DEBUG - " + message);
                }
            }
              
        }
        public static void Info(String message)
        {
            if (loggerLevel_.ToLower() == "info")
            {
                DateTime dateNow = DateTime.Now;
                string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " INFO - " + message);
                }
            }
        }
        public static void Trace(String message)
        {
            if (loggerLevel_.ToLower() == "trace")
            {
                DateTime dateNow = DateTime.Now;
                string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " TRACE - " + message);
                }
            }
        }

        public static void Error(String message)
        {
            if (loggerLevel_.ToLower() == "info" || loggerLevel_.ToLower() == "trace" || loggerLevel_.ToLower() == "debug")
            {
                DateTime dateNow = DateTime.Now;
                string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " ERROR - " + message);
                }
            }
        }

        public static void InfoDebugTrace(String message)
        {
            DateTime dateNow = DateTime.Now;
            string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
            if (loggerLevel_.ToLower() == "info")
            {
               
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " INFO - " + message);
                }
            }
            if (loggerLevel_.ToLower() == "trace")
            {
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " TRACE - " + message);
                }
            }
            if (loggerLevel_.ToLower() == "debug")
            {
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " DEBUG - " + message);
                }
            }
        }

        public static void DebugTrace(String message)
        {
            DateTime dateNow = DateTime.Now;
            string now = dateNow.ToString("yyyy-MMM-dd ddd HH:mm:ss");
            if (loggerLevel_.ToLower() == "trace")
            {
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " TRACE - " + message);
                }
            }
            if (loggerLevel_.ToLower() == "debug")
            {
                using (TextWriter tw = new StreamWriter(logFolder_ + logFile_, true))
                {
                    tw.WriteLine(now + " DEBUG - " + message);
                }
            }
        }

    }
}

