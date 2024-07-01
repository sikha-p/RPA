using System;
using MimeKit;
using TheArtOfDev.HtmlRenderer.PdfSharp;
using PdfSharp.Pdf;
using PdfSharp;

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

                // Extract email metadata
                string subject = message.Subject ?? "No Subject";
                string from = message.From.ToString();
                string to = message.To.ToString();
                string cc = message.Cc.ToString();
                string bcc = message.Bcc.ToString();
                string date = message.Date.ToString("f");
                string body = message.HtmlBody ?? message.TextBody ?? "No Body";

                // Extract the HTML body from the email
                // var body = message.HtmlBody ?? message.TextBody;
                // Create HTML content with metadata and body
                string html = $@"
            <html>
                <body>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p><strong>From:</strong> {from}</p>
                    <p><strong>To:</strong> {to}</p>
                    <p><strong>CC:</strong> {cc}</p>
                    <p><strong>BCC:</strong> {bcc}</p>
                    <p><strong>Date:</strong> {date}</p>
                    <hr />
                    {body}
                </body>
            </html>";

                if (html != null)
                {
                    // Create a new PDF document
                    PdfDocument pdf = new PdfDocument();

                    // Render the HTML to the PDF
                    pdf = PdfGenerator.GeneratePdf(html, PageSize.A4);
                    // Save the PDF document to a file
                    pdf.Save(pdfFilePath);

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
