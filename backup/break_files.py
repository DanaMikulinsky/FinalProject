import os

# Define the merged file path
merged_file = './merged_file.txt'
# Define the output directory for split files
output_dir = './split_files'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the merged file
with open(merged_file, 'r', encoding='utf-8') as infile:
    content = infile.read()

# Split the content by the separator
sections = content.split('#' * 20)

# Write each section to a separate file
for i, section in enumerate(sections):
    if section.strip():  # Skip empty sections
        output_path = os.path.join(output_dir, f'file{i+1}.txt')
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(section.strip())

print(f"Split {len(sections)} files into {output_dir} successfully!")
