import socket
import re
import os
import sys
from serverUtils import *
from threading import Thread
from Queue import Queue

class httpServerMT (object):

    def __init__ (self, port,timeout): #The server's constructor
        self.serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #af_inet=(ip,host) addresses, 
        self.port=port
        self.host=''
        self.threadpool=20
        self.q=Queue(self.threadpool)
        self.timeout=timeout #Maximum time (in seconds) of accepting one request packet from a client, works with time because there was no EOF indicator.
        self.serverip=self.FindInternalIP()

    
    def doWork(self): #Each thread runs this function
        while 1:
            #pull next conncetion from the queue
            conn, addr=self.q.get()
            #Take care of clients requests
            one_client_request(conn, addr,self.timeout)
            self.q.task_done() #Indicates that the former request was adressed.


    def FindInternalIP (self): #A function that finds the internal IP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #SOCK_DGRAM=udp socket
        s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
        local_ip_address = s.getsockname()[0]
        s.close()
        return local_ip_address

    
    def ServerActivation (self):
        #Start a pool of workers
        for i in xrange(self.threadpool):
            t=Thread(target=self.doWork, args=()) #Creates a thread, and tells it what function it should do with which arguments.
            t.daemon=True #This means that every thread would be automatically "killed" once the server shuts down.
            t.start()


        #Establish server
       
        
        #Find a free port
        while 1:
            try:
                self.serversocket.bind((self.host, self.port))
                break
            except Exception:
                self.port=self.port+1

        #Start main server
        self.serversocket.listen(0) #Listens without limiting to a specific amount of clients.
        print "Server Started: Listening on address: {}:{}".format(self.serverip, self.port)
        while 1: #Accepts connections.
            conn, addr = self.serversocket.accept()
            
           
            print "Server log: New connection: {}:{}\n".format(addr[0],str(addr[1]))
            #Put info in queue and return to serve another client
            self.q.put((conn, addr))     




