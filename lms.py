class Book:

    #Initializes book with a tittle, year and author
    def __init__(self, tittle, year, author):
        self.tittle = tittle
        self.year = str(year)
        self.author = author
        self.serial = None

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

                #Formats the attributes of each Book as a delimited string. 
                #Writes to inventory file. 
                data = "\n" + newbook.tittle+"," + str(newbook.year) + ","+newbook.author + ","+ i
                with open (filepath, "a") as file:
                    file.write(data)
        print(f"Operation completed. {len(duplicates)} duplicates found and skipped.") 
    
    def importBook(self, file):
        with open(file, "r") as i:
            data = i.readlines()

        for book in data:
            book_elements= book.split(",")
            tittle = book_elements[0]
            year = book_elements[1]
            author = book_elements[2]
            serial = book_elements[3]
    
            newbook= Book(tittle, year, author)
            newbook.setSerial(serial)
            self.addBook(newbook, [newbook.bookSerial()])

    ##debugg this 
    def editRecord(self, serial, newserial = None, newTittle= None, newyear = None, newauthor = None ):
        
        if serial not in self.booklist:
            raise KeyError(f"Serial number {serial} not found.")
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
oat.addBook(Book("The Golden  Apple", 2023, "Ed Boon"), [111111,222222,3333336])
oat.addBook(Book("Jumanji", 2022, "oat" ), [111111, 555555])
res = oat.booklist.keys()    
print (res)
#oat.editRecord("111111", newserial="11112222") 
#print (res)

#oat.importBook("import.csv")

