import socket
import re
import os
import sys
import httplib
import urllib2
ROOT = "."
err404="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>404 Not Found</h1>\n</body></html>\n"
err403="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>403 Forbidden</title>\n</head><body>\n<h1>403 Forbidden</h1>\n</body></html>\n"
err302="<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>302 Found</title>\n</head><body>\n<h1>302 Found. File has been temporarly moved to /file2.txt</h1>\n</body></html>\n"
def isvalidreq (string): #checks if the request is a valid http get request
    listt=string.split(' ')
    return (listt[0]=='GET')#and listt[2][:8]!='HTTP/1.1') and listt[2][:8]!='HTTP/1.0')
def gethost (string): #gets the host from the get string
    i=string.find('Host')
    return string[i+6:string.find("\r\n",i+5)]

def getget (string): #gets the resource from the get request
    list=string.split(" ")
    return list[1]

##def save_image(data, cs):
##    g=re.search("Content-Length: ([0-9]+)",data)
##    if g:
##        cl=int(g.group(1))
##    else:
##        return False
##    g=re.search("image-name=(\w+\.\w+)",request)
##    if g:
##        fname=g.group(1)
##    else: return False
##    with open("pics/"+fname,'wb') as f:
##        ind=request.find("image=")+6
##        img=request[ind:]
##        f.write(img)
##        restl=cl-len(img)
##        while restl>0:
##            img=cs.recv(restl)
##            f.write(img)
##            restl-=len(img)
##        f.close()
##        return True
##    return False

def one_client_request(cs, addr):
    #Dealing with one client's request
##    while True:
    try:
        
        
        txt=cs.recv(1024) #getting requested by our beloved client
        print txt
        print "isvalid" + str(isvalidreq(txt))
        if isvalidreq(txt):
            print "Host--"+gethost(txt)
            csa = httplib.HTTPConnection(gethost(txt))
            print "GET "+getget(txt)
            try:
                csa.request("GET", getget(txt),headers={})
                r1 = csa.getresponse()
                print "nana",r1.status
                senttxt=r1.read()
                if r1.status==302 or r1.status==301:
                    print "respp"
                    resp=urllib2.urlopen("http://"+gethost(txt))
                    print resp.geturl()
                    loc=resp.geturl()[7:]
##                    print "MOVED ERR" , r1.reason
##                    loc=r1.getheader('Location')
##                    print "Original Loc", loc
##                    print "loc",loc[7:]
                    csa.close()
                    print "csa closed after another loc", loc[:loc.find('/')]
                    csa = httplib.HTTPConnection(loc[:loc.find('/')])
                    print "able to connect to new csa"
                    print "before get succeeded",loc[loc.find('/'):]
                    csa.request("GET",loc[loc.find('/')+1:] ,headers={})
                    print "hirfun"
                    r1 = csa.getresponse()
                    print r1.status
                    #print "nanana",r1.read()
                    print "lalalalala"
                    senttxta=r1.read()
                    cs.send(senttxta)
                    print "text was sent1"
                    csa.close()
                    cs.close()
                else:
                    cs.send(senttxt)
                    print "text was sent2"
            except:
                cs.send("404 not found")
                cs.close()
            csa.close()
        cs.close()
    except:
        pass
