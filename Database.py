import pickle, os,sys

ADDRSTR=os.path.dirname(os.path.abspath(sys.argv[0])) #Gets the full path to the server.
class Database(object):
    def __init__(self):
        """The database constructor"""
        lists = open(ADDRSTR+"/mylists.txt", 'r')
        # All lists are saved in one text document
        # When opening the lists, use pickle
        self.BlackList = pickle.load(lists)
        self.EngineList = pickle.load(lists)
        self.IpList = pickle.load(lists)
        lists.close()
    
    def IfExists(self, item):
        """Gets an item, returns whether it exists and the name of the list."""

        # Search item in every list
        item = item.lower() #Lowers the item string to ignore the user's future penetrations attempts with case sensitivity.
        
        for i in self.BlackList:
            # The function searches the string item in every name in the list.
            
            if(item.find(i) != -1):
                return True, "Black"
        for i in self.EngineList:
            if(item.find(i) != -1):
                return True, "Engine"
        for i in self.IpList:
            if(item.find(i) != -1):
                return True, "Ip"
        return False, ""
    
    def Add(self, listname, item):
        """A functions that receives the item name and the list name and adds it to the database."""
        item = item.lower() #Lowers the item to prevent duplications.
        listname = listname.lower()
        # Adds the item only if it doesn't exist in the list
        (t, s) = self.IfExists(item)
        if t == False:
            # Finding the requested list
            if listname == "enginelist" or listname == "engine list":
                self.EngineList.append(item)
                self.__Update()
                print "Adding succeeded"
            elif listname == "blacklist" or listname == "black list":
                self.BlackList.append(item)
                self.__Update()
                print "Adding succeeded"
            elif listname == "iplist" or listname == "ip list":
                self.IpList.append(item)
                self.__Update()
                print "Adding succeeded"
            else:
                print "No such list :("
        else:
            print "Item exists"

    def __Update(self):
        """Updates the database textfile"""
        # This function updates all lists
        # It is used after every time a list is changed
        lists = open(ADDRSTR+"/mylists.txt", "r+")
        pickle.dump(self.BlackList, lists)
        pickle.dump(self.EngineList, lists)
        pickle.dump(self.IpList, lists)
        lists.close()
    
    def Remove(self, listname, item):
        """This function removes item from the list named listname"""
        item = item.lower()
        listname = listname.lower()
        # This flag is used to identify if an item has been removed
        flag = False
        # Searching the requested list
        if listname == "enginelist" or listname == "engine list":
            for i in self.EngineList:
                # Search the item in the list
                if item.find(i) != -1:
                    self.EngineList.remove(i)
                    # After removing, don't forget to update!
                    self.__Update()
                    flag = True
                    print "Removing succeeded"
        elif listname == "blacklist" or listname == "black list":
            for i in self.BlackList:
                if item.find(i) != -1:
                    self.BlackList.remove(i)
                    self.__Update()
                    flag = True
                    print "Removing succeeded"
        elif listname == "iplist" or listname == "ip list":
            for i in self.IpList:
                if item.find(i) != -1:
                    self.IpList.remove(i)
                    self.__Update()
                    flag = True
                    print "Removing succeeded"
        # If the listname wasn't any of above...
        else:
            print "listname Error"
            flag = True
        if flag == False:
            print "item doesn't exist"

    def Print(self, listname):
        """Prints each member of the list called listname"""
        listname = listname.lower()
        if listname == "blacklist" or listname == "black list":
            for i in self.BlackList:
                print i
        elif listname == "enginelist" or listname == "engine list":
            for i in self.EngineList:
                print i
        elif listname == "iplist" or listname == "ip list":
            for i in self.IpList:
                print i

    def StringList(self, listname):
        """Returns a string of all the members of listname"""
        listname = listname.lower()
        st=""
        if listname == "blacklist" or listname == "black list":
            for i in self.BlackList:
                st+=i+"\n"
        elif listname == "enginelist" or listname == "engine list":
            for i in self.EngineList:
                st+=i+"\n"
        elif listname == "iplist" or listname == "ip list":
            for i in self.IpList:
                st+=i+"\n"
        return st

