## Locate and Highlight Specific Text in a PDF using DLL
##### This A360 Bot will help you to locate and highlight Specific Text in a PDF using a DLL

eg :  text : "Null"

![image](https://github.com/user-attachments/assets/d8166767-3069-47b3-bdc7-dca8f74024fd)

* This solution will rely on the camel case of the input text given.




- Run the DLL function "display" using the A360 bot by providing the following inputs
  -  keyword
  -  pdffilepath
- DLL Details:
  - Namespace  : HighlightPDFTextV2
  - Class name  : Class1
  - Function : display
  - Function Input parameters :
       - keyword (eg : "sample text")
       - pdffilepath (eg : "C:/Users/sample.pdf" )
  - Dependant DLLs
       - Spire.License.dll
       - Spire.Pdf.dll
         

- After executing the function, the input PDF will be saved with highlights on the specified "search_text"
