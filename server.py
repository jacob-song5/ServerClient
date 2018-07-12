import socket
import os
from pathlib import Path
import pathFunctions

def main():
    server = makeSocket()
    while True:
        currentPath = Path("E:\\Users\\Jake\\Pictures\\Bookmarks")
        handleConnection(server, currentPath)

def makeSocket():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    #public ip of server is 108.192.40.180
    port = 9462
    s.bind((host, port))
    s.listen(5)
    return s

def handleConnection(s, currentPath: Path):
    c, addr = s.accept()
    print("Got connection from", addr)
    request = c.recv(8192).decode()
    validateRequest(request, c, currentPath)
    
def copyFile(c, fileName):
    f = open(fileName, 'rb')
    n = 1
    while (n):
        #print('Writing')
        n = f.read(8192)
        c.send(n)
    f.close()
    print("Done Writing")

def lsCommand(path: Path, c):
    pathList = os.listdir(path)
    for item in pathList:
        c.send((item+'\n').encode())
    c.send("!!!!".encode())
    print("ls handled")

def validateRequest(request: str, c, path: Path):
    if pathFunctions.validPath(request):
        c.send("Transfering your file now".encode())
        copyFile(c, request)

    elif request == "ls":
        c.send("ls incoming".encode())
        lsCommand(path, c)
        validateRequest(c.recv(8192).decode(), c, path)
    
    else:
        c.send("Not a valid file".encode())
        print("Rejected a request")

    c.close()

main()
