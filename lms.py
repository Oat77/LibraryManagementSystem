import copy 
from datetime import datetime


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
    def bookStatus(self):
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


class Member:

    def __init__(self, fname, lname, id):
        self.fname = fname
        self.lname = lname
        self.id = id
        self.books = []

    def firstName(self):
        return self.fname
    
    def lastName(self):
        return self.lname
    
    def idNum(self):
        return self.id
    
    def setFname(self, newname):
        self.fname = newname

    def setLname(self, newname):
        self.lname = newname

    def registerBook(self, book, duedate):
        self.books.append([book, duedate])

    def returnBook(self, book):
        for booking in self.books:
            if booking[0] == book:
                self.books.remove(booking)
                break
        else:
            raise KeyError ("Booking not found.")

class Inventory:

    #Initializes with an empty dictionary
    def __init__(self): 
        self.booklist = {}

    #Library inventory file
        self.filepath = "inventory.csv"
        self.borrowinglogpath = "borrowinglog.csv"

    #Adds a book object to the dictionary (accepts a list of serial numbers)
    def addBook(self, newbook, serials = None):
        duplicates = []    
        #Iterates through each serial number in the list 
        #Adds Book objects to the booklist each having a serial number as a key.  
        if not serials:
            raise ValueError ("No serials provided. Operation cancelled.")
        for i in serials:
            if str(i) in self.booklist.keys():
                duplicates.append(i)
                continue
            else:
                book = copy.deepcopy(newbook)
                i = str(i)
                self.booklist[i] = book
                book.setStatus("Available")
                book.setSerial(i)
                

                #Formats the attributes of each Book as a delimited string. 
                #Writes to inventory file. 
                data = book.tittle+"," + str(book.year) + ","+book.author + ","+ book.bookStatus() + ","+ i + "\n" 
                with open (self.filepath, "a") as file:
                    file.write(data)
        print(f"Operation completed. {len(duplicates)} duplicates found and skipped.") 
    
    #imports books from a .csv file
    def importBook(self, file):

        #splits each line in the import file based on a delimiter and stores each element in a variable
        with open(file, "r") as i:
            data = i.readlines()

        for book in data:
            book_elements= book.split(",")
            tittle = book_elements[0].strip()
            year = book_elements[1].strip()
            author = book_elements[2].strip()
            status = book_elements[3].strip()
            serial_raw = book_elements[4:]

            #Removes whitespace from serial numbers
            serial = [s.strip() for s in serial_raw]

            #Checks list of serials extracted from the import fike  for entries already present in the system.
            #If duplicate is found, serial number is removed from the import file variable. 
            total_duplicates = []
            duplicates = [s for s in serial if s in self.booklist.keys()]
            serial = [s for s in serial if s not in self.booklist.keys()]
            total_duplicates.extend(duplicates)

                    
            #Creates a Book object, adds it to the database. 
            newbook= Book(tittle, year, author)
            self.addBook(newbook, serial)

            #addBook() method defaults the books status as 'Available'. 
            #This will set them to the status specified in the import file. 
            for i in serial:
                if i in self.booklist.keys():
                    self.booklist[i].setStatus(status)          

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
                if newserial not in self.booklist or serial == newserial:
                    del self.booklist[serial]
                    self.booklist[newserial] = book
                    book.setSerial(newserial)
                else:
                    raise KeyError("Invalid entry. Please verify data and try again.")
    
    #deletes a book based on supplied serial number.
    def delBook(self, serial):
        if serial not in self.booklist:
            raise KeyError(f"Serial number {serial} not found")
        else: 
            del self.booklist[serial]
            with open(self.filepath, "w") as file:
                for book in self.booklist.values():
                    # Write one CSV line per book: tittle, year, author, status, serial
                    line = (
                        str(book.bookTittle()) + "," +
                        str(book.bookYear()) + "," +
                        str(book.bookAuthor()) + "," +
                        str(book.bookStatus()) + "," +
                        str(book.bookSerial())+ "\n")
                    file.write(line)

    #Deletes the records of all books of a given tittle. 
    def delRecords(self, tittle):
        serials_to_delete = []
        for i in self.booklist.values():
            if i.bookTittle() == tittle:
                serial = i.bookSerial()
                serials_to_delete.append(serial)
                
        for serial in serials_to_delete:
            if serial in self.booklist:
                del self.booklist[str(serial)]
                with open(self.filepath, "w") as file:
                    for book in self.booklist.values():
                        # Write one CSV line per book: tittle, year, author, status, serial
                        line = (
                            str(book.bookTittle()) + "," +
                            str(book.bookYear()) + "," +
                            str(book.bookAuthor()) + "," +
                            str(book.bookStatus()) + "," +
                            str(book.bookSerial())+ "\n")
                        file.write(line)


    #Runs a search for a specific tittle returning the number of available copies. 
    def tittleSearchQuery(self, tittle):
        queryresults=[]
        for i in self.booklist.values():
            if i.bookTittle() == tittle and i.bookStatus() == "Available":
                queryresults.append(i)
        return tittle + ": "+ str(len(queryresults))+ " available copies."

    #Returns a listing of books based on a given status. 
    def statusSearchQuery(self, status):
        queryresults=[i for i in self.booklist.values() if i.bookStatus() ==status]
        if not queryresults:
            return status + " books: 0"
        else:
            for book in queryresults:
                return  ", ".join(book.bookTittle() + " ("+ book.bookSerial()+ ")" )

    def bookListing(self):
        listing = []
        for i in self.booklist.values():
            listing.append((i.bookSerial(), i.bookTittle(),i.bookStatus()))
        return listing
        
    def checkOut(self, serial, member, duedate):
        current_time = datetime.now()
        if serial not in self.booklist.keys():
            raise KeyError (f"Serial {serial} not found. Operation cancelled.")
        elif self.booklist[serial].bookStatus() == "Checked Out" or self.booklist[serial].bookStatus() == "Reserved":
            raise KeyError (f"Book is not available. Please choose another book.")
        else:
            self.booklist[serial].setStatus("Checked Out")
            member.registerBook(self.booklist[serial], duedate)
            data =  (str(current_time)+ "," + "Checkout"+ ","+ self.booklist[serial].bookTittle()+ ","+self.booklist[serial].bookSerial()+","+ member.firstName() +" "+ member.lastName()+ "," + str(member.idNum())+ "\n")
            with open (self.borrowinglogpath, "a") as file:
                    file.write(data)
            
    
    def checkIn(self, serial, member):
        current_time = datetime.now()
        if serial not in self.booklist.keys():
            raise KeyError (f"Serial {serial} not found. Operation cancelled.")
        elif self.booklist[serial].bookStatus() == "Available":
            raise KeyError (f"Book is unassigned. Please review submission.")
        else:
            member.returnBook(self.booklist[serial])
            self.booklist[serial].setStatus("Available")
            data = (str(current_time)+ "," + "Checkin"+ ","+ self.booklist[serial].bookTittle()+ ","+self.booklist[serial].bookSerial()+","+ member.firstName() +" "+ member.lastName()+ ","+  str(member.idNum())+ "\n")
            with open (self.borrowinglogpath, "a") as file:
                file.write(data)
           
   """  def borrowingReport(self, reportday):
        with open(self.borrowinglogpath, 'r') as i:
            data = i.readlines()
        
        for log in data:
            if log[1] == "Checkout":
                
 """


        





                
        



           

    


            




    

    
oat = Inventory()
#oat.addBook(Book("The Golden  Apple", 2023, "Ed Boon"), [111111,222222,3333336])
oat.addBook(Book("Jumanji", 2022, "oat" ), ["111111", "555555"])
#oat.delRecords("Jumanji")
#oat.importBook("import.csv")
res = oat.booklist.keys()  
items = oat.booklist.values()

#serials = [i.bookSerial() for i in items]
print (res)
print (items)
query = oat.searchQuery("Jumanji")
print (query)
# for i in items:
#     status = i.status
#     print (status)
    #print (i.status())
#oat.editRecord("111111", newserial="11112222") 
#print (res)


