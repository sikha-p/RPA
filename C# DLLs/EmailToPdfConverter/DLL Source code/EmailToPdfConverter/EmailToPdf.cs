//**********************************//
// AUTHOR : Sikha Poyyil
//          Global Solution Desk
//          Automation Anywhere
//**********************************//
using System;
using MimeKit;
using TheArtOfDev.HtmlRenderer.PdfSharp;
using PdfSharp.Pdf;
using PdfSharp;
using System.Linq;
using System.Text;
using System.IO;

namespace EmailToPdfConverter
{
    public class EmailToPdf
    {
        public string convertToPdf(string emlFilePath,string pdfFilePath)
        {
            try
            {
                // Load the .eml file
                var message = MimeMessage.Load(emlFilePath);

               
                //// Extract email metadata
                string subject = message.Subject ?? "No Subject";
                string fromAddresses = message.From.ToString();
                fromAddresses = fromAddresses.Replace("<", string.Empty);
                fromAddresses = fromAddresses.Replace(">", string.Empty);

                string toAddresses = message.To.ToString();
                toAddresses = toAddresses.Replace("<", string.Empty);
                toAddresses = toAddresses.Replace(">", string.Empty);
                string Sent = message.Date.ToString("f");
                //var body = message.HtmlBody ?? message.TextBody ?? "No Body";
                var body = "";
                if (message.HtmlBody == null)
                {
                    body = message.TextBody;
                    body = $"<pre>{body}</pre>";
                    body = body.Replace("\t", "\u00A0\u00A0\u00A0\u00A0"); // Replace tab with 4 non-breaking spaces
                    body = body.Replace(" ", "\u00A0"); // Non-breaking space
                    body = body.Replace("\n", "<br>");
                }
                else if (message.HtmlBody != null)
                {
                    body = message.HtmlBody;
                }
                else
                {
                    body = "No Body";
                }




                // Create HTML content with metadata and body
                string html = $@"
            <html>
                <body>
                    <p><strong>From:</strong> {fromAddresses}</p>
                    <p><strong>Sent:</strong> {Sent}</p>
                    <p><strong>To:</strong> {toAddresses}</p>
                    <p><strong>Subject:</strong> {subject}</p>
                   
                 <br />
                 {body}
                </body>
            </html>";
                if (html != null)
                {
                    StringBuilder HTMLContent = new StringBuilder(html);

                // Process each body part
                foreach (var bodyPart in message.BodyParts)
                {
                    if (bodyPart is MimePart mimePart && mimePart.ContentId != null)
                    {
                        using (var stream = new MemoryStream())
                        {
                            mimePart.Content.DecodeTo(stream);
                            var base64Image = Convert.ToBase64String(stream.ToArray());
                            var imageSrc = $"data:{mimePart.ContentType.MimeType};base64,{base64Image}";

                            // Replace cid references with base64 image data
                            HTMLContent.Replace($"cid:{mimePart.ContentId}", imageSrc);
                        }
                    }
                }


                // Process each image attachment
                foreach (var attachment in message.Attachments)
                {
                    if (attachment is MimePart mimePart && mimePart.ContentId != null)
                    {
                        using (var stream = new MemoryStream())
                        {
                            mimePart.Content.DecodeTo(stream);
                            var base64Image = Convert.ToBase64String(stream.ToArray());
                            var imageSrc = $"data:{mimePart.ContentType.MimeType};base64,{base64Image}";

                            // Replace cid references with base64 image data
                            HTMLContent.Replace($"cid:{mimePart.ContentId}", imageSrc);
                        }
                    }
                }
                //Configure page settings
                var configurationOptions = new PdfGenerateConfig();

                //Page is in Landscape mode, other option is Portrait
                configurationOptions.PageOrientation = PdfSharp.PageOrientation.Landscape;

                //Set page type as Letter. Other options are A4 ...
                configurationOptions.PageSize = PdfSharp.PageSize.A4;

                //This is to fit Chrome Auto Margins when printing.Yours may be different
                configurationOptions.MarginBottom = 19;
                configurationOptions.MarginLeft = 20;
                configurationOptions.MarginTop = 10;
                //******IMPORTANT NOTE: **** // Increasing the margin value may cause content to be hidden in the email.
                //If you notice any missing content in the PDF, reduce the margin value and convert the document again.

                //The actual PDF generation
                var PdfPage = PdfGenerator.GeneratePdf(HTMLContent.ToString(), configurationOptions);
                PdfPage.Save(pdfFilePath);
                    return "PDF saved successfully at " + pdfFilePath;
                }
                else
                {
                    return "No body content found in the email.";
                }

            }
            catch(Exception ex)
            {
                return "ERROR:  Exception Type: " + ex.GetType() +",  Exception Message: " + ex.Message + "    Stack Trace: " + ex.StackTrace ;
            }
        }
    }
}
