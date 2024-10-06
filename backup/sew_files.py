import os

# Define the directory containing the .txt files
directory_path = './all files 19_2'
# Define the output file
output_file = 'merged_file.txt'
def read_file_with_fallback(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try a fallback encoding (latin-1 or ISO-8859-8)
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()

# Function to check if a file is a text file
def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()  # Try reading the file
        return True
    except (UnicodeDecodeError, OSError):
        return False

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Iterate over all .txt files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            # Check if the file is a valid text file
            if is_text_file(file_path):
                # Read the content of the current file with fallback encoding
                content = read_file_with_fallback(file_path)
                # Write the content to the output file
                outfile.write(content)
                # Add a separator after the content
                outfile.write('\n' + '#' * 20 + '\n')
            else:
                print(f"Skipping non-text file: {filename}")

print("Files merged successfully!")