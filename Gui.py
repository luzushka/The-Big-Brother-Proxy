import Database, httpServerMT, os,sys, EmailGL
print "Welcome, Big Brother!"
addrstr=os.path.dirname(os.path.abspath(sys.argv[0]))
while 1:
    print "What would you like to do? \npress 'O' to activate the proxy server \n1. Print Black list \n2. Print Engine list \n3. Print IP List \n4. Add to Black list \n5. Add to Engine list \n6. Remove something from Black List \n7. Remove something from Engine List\n8. Email the rat addresses to you!"
    data = Database.Database()
    a = raw_input("Insert a request: ")
    if a == '1':
        data.Print("BlackList")
    if a == '2':
        data.Print("EngineList")
    if a == '3':
        data.Print("IpList")
    if a == '4':
        b = raw_input("What would you like to add? ")
        data.Add("blacklist", b)
    if a == '5':
        b = raw_input("What would you like to add? ")
        data.Add("enginelist", b)
    if a == '6':
        b = raw_input("What would you like to remove? ")
        data.Remove("blacklist", b)
    if a == '7':
        b = raw_input("What would you like to remove? ")
        data.Remove("enginelist", b)
    if a=='O' or a=='o':
        port=raw_input("Which port would you like it to be on? ")
        timeout=raw_input("What is the timeout you'd like to work with? (leave blank for 0.25s)")
        os.system("start cmd /c "+addrstr+"\serverstarter.py "+port+" "+timeout)
    if a=='8':
        to=raw_input("To whom would you like to send it to, brother?")
        subject="A list of filthy rats!"
        text="These are the IP addresses of the people who betrayed you, Big Brother:\n"+data.StringList("iplist")
        try:
            EmailGL.SendMail (to,subject,text)
        except:
            print "Some error occured, you've probably been blocked"
    a=raw_input("\nPress enter to continue")
    

        
        
    
