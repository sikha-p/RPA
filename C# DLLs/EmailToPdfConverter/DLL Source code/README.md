# Email To Pdf Converter

#### This can be used to convert the ".eml" file to ".pdf"
This DLL can convert .eml files, including their CSS styles, to PDF

Main DLL - EmailToPdfConverter.dll

Dependant DLLs :
* HtmlRenderer.PdfSharp.dll
* MailKit.dll
* HtmlRenderer.dll
* MimeKit.dll
* PdfSharp.dll



#### Important Note:  
You can configure the Pdf pagesize, Margins etc. But please be careful if you modify the below configuration. Increasing the margin value may cause content to be hidden in the email. If you notice any missing content in the PDF, reduce the margin value and convert the document again.

```C#
                //Page is in Landscape mode, other option is Portrait
                configurationOptions.PageOrientation = PdfSharp.PageOrientation.Portrait;

                //Set page type as Letter. Other options are A4 ...
                configurationOptions.PageSize = PdfSharp.PageSize.Letter;

                //This is to fit Chrome Auto Margins when printing.Yours may be different
                configurationOptions.MarginBottom = 19;
                configurationOptions.MarginLeft = 20;
                configurationOptions.MarginTop = 10;
                
