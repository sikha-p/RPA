//*************************************//
//**** AUTHOR: Sikha Poyyil
//**** Global Solution Desk(GSD)
//**** Automation Anywhere
//*************************************//

using Spire.Pdf;
using Spire.Pdf.General.Find;
using System;
using System.Diagnostics;

namespace HighlightPDFTextV2
{
    public class Class1
    {
        public int count = 0;

        [Obsolete]
        public string display(string keyword, string pdffilepath)
        {
            try
            {
                PdfDocument pdfDocument = new PdfDocument();
                pdfDocument.LoadFromFile(pdffilepath);
                foreach (PdfPageBase page in pdfDocument.Pages)
                {
                    foreach (PdfTextFind find in page.FindText(keyword, TextFindParameter.CrossLine).Finds)
                    {
                        int length = keyword.Length;
                        ++this.count;
                        find.ApplyHighLight();
                        Console.WriteLine(this.count.ToString() + keyword);
                    }
                }
                pdfDocument.SaveToFile(pdffilepath, FileFormat.PDF);
                return "Modified PDF saved to " + pdffilepath;
            }
            catch(Exception ex)
            {
                return "ERROR: "+ex.Message;
            }
            
        }
    }   
}