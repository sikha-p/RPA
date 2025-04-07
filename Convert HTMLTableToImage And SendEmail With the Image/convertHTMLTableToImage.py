import imgkit
import os

def convert_html_to_image(args):
    # Save the HTML string to a temporary HTML file
    html_string = args[0]
    output_folder= args[1]
    output_image_path =  os.path.join(output_folder, "temp.jpg")
    html_file_path = os.path.join(output_folder, "temp_table.html")
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_string)
    options = {
        'format': 'jpg',
        'quality': '100',
        'zoom': '2',         # Makes image larger/sharper
        'width': '1000',     # Control overall width
        'disable-smart-width': ''  # Prevent auto-shrinking
    }
    # Convert the HTML file to an image
    imgkit.from_file(html_file_path, output_image_path, options=options)
    return f"Image saved as {output_image_path}"
