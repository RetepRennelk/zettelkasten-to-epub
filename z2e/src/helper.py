import re
import os
import shutil

def dunderfy(s):
    return s.replace("_", "__").replace(" ","_")

def get_all_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        #for file in files:
        #    file_list.append(os.path.join(root, file))
        file_list += files
    return file_list

def readlines(filename):
    with open(filename) as f:
        file_content = f.read().rstrip("\n")
    return file_content.split("\n")

def writestr(s, target_path):
    with open(target_path, "w") as f:
        f.write(s)

def write(source_path, target_path):
    shutil.copy2(source_path, target_path)