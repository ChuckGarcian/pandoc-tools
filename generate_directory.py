# Description: Generates a directory/table of contents recursively from the file directories
import os

def file_exists(file_path):
    # Check if a file exists
    try:
        open(file_path, 'r')
        return True
    except FileNotFoundError:
        return False

def contains_any_string(string, substrings):
    # Check if a string contains any of the given substrings
    return any(substring in string for substring in substrings)

def generate_directory_index(root, dir_names, file_names, ignore_dirs, ignore_file_patterns, ret_url):
    # Generate the directory index for a given directory
    root_base = os.path.basename(root)
    new_index_path = os.path.join(root, 'dir.md')
    
    with open(new_index_path, 'w') as new_index, open(main_dir_h_path, 'r') as f2:
        # Write the YAML header to the directory index file
        yaml_header = f2.read()
        yaml_header = yaml_header.replace("[replace]", root_base)
        yaml_header = yaml_header.replace("[ret-url]", ret_url)
        new_index.write(yaml_header)
        
        if len(dir_names) > 1:
            # Write the subdirectories section to the directory index file
            new_index.write("\n# Subdirectories\n")
            for dir_base in dir_names:
                dir_path = os.path.join(root, dir_base)
                readme_path = os.path.join(dir_path, 'readme.md')
                if file_exists(readme_path):
                    print(f'Subdirectory Path: {dir_path}')
                    with open(readme_path, 'r') as readme:
                        s = f'- [{dir_base}]({dir_base}/dir.html): {readme.read()}\n'
                        new_index.write(s)
                else:
                    ignore_dirs.append(dir_base)
        
        if len(file_names) > 1:
            # Write the files section to the directory index file
            wrote = False
            for entry in file_names:
                if not contains_any_string(entry, ignore_file_patterns):
                    if not wrote:
                        new_index.write("\n# Files\n")
                        wrote = True
                    filename_without_ext, _ = os.path.splitext(entry)
                    s = f'- [{filename_without_ext}]({filename_without_ext}.html)\n'
                    new_index.write(s)
    
    return '../dir.html'

current_path = os.getcwd()
target_dir = "ut-website-md/Writings"
parent_folder_path = os.path.dirname(current_path)
target_folder_path = os.path.join(parent_folder_path, target_dir)
includes_path = os.path.join(current_path, "includes")

main_dir_md = "main-dir.md"
main_dir_h = "main-dir-h.md"
main_dir_path = os.path.join(target_folder_path, main_dir_md)
main_dir_h_path = os.path.join(includes_path, main_dir_h)

def main():
    # Main function to generate the directory index recursively
    home = os.path.expanduser("~")
    print(home)
    print("done")
    print(f"Top Directory Path: {target_folder_path}")
    
    ignore_dirs = ['.git', 'img-src']
    ignore_file_patterns = ['dir.md', 'readme.md']
    
    ret_url = '../index.html'
    
    for root, dir_names, file_names in os.walk(target_folder_path):
        # Skip directories that should be ignored
        if any(ignore_dir in root for ignore_dir in ignore_dirs):
            continue
        
        # Generate the directory index for the current directory
        ret_url = generate_directory_index(root, dir_names, file_names, ignore_dirs, ignore_file_patterns, ret_url)

if __name__ == "__main__":
    main()