from PIL import Image
import os

def split_image_vertically(input_path, output_directory):

    os.makedirs(output_directory, exist_ok=True)
    original_image = Image.open(input_path)

    width, height = original_image.size

    midpoint = width // 2

    left_half = original_image.crop((0, 0, midpoint, height))
    right_half = original_image.crop((midpoint, 0, width, height))

    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    left_output_path = os.path.join(output_dir, f"{base_filename}_left_half.png")
    right_output_path = os.path.join(output_dir, f"{base_filename}_right_half.png")

    left_half.save(left_output_path)
    right_half.save(right_output_path)


input_image_path = r"input_path"
output_dir = r"output_folder"

split_image_vertically(input_image_path, output_dir)

