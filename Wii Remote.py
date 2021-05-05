#!/usr/bin/env python
import sys
import socket
import random
LISTENQ = 5
def CreateServerSocket(port):
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveraddr = ('', port)
    serversock.bind(serveraddr)
    serversock.listen(LISTENQ)
    return serversock
def getRequest(sock):
    # Receive Something
    try:
        request = sock.recv(512)
    except Exception as e:
        print str(e)+ "Recieving"
    return request
def sendResponse(message,sock):
    # Send Something
    crlf = "\r\n"
    httpResponse = "HTTP/1.1 200 OK" + crlf
    httpResponse += "Content-Type: text/html; charset=ISO-8859-1" + crlf
    httpResponse += "Access-Control-Allow-Origin: *" + crlf
    httpResponse += crlf
    httpResponse += message + crlf
    try:
        sock.send(httpResponse)
    except Exception as e:
        print str(e)+ "Sending"
def getCommand(sock):
    request=getRequest(sock)
    if len(request)>0:
        if "GET" in request:
            command = request[5:request.index("HTTP")-1:]
            command = command.split("/")
        else:
            command=''
    else:
        command=''
    return command
def policyFile(port):
    return '<cross-domain-policy>\n\
<allow-access-from domain="*" to-ports="'+str(port)+'"/>\n\
</cross-domain-policy>\n\0'
def doCommand(command,sock,svars,wii):
    response = "okay"
    if "crossdomain.xml" in command:
        response = policyFile(9013)
    elif len(command) == 0:
        response = "HTTP Extension Example Server<br><br>"
    elif "poll" in command:
        s=""
        for key in svars:
            s += key + ' ' + svars[key] + '\n'
        response=s[:len(s)-1:]
    elif "kill" in command:
        wii.send("/".join(command)+",")
        print "Ending Server"
        return True, svars
    elif "reset_all" in command:
        print "Stop!!"
        response = "Stop!!"
    elif "rumble" in command:
        wii.send("/".join(command)+",")
    elif "light" in command:
        wii.send("/".join(command)+",")
    elif "con" in command:
        wii.send("/".join(command)+",")
    else:
        response = "unknown command: " + command[0]
    sendResponse(response,sock)
    return False, svars
def main():
    port = 9013
    serversock = CreateServerSocket(port)
    serversock.setblocking(0)
    wiisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wiiaddr=("192.168.1.230",9075)
    wiisock.connect(wiiaddr)
    wiisock.setblocking(0)
    print "connected to wii server"
    done = False
    svars={}
    info=[]
    while not done:
        try:
            info = wiisock.recv(512).split(",")
        except Exception as e:
            if not "imme" in str(e):
                print str(e)+"Wii"
        if len(info)>0:
            for i in info:
                if ":" in i:
                    a=i.split(":")
                    svars[a[0]]=a[1]
        g=1
        try:
            (sock, clientaddr) = serversock.accept()
            sock.setblocking(1)
        except:
            g=0
        if g==1:
            command = getCommand(sock)
            done, svars = doCommand(command,sock,svars,wiisock)
            sock.close()
main()

