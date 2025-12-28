
# lms.py
import copy
from datetime import datetime
import os


class Book:
    """Represents a single copy of a book in the library."""

    def __init__(self, title, year, author):
        self.title = title
        self.year = str(year)
        self.author = author
        self.serial = None
        self.status = None  # "Available", "Checked Out", "Reserved"z

    # Getters
    def bookTitle(self):
        return self.title

    def bookYear(self):
        return self.year

    def bookAuthor(self):
        return self.author

    def bookSerial(self):
        return self.serial

    def bookStatus(self):
        return self.status

    # Setters
    def setTitle(self, new_title):
        self.title = new_title

    def setYear(self, new_year):
        self.year = str(new_year)

    def setAuthor(self, new_author):
        self.author = new_author

    def setSerial(self, new_serial):
        self.serial = str(new_serial)

    def setStatus(self, new_status):
        self.status = new_status


class Member:
    """Represents a library member and their current checkouts."""

    def __init__(self, fname, lname, id):
        self.fname = fname
        self.lname = lname
        self.id = str(id)
        self.books = []  # list of [Book, duedate]
        self.status = "Active"

    #Getters
    def firstName(self):
        return self.fname

    def lastName(self):
        return self.lname

    def idNum(self):
        return self.id

    def memberStatus(self):
        return self.status

    #Setters
    def setFname(self, newname):
        self.fname = newname

    def setLname(self, newname):
        self.lname = newname

    def setStatus(self, nwstatus):
        self.status = nwstatus

    def registerBook(self, book, duedate):
        self.books.append([book, duedate])

    def returnBook(self, book):
        for booking in self.books:
            if booking[0] == book:
                self.books.remove(booking)
                break
        else:
            raise KeyError("Booking not found.")


