import socket
import os
import tqdm
import buffer

# device's IP address
SERVER_HOST = '10.42.0.37'
# SERVER_HOST = socket.gethostname()
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


# create the server socket
# TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Waiting for connection as {SERVER_HOST}:{SERVER_PORT} .....")

while True:
    save_dir = input("Recieving Path: ")
    if os.path.isdir(save_dir):
        print(f"Saving recieved files to {save_dir}")
        break
    else:
        print("Entered path does not exist\n Enter Again...\n")

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return True

while True:
    conn, addr = s.accept()
    print("Got a connection from ", addr)
    connbuf = buffer.Buffer(conn)

    while True:
        hash_type = connbuf.get_utf8()
        if not hash_type:
            break
        print('hash type: ', hash_type)
        if hash_type == "folder":
            folder_path = connbuf.get_utf8()
            folder_path = "/".join(folder_path.split(SEPARATOR))
            print(f"we got a folder {folder_path}")
            create_dir(os.path.join(save_dir, folder_path))

        elif hash_type == "file":
            file_name = connbuf.get_utf8()
            if not file_name:
                break
            file_name = "/".join(file_name.split(SEPARATOR))
            file_name = os.path.join(save_dir, file_name) 
            print('file name: ', file_name)

            file_size = int(connbuf.get_utf8())
            print('file size: ', file_size )

            progress = tqdm.tqdm(range(file_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = connbuf.get_bytes(chunk_size)
                    if not chunk: break
                    f.write(chunk)
                    remaining -= len(chunk)
                    progress.update(len(chunk))
                if remaining:
                    print('File incomplete.  Missing',remaining,'bytes.')
                else:
                    print('File received successfully.')
    print('Connection closed.')
    conn.close()