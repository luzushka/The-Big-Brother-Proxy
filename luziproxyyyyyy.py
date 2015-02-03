import httplib
import socket

def isvalidreq (string): #checks if the request is a valid http get request
    listt=txt.split(' ')
    return (listt[0]=='GET' and listt[2][:8]!='HTTP/1.1') or  (listt[0]=='GET' and listt[2][:8]!='HTTP/1.0')
def gethost (string): #gets the host from the get string
    i=string.find('Host')
    return string[i+6:string.find("\r\n",i+5)]

def getget (string): #gets the resource from the get request
    list=string.split(" ")
    return list[1]



server_socket=socket.socket()
server_socket.bind(('0.0.0.0',8080))

while True:
    try: #try to handle sudden closed connections
        server_socket.listen(1)

        while True:
            (client_socket,client_address)=server_socket.accept()
            txt=client_socket.recv(4096) #getting requested by our beloved client
            print txt
            print "isvalid" + str(isvalidreq(txt))
            if isvalidreq(txt):
                print "Host--"+gethost(txt)
                conn = httplib.HTTPConnection(gethost(txt))
                print "GET "+getget(txt)
                try:
                    conn.request("GET", getget(txt),headers={})
                    r1 = conn.getresponse()
            
                    senttxt=r1.read()
                    client_socket.send(senttxt)
                except:
                    client_socket.send("404 not found")
                conn.close()
            client_socket.close()
        
    except:
        continue
