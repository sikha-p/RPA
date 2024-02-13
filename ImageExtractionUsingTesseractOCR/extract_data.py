import pytesseract
import json
from PIL import Image

#This code is used to extract name and designation from a particular document
def extract_fields_from_image(image_path):
    image = Image.open(image_path)

    pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract.exe'

    # Perform OCR to get the raw text
    raw_text = pytesseract.image_to_string(image)

    # Extract fields using regular expressions
    import re

    # Define patterns for "for," "name," and "designation"
    name_pattern = re.compile(r'Name:\s*(.*)', re.IGNORECASE)
    designation_pattern = re.compile(r'Designation:\s*(.*)', re.IGNORECASE)

    name_field = None
    designation_field = None

    for match in name_pattern.finditer(raw_text):
        name_field = match.group(1).strip()

    for match in designation_pattern.finditer(raw_text):
        designation_field = match.group(1).strip()

    # Create a dictionary with the extracted fields
    extracted_data = {
        'name': name_field,
        'designation': designation_field
    }

    # Save the extracted data to a JSON file
    output_file = r'output_json.json'
    with open(output_file, 'w') as file:
        json.dump(extracted_data, file, indent=4)

    print(f"Extracted data saved to: {output_file}")


extract_fields_from_image(r"input_img")



