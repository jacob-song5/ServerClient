import socket
#public ip of server is 70.187.186.128

def main():
    connection = makeSocket("108.192.40.180")
    wantedFile = input("What file would you like: ")
    connection.send(wantedFile.encode())
    validateRequest(connection.recv(8192).decode(), wantedFile, connection)
    connection.close()

def makeSocket(ip):
    s = socket.socket()
    host = ip
    port = 9462
    s.connect((host, port))
    return s

def adjustFileName(fn):
    for i in range(len(fn)-1, 0, -1):
        if fn[i] == '\\':
            return fn[i+1:]

def copyFile(fileName: str, connection):
    f = open(fileName, 'wb')
    n = 1
    while (n):
        print("Receiving")
        n = connection.recv(8192)
        f.write(n)
    f.close()
    print("Done Receiving")

def validateRequest(response: str, wantedFile: str, connection) -> bool:
    if response == "Transfering your file now":
        copyFile(adjustFileName(wantedFile), connection)
    

main()
