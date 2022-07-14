import socket
import tqdm
import os
import buffer

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = r"192.168.26.224"
# host = socket.gethostname()
# the port, let's use 5001
port = 5001

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")




def send_folder(folder_path, parent_folder, sbuf):
    # send the foldername 
    foldername = os.path.basename(folder_path)
    # s.send(f"folder{SEPARATOR}{parent_folder}".encode())

    hash_type = "folder"
    sbuf.put_utf8(hash_type)
    file_path = SEPARATOR.join(parent_folder.split("\\"))
    sbuf.put_utf8(file_path)
    dir_entry = os.scandir(folder_path)
    for entry in dir_entry:
        if entry.is_file():
            print("file: --------- ", entry.name)
            send_file(os.path.join(folder_path, entry.name), os.path.join(parent_folder, entry.name), sbuf)
        if entry.is_dir():
            send_folder(os.path.join(folder_path, entry.name), os.path.join(parent_folder, entry.name), sbuf)
    return True

def send_file(filename, relative_path, sbuf):
    # # the name of file we want to send, make sure it exists
    # filename = r"D:\PC\edrive\New folder\04.mpg"
    # get the file size
    filesize = os.path.getsize(filename)
    file_path = SEPARATOR.join(relative_path.split("\\"))
    # filename = os.path.basename(filename)
    # send the filename and filesize
    # s.send(f"file{SEPARATOR}{relative_path}{SEPARATOR}{filesize}".encode())
    hash_type = "file"
    sbuf.put_utf8(hash_type)
    sbuf.put_utf8(file_path)
    sbuf.put_utf8(str(filesize))
    #start sending the file
    with open(filename, "rb") as f:
        print("Sending File "+relative_path)
        sbuf.put_bytes(f.read())
        print('File Sent')

with s:
    folder = input("Folder Path: ")
    s_buffer = buffer.Buffer(s)
    send_folder(folder, os.path.basename(folder), s_buffer)
# close the socket
# s.close()