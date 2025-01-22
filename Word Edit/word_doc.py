from docx import Document

# Load the Word document
file_path = r"path-to-word"  # Replace with your file path
doc = Document(file_path)

# Iterate through all tables in the document
for table_index, table in enumerate(doc.tables):
    for row_index, row in enumerate(table.rows):
        for col_index, cell in enumerate(row.cells):
            # Check if "Harry" is in the cell text
            if "Harry" in cell.text:
                print(f"Found 'Harry' in Table {table_index + 1}, Row {row_index + 1}, Column {col_index + 1}")

                # Copy the value to column [2][2] in the same table (1-based indexing)
                try:
                    table.rows[row_index].cells[col_index+1].text = cell.text
                    print(f"Value '{cell.text}' copied to Table {table_index + 1}, Row 3, Column 3.")
                except IndexError:
                    print(f"Table {table_index + 1} does not have a Row 3 or Column 3.")

# Save the updated document
updated_file_path = r"path-to-output-word"
doc.save(updated_file_path)
print(f"Updated file saved as {updated_file_path}")
