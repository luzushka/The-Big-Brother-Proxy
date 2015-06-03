import Database, os,sys

addrstr=os.path.dirname(os.path.abspath(sys.argv[0]))
class Check:

    def __init__ (self):
        """Constructor of Check"""
        self.blistsite=open(addrstr+'/blistsite.html','r+').read()
        self.selsite=open(addrstr+'/selsite.html','r').read()
        self.db=Database.Database()


    def getget (self,string):
        """Get the substring between the two first spaces, which most likely will be the requested resource"""
        list=string.split(" ")
        if list[1].startswith("http://"):
            list=list[1][list[1].find('/',9):]
            return list
        elif list[1].startswith("https://"):
            return list[1][list[1].find('/',9):]
        else:
            return list[1]

    
    def gethostport (self,string):
        """Get the target host and the port from the request"""
        i=string.find('Host')
        host= string[i+6:string.find("\n",i+5)]
        host= host.replace('\r','')
        host=host.replace('\n','')
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        return host,port

    


    def Decide (self,request,addr): #args: request is the whole http request, addr is the client's address
        """Returns a censored version of the HTTP request"""
        if request.startswith("CONNECT"): #https request
            
            
            if self.db.IfExists(self.getget(request))[1]=="Black": #If the requested host is in the black list, send it the blacklist site instead.
                self.db.Add ("IpList",addr[0])
                return "HTTP/1.1 200 OK\r\nContent-Length: "+str(len(self.blistsite))+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+self.blistsite
            if self.db.IfExists(self.getget(request))[1]=="Engine":#If the requested host is in the serch engine list, send it the search engine site instead.
                self.db.Add ("IpList",addr[0])
                return "HTTP/1.1 200 OK\r\nContent-Length: "+str(len(self.selsite))+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+self.selsite
            else: #otherwise don't manipulate it
                return request
        else:#http request
            
            if self.db.IfExists(self.gethostport(request)[0])[1]=="Black":
                self.db.Add ("IpList",addr[0])
                return "HTTP/1.1 200 OK\r\nContent-Length: "+str(len(self.blistsite))+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+self.blistsite
            if self.db.IfExists(self.gethostport(request)[0])[1]=="Engine":
                self.db.Add ("IpList",addr[0])
                return"HTTP/1.1 200 OK\r\nContent-Length: "+str(len(self.selsite))+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+self.selsite
            else:
                return request
            
        
        

        
