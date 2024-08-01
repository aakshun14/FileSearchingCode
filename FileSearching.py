import os
import subprocess

def find_files_and_folders(name, root_directory='C:\\'):
    result = []
    for root, dirs, files in os.walk(root_directory):  # Starting from the C drive
        # Check for files with the matching name (without extension)
        for file in files:
            if os.path.splitext(file)[0] == name:
                result.append(os.path.join(root, file))
        # Check for directories with the matching name
        for dir in dirs:
            if dir == name:
                result.append(os.path.join(root, dir))
    return result

# Function to open the file or folder with the default application
def open_file_or_folder(path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(path)
        elif os.uname().sysname == 'Darwin':  # For macOS
            subprocess.call(['open', path])
        else:  # For Linux
            subprocess.call(['xdg-open', path])
        print(f"Opened: {path}")
    except Exception as e:
        print(f"Error opening {path}: {e}")

# Example usage
name = str(input("Enter any file name : "))  # Name without extension for files or just the directory name
paths = find_files_and_folders(name)
print(paths)

for path in paths:
    print(f"Found: {path}")
    open_file_or_folder(path)
