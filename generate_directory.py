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



def parse_file_name (file_path):
    # Parses the title from the markdown file at the file path 'file_path'
    title = '0'
    
    with open (file_path, 'r') as file: 
        first_line = file.readline().strip() # should be "---"
        second_line = file.readline().strip() # Should contain title

        d, title = second_line.split ("title:", 1)
        title = title.strip()
    return title.replace('"', '')

def parse_text_file(file_path):
    data = {}
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    current_field = None
    current_value = []
    
    for line in lines:
        
        line = line.strip()
        if ':' in line:
            if current_field:
                data[current_field] = current_value
            current_field, current_value = line.split(':', 1)
            current_field = current_field.strip()
            # current_value = [current_value.strip()]
        else:
            current_value = current_value + line.replace("\n", "")
    
    if current_field:
        data[current_field] = current_value
    
    return data

def write_my_description (root, new_index):
    # Writes the `long description` in the readme file located in this directory 
    
    # Get cwd readme path and parse it
    read_me_path = os.path.join (root, 'readme.md');
    data = parse_text_file (read_me_path)
    
    long_description = '';
    try:
        long_description = data['Description-Long']
    except KeyError:
        print("Error: Target directory does not have a readme")
    
    new_index.write (long_description)
    new_index.write("\n")

def generate_directory_index(root, dir_names, file_names, ignore_dirs, ignore_file_patterns, ret_url):
    # Generate the directory index for a given directory
    root_base = os.path.basename(root)
    new_index_path = os.path.join(root, 'dir.md')
    
    with open(new_index_path, 'w') as new_index, open(main_dir_h_path, 'r') as f2:
        # Write the YAML header to the directory index file
        read_me_path = os.path.join (root, 'readme.md');
        data = parse_text_file (read_me_path)
        
        yaml_header = f2.read()
        yaml_header = yaml_header.replace("[replace]", data['Title'])
        yaml_header = yaml_header.replace("[ret-url]", ret_url)
        new_index.write(yaml_header)
        
        
        write_my_description (root, new_index)

        if len(dir_names) > 1:
            # Write the subdirectories section to the directory index file
            new_index.write("\n# Subdirectories\n")
            dir_names.sort()
            
            for dir_base in dir_names:
                dir_path = os.path.join(root, dir_base)
                readme_path = os.path.join(dir_path, 'readme.md')
                if file_exists(readme_path):
                    print(f'Subdirectory Path: {dir_path}')
                    with open(readme_path, 'r') as readme:
                        print(readme_path)
                        data = parse_text_file(readme_path)
                        print (f'dir_base:{dir_base}')
                        title = dir_base;
                        description = readme.read();
                        try: 
                            title = data['Title']
                            description = data['Description']
                        except KeyError:
                            print("Error: Target directory does not have a readme")
                        # include = data['Include']

                        # print(f"Title: {title}")
                        # print(f"Description: {description}")
                        # print(f"Include:\n{include}")
                        # print ("FINISH\n\n")
                        s = f'- [{title}]({dir_base}/dir.html): {description}\n'
                        new_index.write(s)
                else:
                    ignore_dirs.append(dir_base)
        
        if len(file_names) > 1:
            # Write the files section to the directory index file
            wrote = False
            file_names.sort()
            for entry in file_names:
                if not contains_any_string(entry, ignore_file_patterns):
                    if not wrote:
                        new_index.write("\n# Files\n")
                        wrote = True
                    filename_without_ext, _ = os.path.splitext(entry)
                    
                    title =  parse_file_name (os.path.join (root, entry));
                    
                    s = f'- [{title}]({filename_without_ext}.html)\n'
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