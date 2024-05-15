from pytube import YouTube
import shutil
import os
import json
import pandas as pd
import inputvalidation as iv

# For Duplicate File Names
def samefilename(directory, basename, extension):

    basename = samebasename(directory, basename, extension)

    newfilepath = os.path.join(directory, basename + extension)
    return newfilepath

def samebasename(directory, basename, extension):
    if os.path.isfile(directory + basename + extension):
        overwritefile = iv.yesno(input("The file with the same name is already existed! Do you want to overwrite it? (y/n) => "))

        if overwritefile != 'y':
            count = 0
            while os.path.isfile(directory + basename + extension):
                count += 1
                basename = basename[:-1] if count > 1 else basename
                basename += str(count)
    return basename

# Put files in a directory into a list of dictionaries
def get_files_in_directory(directory):
    files_info = []
    for idx, f in enumerate(os.listdir(directory)):
        if os.path.isfile(os.path.join(directory, f)):
            size = os.path.getsize(os.path.join(directory, f))
            basename, ext = os.path.splitext(f)

            size = size // 1024
            ext = ext.replace('.', '', 1).upper()

            files_info.append({'No.': idx + 1,'FileName': basename, 'FileType': ext, 'FileSize(KB)': size})
    return files_info

# Write the list into a json file
def jsonfile(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent = 4)

# Read the json file and output as a list back
def readjsonfile():
    with open('filerecord.json', 'r') as f:
        data = json.load(f)
    return data

# update the list and jsonfile, then make a dataframe and create a csv file
def list_json_csv(directory):
    file_record = get_files_in_directory(directory)
    jsonfile(file_record, 'filerecord.json')
    df = pd.read_json('filerecord.json')
    df.to_csv('filerecord.csv', index=False)

# YouTube Download Function
def download_video(url, path, new_name):
    try:    
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video
        stream.download(output_path=path)
        # Get the default name of the downloaded video
        default_filename = stream.default_filename

        # Create the full path of the downloaded video
        old_file_path = os.path.join(path, default_filename)

        # Create the full path of the new file
        new_file_path = os.path.join(path, new_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)

        print("Added successfully!")
    except:
        print("An error occurred while downloading the video!\nYou may retry it.")
        print("!YouTube has certain restrictions for downloading videos!\nYouTube's terms of service do not allow unauthorized downloading.\nSometimes, you won't be able to download.\nAlso make sure the link is correct and available to public!")

def addvideo():
    directory = "./videos/"
    print("1. Add from your local directory\n2. Add from YouTube: https://www.youtube.com/ \n3. Exit")
    addoption = iv.in_vali(3, input("Enter your choice (1-3) => "))
    if addoption != 3:
        if addoption == 1:
            # adding an existed file from a directory
            sourcefile = input("Enter the file path (no quotes) => ")
            if os.path.isfile(sourcefile):
            
                source_dir, filename = os.path.split(sourcefile)
                basename, extension = os.path.splitext(filename)

                rename = iv.yesno(input("Do you want to rename the file? (y/n) => "))
                if rename == "y":
                    basename = input("Enter the new file name (exclude file extension) => ")
                    while ('.' in basename) or (basename == '') or (basename == ' '):
                        print('Invalid Name!')
                        basename = input("Enter the new file name (exclude file extension) => ")
                    directory = samefilename(directory, basename, extension)
                else:
                    directory = samefilename(directory, basename, extension)
                # copy the source file
                shutil.copy(sourcefile, directory)
                print("Added successfully!")
            else:
                print("The specified file path doesn't exist!\nMake sure the file path is correct and the file is existed.")

        if addoption == 2:
            # adding from YouTube using pytube library
            download_video(input("Enter the link of the YouTube video => "), directory, samebasename(directory, input("Enter to rename the video (exclude file extension) => "), ".mp4") + ".mp4")
    # update the json file and csv file
    list_json_csv('./videos/')

def viewrecord():
    # update the json file and csv file
    list_json_csv("./videos/")
    print("1. View as a list\n2. View as a table\n3. Exit")
    viewoption = iv.in_vali(3, input("Enter your choice (1-3) => "))
    if viewoption == 1:
        # output lists line by line
        for lists in readjsonfile():
            print(lists)
        print("Done!!")
    if viewoption == 2:
        # output the json file as a table
        df = pd.read_json('filerecord.json')
        print(df.to_string(index=False))
        print("Done!!")

def searchvideo():
    list_json_csv("./videos/")
    df = pd.read_json('filerecord.json')
    print("1. Search with File Name\n2. Search with File Type\n3. Exit")
    searchoption = iv.in_vali(3, input("Enter your choice (1-3) => "))
    if searchoption == 1:
        search_filename = input("Enter the name of the file (at least one word to filter out) => ")
        # filter the result
        result = df[df['FileName'].str.contains(search_filename, case=False)]
        print(result.to_string(index=False))
        print("Done!!")
    if searchoption == 2:
        search_filetype = input("Enter the type of the file (File Extensions without '.') => ")
        result = df[df['FileType'].str.contains(search_filetype, case=False)]
        print(result.to_string(index=False))
        print("Done!!")

def deletevideo():
    makesure = iv.yesno(input("Are you sure you want to delete a file? (y/n) => "))
    if makesure == 'y':
        # To show the user what to delete
        list_json_csv("./videos/")
        df = pd.read_json('filerecord.json')
        print(df.to_string(index=False))
        deletefile = iv.int_only(input("Enter the 'number' of the file you want to delete => "))
        fileindex = -1
        for idx, files in enumerate(os.listdir("./videos/")):
            if os.path.isfile(os.path.join('./videos/', files)) and (deletefile == idx + 1):
                fileindex = idx
                makesure = iv.yesno(input(f"Is '{files}' the file you want to delete? (y/n) => "))
                if makesure == 'y':
                    os.remove(os.path.join('./videos/', files))
                    print("The File has been deleted!!")
                else:
                    print("The File isn't deleted!!")
        if fileindex == -1:
            print("The File you want to delete doesn't exist!!")
        
    list_json_csv("./videos/")

def updatevideo():
    updateoption = iv.yesno(input("Do you want to rename a file? (y/n) => "))
    if updateoption == 'y':
        list_json_csv("./videos/")
        df = pd.read_json('filerecord.json')
        print(df.to_string(index=False))
        file_rename = iv.int_only(input("Enter the 'number' of the file you want to rename => "))
        fileindex = -1
        for idx, files in enumerate(os.listdir("./videos/")):
            if os.path.isfile(os.path.join('./videos/', files)) and (file_rename == idx + 1):
                fileindex = idx
                makesure = iv.yesno(input(f"Is '{files}' the file you want to rename? (y/n) => "))
                if makesure == 'y':
                    basename, ext = os.path.splitext(files)
                    basename = input("Enter the new file name (exclude file extension) => ")
                    while ('.' in basename) or (basename == '') or (basename == ' '):
                        print('Invalid Name!')
                        basename = input("Enter the new file name (exclude file extension) => ")
                    filename = samebasename('./videos/', basename, ext) + ext
                    os.rename(os.path.join('./videos/', files), os.path.join('./videos/', filename))
                    print(f"The Filename has been changed from {files} to {filename}")
                else:
                    print("The Filenames remain Unchanged!")
        if fileindex == -1:
            print("The file you want to rename doesn't exist!!")
    else:
        print("The Filenames remain Unchanged!")

    # Fix Later to include Media and Resolution Conversion Feature

    list_json_csv("./videos/")