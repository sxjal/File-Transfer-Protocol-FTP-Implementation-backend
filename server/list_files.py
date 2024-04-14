import os
from def_variables import directory

def list_files_in_directory():
    files_dict = {}
    print (directory)
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files_dict[filename] = os.path.join(directory, filename)
    print (files_dict)

list_files_in_directory()