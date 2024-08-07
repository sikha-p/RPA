﻿/*
 * Author : SIKHA P 
 * Lead - Partner Solution Desk
 * Partner Solution Desk(PSD)
 * Automation Anywhere
 */
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Mime;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Xml;
using Microsoft.Win32;

namespace Rest_Web_Services
{
   public class RestWebServiceRequest
    {
        //This method is for both GET& POST types of APIs with/without attaching certificate 
        public static string SendRequest(string domain,
            string apiUrl,
            string cookie,
            string headers,
            string method,
            string inputData,
            Boolean fileDownload,
            string outputFolder,
            string certificatePath,
            string privateKey)
        {
            Console.WriteLine("Hi");
            //***cookie**//
            //key=value;key2=value2

            //****Headers****/
            //key=value;key2=value2

            //****inputData****/
            //from bot   { "companyId":"IQ24143"}
            //from C# code   "{\"companyId\":\"IQ24143\"}",

            //cookie = cookie.Replace(" ", "");

            string[] cookies = cookie.Split(';');
            CookieContainer cookieContainer = new CookieContainer();
            if (cookie.Length != 0)
            {

                Uri target = new Uri(domain);
                foreach (string cookie_ in cookies)
                {
                    if (cookie_.Length != 0)
                    {
                        cookieContainer.Add(new Cookie(cookie_.Split('=')[0], cookie_.Split('=')[1]) { Domain = target.Host });
                    }
                }
            }

            string remoteUrl = string.Format(apiUrl);
            HttpWebRequest httpRequest = (HttpWebRequest)WebRequest.Create(remoteUrl);
            httpRequest.CookieContainer = cookieContainer;


            if (headers.Length != 0)
            {
                string[] headers_ = headers.Split(';');
                foreach (string header in headers_)
                {
                    if (header.Length != 0)
                    {
                        // Find the first index of '='
                        Int32 index = header.IndexOf('=');
                        string key = header.Split('=')[0];
                        string value = header.Substring(index + 1);
                        if (key == "Accept" || key == "accept")
                        {
                            httpRequest.Accept = header.Split('=')[1];
                        }
                        else if (key == "Content-Type")
                        {
                            httpRequest.ContentType = header.Split('=')[1];
                        }
                        else
                        {
                            httpRequest.Headers.Add(key, value);
                        }

                    }
                }
            }
            httpRequest.Method = method;
            if (method == "POST")
            {

                byte[] dataStream = Encoding.UTF8.GetBytes(inputData);
                httpRequest.ContentLength = dataStream.Length;
                Stream newStream = httpRequest.GetRequestStream();
                // Send the data.
                newStream.Write(dataStream, 0, dataStream.Length);
                newStream.Close();
            }

            try
            {
                if (certificatePath != "")
                {
                    httpRequest = AttachClientCertificate(httpRequest, certificatePath, privateKey);
                }

                if (!fileDownload)
                {
                    StreamReader sr = new StreamReader(httpRequest.GetResponse().GetResponseStream());
                    string Result = sr.ReadToEnd();
                    return Result;
                }
                else
                {
                    WebResponse response = httpRequest.GetResponse();

                    if (response.Headers.AllKeys.Contains("Content-Disposition"))
                    {
                        string contentDisposition = response.Headers["Content-Disposition"];


                        if (contentDisposition != "")
                        {
                            string[] stringSeparators = new string[] { "filename=" };
                            LogToFile(" INFO line 125:: contentDisposition " + contentDisposition);
                            var fileName = CleanFileName(contentDisposition.Split(stringSeparators, StringSplitOptions.None)[1]);
                            LogToFile(" INFO line 127: fileName after clean: " + fileName);
                            string[] stringSeparators2 = new string[] { ";" };
                            fileName = CleanFileName(fileName.Split(stringSeparators2, StringSplitOptions.None)[0]);
                            LogToFile(" INFO line 130:: fileName after clean: " + fileName);
                            //var cp = new ContentDisposition(contentDisposition);
                            //string fileName = cp.FileName;
                            using (Stream output = File.OpenWrite("" + outputFolder + "/" + fileName))
                            using (Stream input = response.GetResponseStream())
                            {
                                input.CopyTo(output);
                            }
                            //
                            return "File saved in  : " + "" + outputFolder + "/" + fileName;
                        }
                        else
                        {
                            LogToFile(" INFO : Unable to retrive file name & extension from the response ,  contentDisposition is empty");
                            return "Unable to retrive file name & extension from the response ,  contentDisposition is empty";
                        }
                    }
                    else
                    {
                        LogToFile(" INFO : There is no response header named contentDisposition");
                        return "There is no response header named contentDisposition!";
                    }

                      
                }

            }
            catch (Exception ex)
            {
                LogToFile(" ERROR line 151:: contentDisposition " + ex.ToString());
                LogToFile(" ERROR line 151:: contentDisposition " + ex.Message);
                Console.WriteLine(ex.ToString());
                return ex.ToString();
            }
        }

        private static readonly Encoding encoding = Encoding.UTF8;

