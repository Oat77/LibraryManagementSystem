class Book:

    #Initializes book with a tittle, year and author
    def __init__(self, tittle, year, author):
        self.tittle = tittle
        self.year = str(year)
        self.author = author
        self.serial = None
        self.status = None

    #Returns book's tittle
    def bookTittle(self):
        return self.tittle

    #Returns book's year
    def bookYear(self):
        return self.year
    
    #Returns book's author
    def bookAuthor(self):
        return self.author
    
    #Returns book's serial number
    def bookSerial(self):
        return self.serial
    
    #Returns book's status
    def status(self):
        return self.status
    
    #Sets book's new tittle
    def setTittle(self, newtittle):
        self.tittle = newtittle

    #Sets book's new year
    def setYear(self, newyear):
        self.year = newyear
    
    #Sets book's new author
    def setAuthor(self, newauthor):
        self.author = newauthor

    #Sets book's serial number
    def setSerial(self, newserial):
        self.serial = newserial

    #Sets book's status
    def setStatus(self, newstatus):
        self.status = newstatus


class Inventory:

    #Initializes with an empty dictionary
    def __init__(self): 
        self.booklist = {}

    #Adds a book object to the dictionary (accepts a list of serial numbers)
    def addBook(self, newbook, serials = None):

        #Library inventory file
        filepath = "inventory.csv"
        duplicates = []

        
        #Iterates through each serial number in the list 
        #Adds Book objects to the booklist each having a serial number as a key.  
        for i in serials:
            if str(i) in self.booklist.keys():
                duplicates.append(i)
                #raise KeyError (f"Serial number {i} already in database. Operation cancelled.")
            else:
                i = str(i)
                self.booklist[i] = newbook
                newbook.setStatus("Available")

                #Formats the attributes of each Book as a delimited string. 
                #Writes to inventory file. 
                data = "\n" + newbook.tittle+"," + str(newbook.year) + ","+newbook.author + ","+ newbook.status + ","+ i
                with open (filepath, "a") as file:
                    file.write(data)
        print(f"Operation completed. {len(duplicates)} duplicates found and skipped.") 
    
    #imports books from a .csv file
    def importBook(self, file):

        #holder for duplicate serial numbers
        duplicates = []

        #splits each line in the import file based on a delimiter and stores each element in a variable
        with open(file, "r") as i:
            data = i.readlines()

        for book in data:
            book_elements= book.split(",")
            tittle = book_elements[0]
            year = book_elements[1]
            author = book_elements[2]
            status = book_elements[3]
            serial = book_elements[4:]

            #Checks list of serials extracted from the import fike  for entries already present in the system.
            #If duplicate is found, serial number is removed from the import file variable. 
            for i in serial:
                if i in self.booklist.keys():
                    duplicates.append(i)
                    serial.remove(i)
                    
            #Creates a Book object, adds it to the database. 
            newbook= Book(tittle, year, author)
            self.addBook(newbook, serial)

            #addBook() method defaults the books status as 'Available'. 
            #This will set them to the status specified in the import file. 
            for i in serial:
                for y in self.booklist.keys():
                    if i == y:
                        self.booklist[i].setStatus(status)
                    continue          
            print(f"Operation completed. {len(duplicates)} duplicates found and skipped.") 
                
    #Allows for the editing of any of a book's attributes
    def editRecord(self, serial, newserial = None, newTittle= None, newyear = None, newauthor = None ):
        
        #Raises KeyError if the book tied to the given serial is not found
        if serial not in self.booklist:
            raise KeyError(f"Serial number {serial} not found.")
        
        #Sets new attributes based on the submitted arguements in the function
        else:
            book = self.booklist[serial]
            if newTittle != None:
                book.setTittle(newTittle)
            if newyear != None:
                book.setYear(newyear)
            if newauthor != None:
                book.setAuthor(newauthor)
            if newserial != None:
                if serial in self.booklist.keys() and serial != newserial:
                    self.booklist[newserial] = book
                    del self.booklist[serial]
                else:
                    raise KeyError("Invalid entry. Please verify data and try again.")


           

    


            




    

    
oat = Inventory()
#oat.addBook(Book("The Golden  Apple", 2023, "Ed Boon"), [111111,222222,3333336])
oat.addBook(Book("Jumanji", 2022, "oat" ), ["111111", "555555"])
oat.importBook("import.csv")
res = oat.booklist.keys()  
items = oat.booklist.values()
print (res)
print (items)
for i in items:
    status = i.status
    print (status)
    #print (i.status())
#oat.editRecord("111111", newserial="11112222") 
#print (res)


