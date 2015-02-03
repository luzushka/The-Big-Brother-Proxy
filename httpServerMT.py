import socket
import re
import os
import sys
from serverUtils import *
from threading import Thread
from Queue import Queue

HOST = ''
PORT = 8200
#Number of threads in the pool
THREADPOOL = 20
#Queue size
QUEUESIZE= THREADPOOL * 2

#Start a new Queue object
q=Queue(QUEUESIZE)

#Each thread does this work
def doWork(name):
    print "{} started\n".format(name)
    while True:
        #pool next conncetion from the queue
        conn, addr=q.get()
        #Take care of clients requests
        
        one_client_request(conn, addr)
        print "Server log: Thread {} completed to serve request from: {}:{}".format(name,addr[0],str(addr[1]))
        q.task_done()

#Start a pool of workers
for i in xrange(THREADPOOL):
    name="T-"+str(i)
    t=Thread(target=doWork, args=(name,))
    t.daemon=True
    t.start()


#Establish server
#The server expects that files reside in teh same direcotry it run from. There should be a file index.html in this directory and a sub directory ./pics to store and serve images
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Find a free port
while True:
    try:
        s.bind((HOST, PORT))
        break
    except Exception:
        PORT=PORT+1

#Start main server
s.listen(1)
print "Server log: Listening on address: {}:{}".format(HOST, PORT)
#Server's main loop
while True:
    conn, addr = s.accept()
    
   
    print "Server log: New connection: {}:{}\n".format(addr[0],str(addr[1]))
    #Put info in queue and return to serve another client
    q.put((conn, addr))     
    

s.close()
