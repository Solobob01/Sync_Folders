import hashlib

MAX_THR = 10000

#we create a md5 hash for a file
def get_hash(file_path : str) -> bytes: 
    hasher = hashlib.md5()
    file_path_stream = open(file_path, "rb")
    hasher.update(file_path_stream.read())
    return hasher.digest()

#based on the md5 hash we verify if the first file (src) and the second file(dest) are the same
def check_same_file(src : str, dest : str) -> bool:
    return get_hash(src) == get_hash(dest)

#function to copy a file (src) to a destination path (dest)
def copy_file(src : str, dest : str) -> None:
    src_stream = open(src, "rb")
    
    #check for coruption
    for _ in range(0, MAX_THR):
        dest_stream = open(dest, "wb")  
        dest_stream.write(src_stream.read())
        dest_stream.flush()
        if check_same_file(src, dest):
            dest_stream.close()
            break
        dest_stream.close()
   

    src_stream.close()