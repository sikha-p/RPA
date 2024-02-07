#Author:Prasad Katankot, Partner Solution Desk
#Feb-07-2024
import pandas as pd
import Levenshtein


# Predefined full column titles
#pick it from config or global variables etc
predefined_titles = [
    "Invoice Number",
    "invoice date",
    "Vendor Name",
    "Vendor Addr",
    "Quantity",
    # Add more predefined titles as needed
]
min_distance = 4  # define the threshold here explicitly
closest_title_attributes =[]
# Function to find the closest matching title
def find_closest_title(column_title):
    closest_title = None
    for predefined_title in predefined_titles:
        distance = Levenshtein.distance(column_title.lower(), predefined_title.lower())
        if distance < min_distance:
            #min_distance = distance
            closest_title_attributes.append({"predefined_title":predefined_title, "column_title":column_title,  "distance":distance})
        # else:
        #     # if required add code here to handle the threshold exception
        #     #print("distance is more than the defined threshold")
        #     print(distance,column_title.lower(), predefined_title.lower() )
        #     closest_title= "distance_breached"
    return closest_title_attributes

# Read Excel file
excel_file_path = "Invoice.xlsx"  # Update with your Excel file path
df = pd.read_excel(excel_file_path)

# Match column titles
matched_titles = [find_closest_title(title) for title in df.columns]

all_cols_matched=True
#for closest_title_attribute in matched_titles:
for predefined_title in predefined_titles:
    res=list(filter(lambda sub: sub["predefined_title"] == predefined_title, closest_title_attributes))
    if len(res) <= 0:
        all_cols_matched = False
        print("Columns mismatch for", predefined_title) # add to custom log
        #break
    #if distance < min_distance:
    #if title == "distance_breached":
    # if closest_title_attribute[2] > min_distance:
    #     #add more logic to integrate with the bot to skip this file.Maybe you should capture the file name in a seperate log
    #     print("breached, distance-", closest_title_attribute[2] , closest_title_attribute[0],  closest_title_attribute[1])
    #     exit()
    # else:
    #     # Replace column titles with matched titles
    #     df.columns = matched_titles
        # Save DataFrame with updated column titles back to Excel file
if all_cols_matched:
    output_excel_file_path = "output_excel_file.xlsx"  # Update with desired output file path
    df.to_excel(output_excel_file_path, index=False)
else:
    print("one of the columns mismatch") #add to custom logs if reqd

# Display DataFrame with updated column titles
#print(df.head())


