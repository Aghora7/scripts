import os
import datetime
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script.py <vendor_folder_path>")
    sys.exit(1)

# Set the path to your "vendor" folder
vendor_folder = sys.argv[1]

# Get user input for brand and model names
brand_name = input("Enter the brand name: ")
model_name = input("Enter the model name: ")

# Create a list to store file names and locations
file_list = []

# Traverse through the files in the "vendor" folder
for root, dirs, files in os.walk(vendor_folder):
    for file in files:
        # Get the full path of each file
        file_path = os.path.join(root, file)

        # Replace the specified text in the file path
        file_path = file_path.replace('/home/aghora7/DumprX/out/', 'vendor/{}/{}/proprietary/'.format(brand_name, model_name))

        # Append the modified file path to the list
        file_list.append(file_path)

# Specify the name of the text file to store the information
output_file = '{}-{}.mk'.format(model_name, brand_name)

# Write the modified file paths to the text file with "PRODUCT_COPY_FILES +="
with open(output_file, 'w') as file:
    # Copyright notice
    file.write('# Thank you for using it\n')
    file.write('#\n')
    file.write('# Copyright (c) {}. All rights reserved.\n'.format(datetime.datetime.now().year))

    # Add a single space
    file.write('\n')

    # Add the additional line without a space after the backslash and remove trailing slash
    file.write('PRODUCT_SOONG_NAMESPACES += \\\n    vendor/{}/{}\n'.format(brand_name, model_name))

    # Add a single space
    file.write('\n')

    # Product copy files notice
    file.write('PRODUCT_COPY_FILES += \\\n')

    # Write the modified file paths
    for file_path in file_list:
        target_folder = '$(TARGET_COPY_OUT_ODM)' if 'odm' in file_path else '$(TARGET_COPY_OUT_VENDOR)'
        
        # Calculate the relative path properly
        relative_path = os.path.relpath(file_path, os.path.join(vendor_folder, 'vendor', brand_name, model_name, 'proprietary'))
        target_path = os.path.join(target_folder, relative_path)

        # Replace "$(TARGET_COPY_OUT_ODM)/vendor/odm" with "$(TARGET_COPY_OUT_ODM)/"
        target_path = target_path.replace('$(TARGET_COPY_OUT_ODM)/vendor/odm', '$(TARGET_COPY_OUT_ODM)')

        # Replace "$(TARGET_COPY_OUT_VENDOR)/vendor/" with "$(TARGET_COPY_OUT_VENDOR)/"
        target_path = target_path.replace('$(TARGET_COPY_OUT_VENDOR)/vendor/', '$(TARGET_COPY_OUT_VENDOR)/')

        file.write('    {}:{} \\\n'.format(file_path, target_path))

print(f"Modified file paths have been saved to {output_file}")