class Inventory:
    """In-memory inventory with CSV persistence for books and borrowing log."""

    def __init__(self, inventory_path="inventory.csv", borrowing_log_path="borrowinglog.csv"):
        self.booklist = {}  # serial -> Book
        self.filepath = inventory_path
        self.borrowinglogpath = borrowing_log_path

        # Ensure files exist
        for p in (self.filepath, self.borrowinglogpath):
            if not os.path.exists(p):
                with open(p, "w", encoding="utf-8") as f:
                    # No header; use plain lines for simplicity
                    pass

    def addBook(self, newbook, serials=None):
        """Adds copies of a book given a list of serial numbers."""
        if not serials:
            raise ValueError("No serials provided. Operation cancelled.")
        duplicates = []
        for s in serials:
            s = str(s)
            if s in self.booklist:
                duplicates.append(s)
                continue
            book = copy.deepcopy(newbook)
            book.setSerial(s)
            book.setStatus("Available")
            self.booklist[s] = book

            # Append to inventory file
            data = f"{book.bookTitle()},{book.bookYear()},{book.bookAuthor()},{book.bookStatus()},{s}\n"
            with open(self.filepath, "a", encoding="utf-8") as file:
                file.write(data)

        print(f"Operation completed. {len(duplicates)} duplicates found and skipped.")

    def importBook(self, file):
        """
        Imports multiple books from a CSV.
        Expected format per line:
            title,year,author,status,serial1,serial2,serial3,...
        """
        total_duplicates = []

        with open(file, "r", encoding="utf-8") as i:
            lines = i.readlines()

        for line in lines:
            parts = [p.strip() for p in line.split(",") if p.strip() != ""]
            if len(parts) < 5:
                # Not enough fields; skip line
                continue

            title, year, author, status = parts[0], parts[1], parts[2], parts[3]
            serials = parts[4:]
            if not serials:
                continue

            # Filter duplicates
            duplicates = [s for s in serials if s in self.booklist]
            total_duplicates.extend(duplicates)
            serials = [s for s in serials if s not in self.booklist]

            # Create and add
            newbook = Book(title, year, author)
            self.addBook(newbook, serials)

            # Set status per imported status (overrides default Available)
            for s in serials:
                if s in self.booklist:
                    self.booklist[s].setStatus(status)

        print(f"Operation completed. {len(total_duplicates)} duplicates found and skipped.")

    def editRecord(self, serial, newserial=None, newTitle=None, newyear=None, newauthor=None):
        """Edits a single record by serial."""
        serial = str(serial)
        if serial not in self.booklist:
            raise KeyError(f"Serial number {serial} not found.")

        book = self.booklist[serial]
        if newTitle is not None and newTitle != "":
            book.setTitle(newTitle)
        if newyear is not None and newyear != "":
            book.setYear(newyear)
        if newauthor is not None and newauthor != "":
            book.setAuthor(newauthor)
        if newserial is not None and newserial != "":
            newserial = str(newserial)
            if newserial not in self.booklist or serial == newserial:
                # Move the key
                del self.booklist[serial]
                self.booklist[newserial] = book
                book.setSerial(newserial)
            else:
                raise KeyError("Invalid entry. Please verify data and try again.")

        # Rewrite inventory file after edit
        self._rewrite_inventory_file()

    def delBook(self, serial):
        """Deletes a single book by serial."""
        serial = str(serial)
        if serial not in self.booklist:
            raise KeyError(f"Serial number {serial} not found")
        del self.booklist[serial]
        self._rewrite_inventory_file()

    def delRecords(self, title):
        """Deletes all copies for a given title."""
        to_delete = [s for s, b in self.booklist.items() if b.bookTitle() == title]
        for s in to_delete:
            if s in self.booklist:
                del self.booklist[s]
        self._rewrite_inventory_file()

    def titleSearchQuery(self, title):
        """Returns count of available copies for a title."""
        available = [b for b in self.booklist.values() if b.bookTitle() == title and b.bookStatus() == "Available"]
        return f"{title}: {len(available)} available copies."

    def statusSearchQuery(self, status):
        """Returns a listing of all books with a given status."""
        results = [b for b in self.booklist.values() if b.bookStatus() == status]
        if not results:
            return f"{status} books: 0"
        return ", ".join(f"{b.bookTitle()} ({b.bookSerial()}) \n" for b in results)

    def bookListing(self):
        """Returns a list of (serial, title, status)."""
        return [(b.bookSerial(), b.bookTitle(), b.bookStatus()) for b in self.booklist.values()]

    def checkOut(self, serial, member, duedate):
        """Checks out a book to a member."""
        current_time = datetime.now()
        serial = str(serial)
        if serial not in self.booklist:
            raise KeyError(f"Serial {serial} not found. Operation cancelled.")
        status = self.booklist[serial].bookStatus()
        if status in ("Checked Out", "Reserved"):
            raise KeyError("Book is not available. Please choose another book.")

        self.booklist[serial].setStatus("Checked Out")
        member.registerBook(self.booklist[serial], duedate)
        data = (
            f"{current_time},Checkout,"
            f"{self.booklist[serial].bookTitle()},{self.booklist[serial].bookSerial()},"
            f"{member.firstName()} {member.lastName()},{member.idNum()}\n"
        )
        with open(self.borrowinglogpath, "a", encoding="utf-8") as file:
            file.write(data)

        # Update inventory persistence
        self._rewrite_inventory_file()

    def checkIn(self, serial, member):
        """Checks in a book from a member."""
        current_time = datetime.now()
        serial = str(serial)
        if serial not in self.booklist:
            raise KeyError(f"Serial {serial} not found. Operation cancelled.")
        if self.booklist[serial].bookStatus() == "Available":
            raise KeyError("Book is unassigned. Please review submission.")

        # Remove from member and mark available 
        member.returnBook(self.booklist[serial])
        self.booklist[serial].setStatus("Available")

        data = (
            f"{current_time},Checkin,"
            f"{self.booklist[serial].bookTitle()},{self.booklist[serial].bookSerial()},"
            f"{member.firstName()} {member.lastName()},{member.idNum()}\n"
        )
        with open(self.borrowinglogpath, "a", encoding="utf-8") as file:
            file.write(data)

        self._rewrite_inventory_file()

    def _rewrite_inventory_file(self):
        """Rewrites the inventory CSV from current in-memory state."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            for book in self.booklist.values():
                line = (
                    f"{book.bookTitle()},{book.bookYear()},{book.bookAuthor()},"
                    f"{book.bookStatus()},{book.bookSerial()}\n"
                )
                file.write(line)


class Membership:
    """Simple in-memory membership registry."""

    def __init__(self):
        self.memberdatabase = {}  # id -> Member

    def registerMember(self, nwmember):
        self.memberdatabase[nwmember.idNum()] = nwmember

    def updateMember(self, id, nwStatus):
        id = str(id)
        if id in self.memberdatabase:
            self.memberdatabase[id].setStatus(nwStatus)
        else:
            raise KeyError(f"ID {id} is not present in library registry.")

    def get(self, id):
        """Returns a Member by id or None."""
        return self.memberdatabase.get(str(id))
