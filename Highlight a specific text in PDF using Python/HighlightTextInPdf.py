import fitz  # PyMuPDF


def highlight_text_in_pdf(args):
    pdf_path = args[0]
    search_text = args[1]
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]

        # Search for the text on the page
        text_instances = page.search_for(search_text)

        # Highlight each instance found
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    # Save the modified PDF back to the same file
    pdf_document.saveIncr()
    pdf_document.close()