        //This method is for a file upload API call
        public static string FileUploadRequest(string uri, string token, string paramsJson)
        {
            try
            {
                var dict = JsonConvert.DeserializeObject<Dictionary<string, string>>(paramsJson);
                Dictionary<string, object> postParameters = new Dictionary<string, object>();
                foreach (var data in dict)
                {
                    if (data.Key == "file")
                    {
                        string filePath = data.Value;
                        string filename = Path.GetFileName(filePath);
                        FileParameter f = new FileParameter(File.ReadAllBytes(filePath), filename, "multipart/form-data");
                        postParameters.Add("file", f);
                    }
                    else
                    {
                        postParameters.Add(data.Key, data.Value);
                    }
                }
                string response = MultipartFormDataPost(uri, postParameters, token);


                return response;
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }


        public static string MultipartFormDataPost(string uri, Dictionary<string, object> postParameters, string token)
        {
            try
            {
                string formDataBoundary = String.Format("----------{0:N}", Guid.NewGuid());
                string contentType = "multipart/form-data; boundary=" + formDataBoundary;

                byte[] formData = GetMultipartFormData(postParameters, formDataBoundary);

                return PostForm(uri, contentType, formData, token);
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
        public static string PostForm(string postUrl, string contentType, byte[] formData, string token)
        {
            HttpWebRequest request = WebRequest.Create(postUrl) as HttpWebRequest;

            if (request == null)
            {
                throw new NullReferenceException("request is not a http request");
            }

            // Set up the request properties.
            request.Method = "POST";
            request.ContentType = contentType;
            // request.Headers.Add("X-Authorization", token);
            request.Headers.Add("Authorization", token);
            request.ContentLength = formData.Length;


            // Send the form data to the request.
            using (Stream requestStream = request.GetRequestStream())
            {
                requestStream.Write(formData, 0, formData.Length);
                requestStream.Close();
            }

            StreamReader sr = new StreamReader(request.GetResponse().GetResponseStream());
            string Result = sr.ReadToEnd();
            return Result;
        }

        private static byte[] GetMultipartFormData(Dictionary<string, object> postParameters, string boundary)
        {
            Stream formDataStream = new System.IO.MemoryStream();
            bool needsCLRF = false;

            foreach (var param in postParameters)
            {
                // Thanks to feedback from commenters, add a CRLF to allow multiple parameters to be added.
                // Skip it on the first parameter, add it to subsequent parameters.
                if (needsCLRF)
                    formDataStream.Write(encoding.GetBytes("\r\n"), 0, encoding.GetByteCount("\r\n"));

                needsCLRF = true;

                if (param.Value is FileParameter)
                {
                    FileParameter fileToUpload = (FileParameter)param.Value;
                    // Add just the first part of this param, since we will write the file data directly to the Stream
                    string header = string.Format("--{0}\r\nContent-Disposition: form-data; name=\"{1}\"; filename=\"{2}\";\r\nContent-Type: {3}\r\n\r\n",
                        boundary,
                        param.Key,
                        fileToUpload.FileName ?? param.Key,
                        fileToUpload.ContentType ?? "application/octet-stream");

                    formDataStream.Write(encoding.GetBytes(header), 0, encoding.GetByteCount(header));

                    // Write the file data directly to the Stream, rather than serializing it to a string.
                    formDataStream.Write(fileToUpload.File, 0, fileToUpload.File.Length);
                }
                else
                {
                    string postData = string.Format("--{0}\r\nContent-Disposition: form-data; name=\"{1}\"\r\n\r\n{2}",
                        boundary,
                        param.Key,
                        param.Value);
                    formDataStream.Write(encoding.GetBytes(postData), 0, encoding.GetByteCount(postData));
                }
            }

            // Add the end of the request.  Start with a newline
            string footer = "\r\n--" + boundary + "--\r\n";
            formDataStream.Write(encoding.GetBytes(footer), 0, encoding.GetByteCount(footer));

            // Dump the Stream into a byte[]
            formDataStream.Position = 0;
            byte[] formData = new byte[formDataStream.Length];
            formDataStream.Read(formData, 0, formData.Length);
            formDataStream.Close();

            return formData;
        }


        public class FileParameter
        {
            public byte[] File { get; set; }
            public string FileName { get; set; }
            public string ContentType { get; set; }
            public FileParameter(byte[] file) : this(file, null) { }
            public FileParameter(byte[] file, string filename) : this(file, filename, null) { }
            public FileParameter(byte[] file, string filename, string contenttype)
            {
                File = file;
                FileName = filename;
                ContentType = contenttype;
            }

        }
        public class param
        {
            public string file { get; set; }
            public string overwriteOption { get; set; }

            public string productionVersionOption { get; set; }

            public string password { get; set; }
        }


        public static HttpWebRequest AttachClientCertificate(HttpWebRequest request, string certPath, string privateKey)
        {
            //creating cert
            X509Certificate2Collection certificates = new X509Certificate2Collection();
            certificates.Import(certPath, privateKey, System.Security.Cryptography.X509Certificates.X509KeyStorageFlags.DefaultKeySet);

            request.AllowAutoRedirect = true;
            request.ClientCertificates = certificates;

            return request;
        }
          private static string CleanFileName(string fileName)
    {
          
            return Path.GetInvalidFileNameChars().Aggregate(fileName, (current, c) => current.Replace(c.ToString(), string.Empty));
    }

        private static void LogToFile(string line)
        {
            string logFile = "Rest_Web_service.log";
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

        private static string getLogFolderPath()
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

  


