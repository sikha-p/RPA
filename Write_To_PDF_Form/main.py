# Author: Prasad Katankot
# Global Solution Desk (GSD)
# Version:1.0
# Oct-10-2024

import traceback
from pypdf import PdfReader
from PyPDFForm import PdfWrapper

def fill_pdf_form(dict_args):

    try:
        input_pdf=dict_args['input_pdf']
        output_pdf=dict_args['output_pdf']
        field_values=dict_args['field_values']
        reader = PdfReader(input_pdf)
        for page in reader.pages:
            # Check if there are annotations (form fields) in the page
            if "/Annots" in page:
                for annotation in page["/Annots"]:
                    field = annotation.get_object()
                    field_name = field.get("/T")  # Get the field name
                    field_value = field.get("/V")  # Get the field name
                    if field_value in field_values:
                        field_values[field_name] = field_values.pop(field_value)
                        #print(field_name, field_value)
        #print(field_values)
        filled = PdfWrapper(input_pdf).fill(
            field_values
        )

        with open(output_pdf, "wb+") as output:
            output.write(filled.read())
    except Exception as innerException:
        # Get the current line number where the exception occurred
        line_number = traceback.extract_tb(innerException.__traceback__)[-1].lineno
        # Get the error message
        error_message = str(innerException)
        return "Python Error:Encountered in function- fill_pdf_form, line number:"+ str(line_number)+' with error message:'+error_message


if __name__ == '__main__':
    # Example usage
    input_pdf = "ExternalFiles\A-6551-RS.pdf"
    output_pdf = "ExternalFiles\sample_template_op.pdf"
    field_values ={
            "<D16>": "prasad",
            "<D23>": "Katankot",
            #"check_2": False, For Checkbox

        }

    dict_arg = {'input_pdf':input_pdf,
    'output_pdf':output_pdf,
    'field_values':field_values}
    print(dict_arg)
    fill_pdf_form(dict_arg)

