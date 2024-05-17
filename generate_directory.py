# Description: Generates a directory/table of contents recursively from the file directories
import os

home = os.path.expanduser("~")
print(home)
print("done")

def file_exists(file_path):
    try:
        open(file_path, 'r')
    except Exception:
        return 0
    return 1

def contains_any_string(string, substrings):
    return any(substring in string for substring in substrings)

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
    print(f"Top Directory Path: {target_folder_path}")
    f2 = open(main_dir_h_path, 'r')
    
    # Directories to ignore
    ignore_dirs = ['.git', 'img-src']
    # Filename patterns to ignore
    ignore_file_patterns = ['dir.md', 'readme.md']
    
    # List of return URL's
    ret_url = '../index.html'
    
    for root, dir_names, file_names in os.walk(target_folder_path):
        if any(ignore_dir in root for ignore_dir in ignore_dirs):
            continue
    
        # Open a new index for current working directory (cwd)
        root_base = os.path.basename(root)
        new_index_path = os.path.join(root, 'dir.md')
        new_index = open(new_index_path, 'w')
        
        f2.seek(0)
        yaml_header = f2.read()
        yaml_header = yaml_header.replace ("[replace]", root_base)
        yaml_header = yaml_header.replace ("[ret-url]", ret_url)
        new_index.write(yaml_header)
        ret_url = '../dir.html'
        
        if (len (dir_names) > 1):
            new_index.write("\n# Subdirectories\n")
            # Add its children
            for dir_base in dir_names:
                dir_path = os.path.join(root, dir_base)
                readme_path = os.path.join(dir_path, 'readme.md')
                if file_exists(readme_path):
                    print(f'Subdirectory Path: {dir_path}')
                    s = f'- [{dir_base}]({dir_base}/dir.html):'
                    new_index.write (s)

                    readme = open(readme_path, 'r')
                    s = f' {readme.read()}\n'
                    new_index.write (s)
                    readme.close()
                else:
                    # Ignore this directory if it does not have a readme
                    ignore_dirs.append(dir_base)
        
        if (len (file_names) > 1):
            wrote = False;
            for entry in file_names:
                if not contains_any_string(entry, ignore_file_patterns):
                    if (not wrote):
                        new_index.write("\n# Files\n");
                        wrote = True
                    
                    filename_without_ext, _ = os.path.splitext(entry)
                    s = f'- [{filename_without_ext}]({filename_without_ext}.html)\n'
                    new_index.write(s)
                    
        
        # print(f"The basename path is: {root_base}")
        # print(f"The root is {root}")
        # print(f"The directory name is: {dir_names}")
        # print(f"The file names are: {file_names}")
        # print("*" * 10)
    
    exit()

if __name__ == "__main__":
    main()