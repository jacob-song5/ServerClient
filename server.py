import socket
import os
from pathlib import Path
import pathFunctions

def main():
    server = makeSocket()
    while True:
        currentPath = Path("E:\\Users\\Jake")
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
    
def copyFile(c, fileName: str):
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

def validateRequest(request: str, c, path: Path):
    if os.path.isfile(request):
        c.send("Transfering your file now".encode())
        copyFile(c, request)

    elif os.path.isfile(pathFunctions.adjustPathString(str(path), request)):
        c.send("Transfering your file now".encode())
        copyFile(c, pathFunctions.adjustPathString(str(path), request))

    elif request == "ls":
        c.send("ls incoming".encode())
        lsCommand(path, c)
        validateRequest(c.recv(8192).decode(), c, path)

    elif request[0:2] == "cd":
        newPath = cdCommand(request, c, path)
        validateRequest(c.recv(8192).decode(), c, newPath)
    
    else:
        c.send("Not a valid request".encode())
        validateRequest(c.recv(8192).decode(), c, path)

    c.close()

def cdCommand(request: str, connection, currentPath: Path) -> Path:
    requestedPath = request[3:]
    
    if pathFunctions.validPath(requestedPath) and os.path.isdir(requestedPath):
        connection.send("path changed".encode())
        return Path(requestedPath)

    elif pathFunctions.validPath(pathFunctions.adjustPathString(str(currentPath), requestedPath)) and \
         os.path.isdir(pathFunctions.adjustPathString(str(currentPath), requestedPath)):
        connection.send("path changed".encode())
        return currentPath / requestedPath

    else:
        connection.send("nothing done".encode())
        return currentPath
    
main()
