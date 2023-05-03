from file_operation import *
import os
from datetime import datetime

#function to delete the files/folders that are not in the scr folder but they are in the replica folder
def delete_old_files(src_path : str, replica_path : str, log_file_stream) -> None:
    all_content_in_replica = os.listdir(replica_path)
    for content in all_content_in_replica:
        repl_path = replica_path + "/" + content
        src_path_content = src_path + "/" + content
        #we check if the file exists in the replica but it doesn`t exist in the source folder
        if os.path.isfile(repl_path) and not os.path.isfile(src_path_content):
            log_file_stream.write(f"Deleted File: {repl_path} at {datetime.time(datetime.now())}\n")
            print(f"Deleted File: {repl_path} at {datetime.time(datetime.now())}")
            os.remove(repl_path)
        if os.path.isdir(repl_path):
            # we check recursively the content of the folder
            delete_old_files(src_path_content, repl_path, log_file_stream)
            #check to see if the folder in the replica exists in the source folder
            if not os.path.isdir(src_path_content):
                os.rmdir(repl_path)
                log_file_stream.write(f"Deleted Folder: {repl_path} at {datetime.time(datetime.now())}\n")
                print(f"Deleted Folder: {repl_path} at {datetime.time(datetime.now())}")

#function to copy/update all the files/folders that are in the src folder but not in the replica folder
def copy_new_files(src_path : str, replica_path : str, log_file_stream) -> None:
    all_content_in_src = os.listdir(src_path)
    for content in all_content_in_src:
        content_path = src_path + "/" + content
        copy_path = replica_path + "/" + content
        if os.path.isfile(content_path):
            #check if the file doesn`t exist in the replica file
            if not os.path.isfile(copy_path):
                copy_file(content_path, copy_path)
                log_file_stream.write(f"Created and Copied File: {content_path} at {datetime.time(datetime.now())}\n")
                print(f"Created Copied File: {content_path} at {datetime.time(datetime.now())}")
            #in case it exists we check if it`s the same file as the original one
            if not check_same_file(content_path, copy_path):
                copy_file(content_path, copy_path)
                log_file_stream.write(f"Updated File: {content_path} at {datetime.time(datetime.now())}\n")
                print(f"Updated File: {content_path} at {datetime.time(datetime.now())}")

        elif os.path.isdir(content_path):
            #check to see if the directory doesn`t exist
            if not os.path.isdir(copy_path):
                os.mkdir(copy_path)
                log_file_stream.write(f"Created Folder: {copy_path} at {datetime.time(datetime.now())}\n")
                print(f"Created Folder: {copy_path} at {datetime.time(datetime.now())}")
            #if it exists we check recursively the contect of that folder
            copy_new_files(content_path, copy_path, log_file_stream)

#function to delete everything in the replica folder
def clear_replica(repl_path : str) -> None:
    all_content_in_replica = os.listdir(repl_path)
    for content in all_content_in_replica:
        content_path = repl_path + "/" + content
        if os.path.isfile(content_path):
            os.remove(content_path)
        elif os.path.isdir(content_path):
            clear_replica(content_path)
            os.rmdir(content_path)

def update_replica(src_path : str, replica_path : str, log_file_stream) -> None:
    delete_old_files(src_path, replica_path, log_file_stream)
    copy_new_files(src_path, replica_path, log_file_stream)
    log_file_stream.flush()