import socket
import os
from pathlib import Path
import pathFunctions
from timeit import default_timer as timer

def main():
    server = makeSocket()
    while True:
        currentPath = Path("E:\\Users\\Jake\\Pictures\\Bookmarks")
        handleConnection(server, currentPath)

def makeSocket():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    port = 9462
    s.bind((host, port))
    s.listen(5)
    return s

def handleConnection(s, currentPath: Path):
    c, addr = s.accept()
    print("Got connection from", addr)
    request = c.recv(16384).decode()
    validateRequest(request, c, currentPath)
    
def copyFile(c, fileName: str):
    f = open(fileName, 'rb')
    n = 1
    start = timer()
    while (n):
        n = f.read(16384)
        c.send(n)
    print(timer() - start)
    f.close()
    print("Done Writing")

def lsCommand(path: Path, c):
    pathList = os.listdir(path)
    for item in pathList:
        c.send((item+'\n').encode())
    c.send("!!!!".encode())

def trfCommand(request: str, c):
    total_list = pathFunctions.recursive_list(Path(request))
    for item in total_list:
        string_item = str(item) + ';'
        c.send(string_item.encode())
    c.send("!".encode())

def validateRequest(request: str, c, path: Path):
    if request == "":
        pass
    
    elif os.path.isfile(request):
        c.send("tr now".encode())
        copyFile(c, request)

    elif os.path.isfile(pathFunctions.adjustPathString(str(path), request)):
        c.send("tr now".encode())
        copyFile(c, pathFunctions.adjustPathString(str(path), request))

    elif os.path.isdir(request):
        c.send("trfnow".encode())
        trfCommand(request, c)

    elif os.path.isdir(pathFunctions.adjustPathString(str(path), request)):
        c.send("trfnow".encode())
        trfCommand(pathFunctions.adjustPathString(str(path), request), c)

    elif request == "ls":
        print("ls handled")
        c.send("ls inc".encode())
        lsCommand(path, c)
        validateRequest(c.recv(16384).decode(), c, path)

    elif request[0:2] == "cd":
        print("cd handled")
        newPath = cdCommand(request, c, path)
        validateRequest(c.recv(16384).decode(), c, newPath)
    
    else:
        c.send("notval".encode())
        validateRequest(c.recv(16384).decode(), c, path)

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
