import socket, re, os, sys, httplib, urllib2, time, struct, select, Check

err404="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>404 Not Found</h1>\n</body></html>\n"
err403="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>403 Forbidden</title>\n</head><body>\n<h1>403 Forbidden</h1>\n</body></html>\n"
err302="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>302 Found</title>\n</head><body>\n<h1>302 Found. File has been temporarly moved to /file2.txt</h1>\n</body></html>\n"
SUPMETHODS=('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE') #supported methods except connect
HTTPVERSION='HTTP/1.1'
BUFLEN=8192
checker=Check.Check()

def recv_timeout(the_socket,timeout=0.5):
    """Receives the whole packet within the time frame given as the argument timeout"""

    
    the_socket.setblocking(0)
    total_data=[]
    data=''
    begin=time.time()
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*4:
            break
        try:
            data=the_socket.recv(BUFLEN)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.01)
        except:
            pass
    return ''.join(total_data)

def gethostport (string):
    """Get the target ip address and the port from the request"""
    i=string.find('Host')
    host= string[i+6:string.find("\n",i+5)]
    host= host.replace('\r','')
    host=host.replace('\n','')
    i = host.find(':')
    if i!=-1: #if there is a port mentioned
        port = int(host[i+1:])
        host = host[:i]
    else: #else give it the default value 80
        port = 80
    return host,port

def getget (string):
    """Get the substring between the two first spaces, which most likely will be the requested resource"""
    list=string.split(" ")
    if list[1].startswith("http://"):
        list=list[1][list[1].find('/',9):]
        return list
    elif list[1].startswith("https://"):
        return list[1][list[1].find('/',9):]
    else:
        return list[1]

def getmethod (string):
    """Returns the HTTP method type from the string"""
    return string[:string.find(' ')]

def one_client_request(client, addr,timeout):#Handling one client's request
    try:
        clientreq=recv_timeout(client,timeout=timeout) #Receives the whole request packet
        checkreq=checker.Decide(clientreq,addr) #Censoring it with check
        
        if (not checkreq.startswith("HTTP/")) and getmethod(checkreq) in SUPMETHODS and getmethod(checkreq)!="CONNECT": #If it's a request, if it is an existing http method
            (soc_family, _, _, _, address) = socket.getaddrinfo(gethostport(checkreq)[0], gethostport(checkreq)[1])[0]
            targetsocket=socket.socket(soc_family)
            targetsocket.connect(address) #Connect to the target socket
            _get=getget(checkreq) 
            _method=getmethod(checkreq)
            checkreq=checkreq[checkreq.find('\n')+1:]
            checkreq=_method+" "+_get+" "+"HTTP/1.1\r\n"+checkreq #Builds a clean HTTP request packet.
            targetsocket.send(checkreq)
            targetres=recv_timeout(targetsocket)
            targetsocket.close()
            client.send(targetres)
        elif (not checkreq.startswith("HTTP/")) and getmethod(checkreq)=="CONNECT": #If the method is connect
            (soc_family, _, _, _, address) = socket.getaddrinfo(gethostport(checkreq)[0], gethostport(checkreq)[1])[0]
            targetsocket=socket.socket(soc_family)
            l=getget(checkreq).split(':')
            connaddr=(l[0],int(l[1])) #gets the ipaddress and the port of the target host
            targetsocket.connect(connaddr)
            client.send('HTTP/1.1 200 Connection established\n'+
                         'Proxy-agent: Luz and Gery \n\n') #starting the handshake
            reedwryte(targetsocket,client) #continuing it
            targetsocket.close()
        else:
            client.send(checkreq) 
    except:
        try:
            client.send(err404)
        except:
            pass
    finally:
        client.close()
        
def reedwryte (targetsocket,client):
    """Data exchange for https"""
    targetsocket.setblocking(1)# set no time blocking
    client.setblocking(1)
    count=0
    limit=2**15 #a limit of while runs
    
    while count<limit:
        try:
            count=count+1
            rlist,_,xlist=select.select([client,targetsocket],[],[client,targetsocket],2) #orders the sockets in 3 lists- ready to read list, ready to write to list and error list. there's a timeout of 2 secs
            if xlist: #if there's an error, break
                break
            if rlist: #if there's anything to read from the sockets
                for soc in rlist:
                    data=soc.recv(BUFLEN)
                    if soc is client: #if you just read from the client, you should set the target as the target server and the opposite.
                        tar=targetsocket
                    if soc is targetsocket:
                        tar=client
                    if data:
                        tar.send(data)
        except:
            break
        

