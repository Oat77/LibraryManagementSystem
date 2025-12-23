
# gui.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import lms_backend

# --- Initialize backend modules ---
membership = lms_backend.Membership()
inventory = lms_backend.Inventory()

# --- Main window setup ---
window = Tk()
window.title("Public Library Management System")
window.geometry("800x600")

# Background (optional)
try:
    bgimage = PhotoImage(file="library.png")
    bg_label = Label(window, image=bgimage)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bgimage  # prevent garbage collection
    bg_label.lower()
except Exception:
    pass

# Header
heading = Label(window,
                text="Public Library Management System",
                font=('Arial', 32, 'bold'),
                bg="#ffffff")
heading.pack(pady=20)

# --- Menubar ---
menubar = Menu(window)

# Membership menu
membership_menu = Menu(menubar, tearoff=0)
membership_menu.add_command(label="Register Member", command=lambda: open_register_member_window())
membership_menu.add_command(label="Update Member Status", command=lambda: open_update_member_status_window())
membership_menu.add_command(label="View Member (by ID)", command=lambda: open_view_member_window())
menubar.add_cascade(label="Membership", menu=membership_menu)

# Inventory menu
inventory_menu = Menu(menubar, tearoff=0)
inventory_menu.add_command(label="Add Book(s)", command=lambda: open_add_books_window())
inventory_menu.add_command(label="Import Inventory (CSV)", command=lambda: open_import_inventory_window())
inventory_menu.add_separator()
inventory_menu.add_command(label="Edit Record (by Serial)", command=lambda: open_edit_record_window())
inventory_menu.add_command(label="Delete Book (by Serial)", command=lambda: open_delete_book_window())
inventory_menu.add_command(label="Delete Records (by Title)", command=lambda: open_delete_records_window())
inventory_menu.add_separator()
inventory_menu.add_command(label="Search Title", command=lambda: open_search_title_window())
inventory_menu.add_command(label="Search Status", command=lambda: open_search_status_window())
menubar.add_cascade(label="Inventory", menu=inventory_menu)

# Rentals menu
rentals_menu = Menu(menubar, tearoff=0)
rentals_menu.add_command(label="Checkout", command=lambda: open_checkout_window())
rentals_menu.add_command(label="Checkin", command=lambda: open_checkin_window())
menubar.add_cascade(label="Rentals", menu=rentals_menu)

# Reports menu
reports_menu = Menu(menubar, tearoff=0)
reports_menu.add_command(label="Borrowing Log Viewer", command=lambda: open_borrowing_log_window())
menubar.add_cascade(label="Reports", menu=reports_menu)

# Help menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: open_about_window())
menubar.add_cascade(label="Help", menu=help_menu)

window.config(menu=menubar)

# --- Quick action buttons ---
button_frame = Frame(window, bg="#A58C88")
button_frame.pack(pady=40)

Button(button_frame, text="Membership Management", font=("Arial", 26),
       command=lambda: open_membership_home()).pack(padx=10, pady=10)
Button(button_frame, text="Inventory Management", font=("Arial", 26),
       command=lambda: open_inventory_home()).pack(padx=10, pady=10)
Button(button_frame, text="Rental Hub", font=("Arial", 26),
       command=lambda: open_rentals_home()).pack(padx=10, pady=10)


# ===========================
# WINDOWS & HANDLERS
# ===========================

def open_membership_home():
    win = Toplevel(window); win.title("Membership"); win.geometry("600x400"); win.transient(window)
    Label(win, text="Membership Management", font=("Arial", 20, "bold")).pack(pady=15)
    Button(win, text="Register Member", font=("Arial", 14), command=open_register_member_window).pack(pady=8)
    Button(win, text="Update Member Status", font=("Arial", 14), command=open_update_member_status_window).pack(pady=8)
    Button(win, text="View Member (by ID)", font=("Arial", 14), command=open_view_member_window).pack(pady=8)
    Button(win, text="Close", command=win.destroy).pack(pady=15)


def open_inventory_home():
    win = Toplevel(window); win.title("Inventory"); win.geometry("700x500"); win.transient(window)
    Label(win, text="Inventory Management", font=("Arial", 20, "bold")).pack(pady=15)
    Button(win, text="Add Book(s)", font=("Arial", 14), command=open_add_books_window).pack(pady=8)
    Button(win, text="Import Inventory (CSV)", font=("Arial", 14), command=open_import_inventory_window).pack(pady=8)
    Button(win, text="Edit Record (by Serial)", font=("Arial", 14), command=open_edit_record_window).pack(pady=8)
    Button(win, text="Delete Book (by Serial)", font=("Arial", 14), command=open_delete_book_window).pack(pady=8)
    Button(win, text="Delete Records (by Title)", font=("Arial", 14), command=open_delete_records_window).pack(pady=8)
    Button(win, text="Search Title", font=("Arial", 14), command=open_search_title_window).pack(pady=8)
    Button(win, text="Search Status", font=("Arial", 14), command=open_search_status_window).pack(pady=8)
    Button(win, text="Close", command=win.destroy).pack(pady=15)


def open_rentals_home():
    win = Toplevel(window); win.title("Rentals"); win.geometry("700x480"); win.transient(window)
    Label(win, text="Rental Hub", font=("Arial", 20, "bold")).pack(pady=15)
    Button(win, text="Checkout", font=("Arial", 14), command=open_checkout_window).pack(pady=8)
    Button(win, text="Checkin", font=("Arial", 14), command=open_checkin_window).pack(pady=8)
    Button(win, text="Close", command=win.destroy).pack(pady=15)


# --- Membership sub-windows ---
def open_register_member_window():
    sub = Toplevel(window); sub.title("Register Member"); sub.geometry("420x300"); sub.transient(window)
    Label(sub, text="Register Member", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    fname_entry = Entry(frm)
    lname_entry = Entry(frm)
    id_entry = Entry(frm)

    Label(frm, text="First Name").grid(row=0, column=0, padx=6, pady=6, sticky="e"); fname_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="Last Name").grid(row=1, column=0, padx=6, pady=6, sticky="e"); lname_entry.grid(row=1, column=1, padx=6, pady=6)
    Label(frm, text="Member ID").grid(row=2, column=0, padx=6, pady=6, sticky="e"); id_entry.grid(row=2, column=1, padx=6, pady=6)

    def handle_save():
        fname = fname_entry.get().strip()
        lname = lname_entry.get().strip()
        mid = id_entry.get().strip()
        if not fname or not lname or not mid:
            messagebox.showerror("Error", "All fields are required.")
            return
        member = lms_backend.Member(fname, lname, mid)
        membership.registerMember(member)
        messagebox.showinfo("Success", f"Member {fname} {lname} (ID: {mid}) registered.")
        sub.destroy()

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Save", font=("Arial", 12), command=handle_save).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_update_member_status_window():
    sub = Toplevel(window); sub.title("Update Member Status"); sub.geometry("420x300"); sub.transient(window)
    Label(sub, text="Update Member Status", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    id_entry = Entry(frm)
    status_combo = ttk.Combobox(frm, values=["Active", "Suspended", "Inactive"], state="readonly")

    Label(frm, text="Member ID").grid(row=0, column=0, padx=6, pady=6, sticky="e"); id_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="New Status").grid(row=1, column=0, padx=6, pady=6, sticky="e"); status_combo.grid(row=1, column=1, padx=6, pady=6)

    def handle_update():
        mid = id_entry.get().strip()
        status = status_combo.get().strip()
        if not mid or not status:
            messagebox.showerror("Error", "Member ID and Status are required.")
            return
        try:
            membership.updateMember(mid, status)
            messagebox.showinfo("Success", f"Member {mid} status updated to {status}.")
            sub.destroy()
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Update", font=("Arial", 12), command=handle_update).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_view_member_window():
    sub = Toplevel(window); sub.title("View Member"); sub.geometry("480x360"); sub.transient(window)
    Label(sub, text="View Member", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    id_entry = Entry(frm)
    Label(frm, text="Member ID").grid(row=0, column=0, padx=6, pady=6, sticky="e"); id_entry.grid(row=0, column=1, padx=6, pady=6)

    display = Text(sub, height=10, width=50)
    display.pack(pady=8)

    def handle_find():
        mid = id_entry.get().strip()
        if not mid:
            messagebox.showerror("Error", "Member ID is required.")
            return
        member = membership.get(mid)
        display.delete("1.0", END)
        if not member:
            display.insert(END, f"Member ID {mid} not found.")
            return
        display.insert(END, f"Name: {member.firstName()} {member.lastName()}\n")
        display.insert(END, f"ID: {member.idNum()}\n")
        display.insert(END, f"Status: {member.memberStatus()}\n")
        display.insert(END, "Books:\n")
        if not member.books:
            display.insert(END, "  (none)\n")
        else:
            for book, due in member.books:
                display.insert(END, f"  {book.bookTitle()} ({book.bookSerial()}) - Due: {due}\n")

    Button(sub, text="Find", font=("Arial", 12), command=handle_find).pack(pady=8)
    Button(sub, text="Close", command=sub.destroy).pack(pady=10)


# --- Inventory sub-windows ---
def open_add_books_window():
    sub = Toplevel(window); sub.title("Add Book(s)"); sub.geometry("520x360"); sub.transient(window)
    Label(sub, text="Add Book(s)", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    title_entry = Entry(frm)
    year_entry = Entry(frm)
    author_entry = Entry(frm)
    serials_entry = Entry(frm, width=40)

    Label(frm, text="Title").grid(row=0, column=0, padx=6, pady=6, sticky="e"); title_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="Year").grid(row=1, column=0, padx=6, pady=6, sticky="e"); year_entry.grid(row=1, column=1, padx=6, pady=6)
    Label(frm, text="Author").grid(row=2, column=0, padx=6, pady=6, sticky="e"); author_entry.grid(row=2, column=1, padx=6, pady=6)
    Label(frm, text="Serials (comma-separated)").grid(row=3, column=0, padx=6, pady=6, sticky="e"); serials_entry.grid(row=3, column=1, padx=6, pady=6)

    def handle_add():
        title = title_entry.get().strip()
        year = year_entry.get().strip()
        author = author_entry.get().strip()
        raw_serials = serials_entry.get().strip()
        if not title or not year or not author or not raw_serials:
            messagebox.showerror("Error", "All fields are required.")
            return
        serials = [s.strip() for s in raw_serials.split(",") if s.strip()]
        try:
            book = lms_backend.Book(title, year, author)
            inventory.addBook(book, serials)
            messagebox.showinfo("Success", f"Added {len(serials)} copy(ies) of '{title}'.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Add", font=("Arial", 12), command=handle_add).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_import_inventory_window():
    sub = Toplevel(window); sub.title("Import Inventory (CSV)"); sub.geometry("520x220"); sub.transient(window)
    Label(sub, text="Import Inventory (CSV)", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    path_entry = Entry(frm, width=40)
    Label(frm, text="CSV File Path").grid(row=0, column=0, padx=6, pady=6, sticky="e"); path_entry.grid(row=0, column=1, padx=6, pady=6)

    def browse():
        fp = filedialog.askopenfilename(title="Select Inventory CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if fp:
            path_entry.delete(0, END)
            path_entry.insert(0, fp)

    def handle_import():
        fp = path_entry.get().strip()
        if not fp:
            messagebox.showerror("Error", "CSV File Path is required.")
            return
        try:
            inventory.importBook(fp)
            messagebox.showinfo("Success", "Inventory import completed.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Browse...", font=("Arial", 12), command=browse).grid(row=0, column=0, padx=6)
    Button(actions, text="Import", font=("Arial", 12), command=handle_import).grid(row=0, column=1, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=2, padx=6)


def open_edit_record_window():
    sub = Toplevel(window); sub.title("Edit Record (by Serial)"); sub.geometry("540x340"); sub.transient(window)
    Label(sub, text="Edit Record (by Serial)", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    cur_serial_entry = Entry(frm)
    new_serial_entry = Entry(frm)
    new_title_entry = Entry(frm)
    new_year_entry = Entry(frm)
    new_author_entry = Entry(frm)

    Label(frm, text="Current Serial").grid(row=0, column=0, padx=6, pady=6, sticky="e"); cur_serial_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="New Serial").grid(row=1, column=0, padx=6, pady=6, sticky="e"); new_serial_entry.grid(row=1, column=1, padx=6, pady=6)
    Label(frm, text="New Title").grid(row=2, column=0, padx=6, pady=6, sticky="e"); new_title_entry.grid(row=2, column=1, padx=6, pady=6)
    Label(frm, text="New Year").grid(row=3, column=0, padx=6, pady=6, sticky="e"); new_year_entry.grid(row=3, column=1, padx=6, pady=6)
    Label(frm, text="New Author").grid(row=4, column=0, padx=6, pady=6, sticky="e"); new_author_entry.grid(row=4, column=1, padx=6, pady=6)

    def handle_apply():
        cur_serial = cur_serial_entry.get().strip()
        new_serial = new_serial_entry.get().strip() or None
        new_title = new_title_entry.get().strip() or None
        new_year = new_year_entry.get().strip() or None
        new_author = new_author_entry.get().strip() or None
        if not cur_serial:
            messagebox.showerror("Error", "Current serial is required.")
            return
        try:
            inventory.editRecord(cur_serial, newserial=new_serial, newTitle=new_title, newyear=new_year, newauthor=new_author)
            messagebox.showinfo("Success", "Record updated.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Apply", font=("Arial", 12), command=handle_apply).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_delete_book_window():
    sub = Toplevel(window); sub.title("Delete Book (by Serial)"); sub.geometry("420x220"); sub.transient(window)
    Label(sub, text="Delete Book (by Serial)", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    serial_entry = Entry(frm)
    Label(frm, text="Serial").grid(row=0, column=0, padx=6, pady=6, sticky="e"); serial_entry.grid(row=0, column=1, padx=6, pady=6)

    def handle_delete():
        s = serial_entry.get().strip()
        if not s:
            messagebox.showerror("Error", "Serial is required.")
            return
        try:
            inventory.delBook(s)
            messagebox.showinfo("Success", f"Serial {s} deleted.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Delete", font=("Arial", 12), command=handle_delete).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_delete_records_window():
    sub = Toplevel(window); sub.title("Delete Records (by Title)"); sub.geometry("520x240"); sub.transient(window)
    Label(sub, text="Delete Records (by Title)", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    title_entry = Entry(frm, width=40)
    Label(frm, text="Title").grid(row=0, column=0, padx=6, pady=6, sticky="e"); title_entry.grid(row=0, column=1, padx=6, pady=6)

    def handle_delete():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return
        try:
            inventory.delRecords(title)
            messagebox.showinfo("Success", f"All records for '{title}' deleted.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Delete", font=("Arial", 12), command=handle_delete).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_search_title_window():
    sub = Toplevel(window); sub.title("Search Title"); sub.geometry("520x260"); sub.transient(window)
    Label(sub, text="Search Title", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    title_entry = Entry(frm, width=40)
    Label(frm, text="Title").grid(row=0, column=0, padx=6, pady=6, sticky="e"); title_entry.grid(row=0, column=1, padx=6, pady=6)

    output = Text(sub, height=8, width=50)
    output.pack(pady=8)

    def handle_search():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return
        result = inventory.titleSearchQuery(title)
        output.delete("1.0", END)
        output.insert(END, result)

    Button(sub, text="Search", font=("Arial", 12), command=handle_search).pack(pady=8)
    Button(sub, text="Close", command=sub.destroy).pack(pady=8)


def open_search_status_window():
    sub = Toplevel(window); sub.title("Search Status"); sub.geometry("520x260"); sub.transient(window)
    Label(sub, text="Search Status", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    status_combo = ttk.Combobox(frm, values=["Available", "Checked Out", "Reserved"], state="readonly")
    Label(frm, text="Status").grid(row=0, column=0, padx=6, pady=6, sticky="e"); status_combo.grid(row=0, column=1, padx=6, pady=6)

    output = Text(sub, height=8, width=50)
    output.pack(pady=8)

    def handle_search():
        status = status_combo.get().strip()
        if not status:
            messagebox.showerror("Error", "Please select a status.")
            return
        result = inventory.statusSearchQuery(status)
        output.delete("1.0", END)
        output.insert(END, result)

    Button(sub, text="Search", font=("Arial", 12), command=handle_search).pack(pady=8)
    Button(sub, text="Close", command=sub.destroy).pack(pady=8)


# --- Rentals sub-windows ---
def open_checkout_window():
    sub = Toplevel(window); sub.title("Checkout"); sub.geometry("560x360"); sub.transient(window)
    Label(sub, text="Checkout", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    serial_entry = Entry(frm)
    fname_entry = Entry(frm)
    lname_entry = Entry(frm)
    id_entry = Entry(frm)
    due_entry = Entry(frm)

    Label(frm, text="Serial").grid(row=0, column=0, padx=6, pady=6, sticky="e"); serial_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="Member First Name").grid(row=1, column=0, padx=6, pady=6, sticky="e"); fname_entry.grid(row=1, column=1, padx=6, pady=6)
    Label(frm, text="Member Last Name").grid(row=2, column=0, padx=6, pady=6, sticky="e"); lname_entry.grid(row=2, column=1, padx=6, pady=6)
    Label(frm, text="Member ID").grid(row=3, column=0, padx=6, pady=6, sticky="e"); id_entry.grid(row=3, column=1, padx=6, pady=6)
    Label(frm, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0, padx=6, pady=6, sticky="e"); due_entry.grid(row=4, column=1, padx=6, pady=6)

    def handle_checkout():
        serial = serial_entry.get().strip()
        fname = fname_entry.get().strip()
        lname = lname_entry.get().strip()
        mid = id_entry.get().strip()
        due = due_entry.get().strip()

        if not serial or not fname or not lname or not mid or not due:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Get or create member
        member = membership.get(mid)
        if not member:
            member = lms_backend.Member(fname, lname, mid)
            membership.registerMember(member)

        try:
            inventory.checkOut(serial, member, due)
            messagebox.showinfo("Success", f"Serial {serial} checked out to {fname} {lname} (ID: {mid}).")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Checkout", font=("Arial", 12), command=handle_checkout).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


def open_checkin_window():
    sub = Toplevel(window); sub.title("Checkin"); sub.geometry("520x300"); sub.transient(window)
    Label(sub, text="Checkin", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    serial_entry = Entry(frm)
    fname_entry = Entry(frm)
    lname_entry = Entry(frm)
    id_entry = Entry(frm)

    Label(frm, text="Serial").grid(row=0, column=0, padx=6, pady=6, sticky="e"); serial_entry.grid(row=0, column=1, padx=6, pady=6)
    Label(frm, text="Member First Name").grid(row=1, column=0, padx=6, pady=6, sticky="e"); fname_entry.grid(row=1, column=1, padx=6, pady=6)
    Label(frm, text="Member Last Name").grid(row=2, column=0, padx=6, pady=6, sticky="e"); lname_entry.grid(row=2, column=1, padx=6, pady=6)
    Label(frm, text="Member ID").grid(row=3, column=0, padx=6, pady=6, sticky="e"); id_entry.grid(row=3, column=1, padx=6, pady=6)

    def handle_checkin():
        serial = serial_entry.get().strip()
        fname = fname_entry.get().strip()
        lname = lname_entry.get().strip()
        mid = id_entry.get().strip()

        if not serial or not fname or not lname or not mid:
            messagebox.showerror("Error", "All fields are required.")
            return

        member = membership.get(mid)
        if not member:
            messagebox.showerror("Error", f"Member ID {mid} not found.")
            return

        try:
            inventory.checkIn(serial, member)
            messagebox.showinfo("Success", f"Serial {serial} checked in from {fname} {lname} (ID: {mid}).")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Checkin", font=("Arial", 12), command=handle_checkin).grid(row=0, column=0, padx=6)
    Button(actions, text="Cancel", font=("Arial", 12), command=sub.destroy).grid(row=0, column=1, padx=6)


# --- Reports ---
def open_borrowing_log_window():
    sub = Toplevel(window); sub.title("Borrowing Log"); sub.geometry("720x460"); sub.transient(window)
    Label(sub, text="Borrowing Log Viewer", font=("Arial", 16, "bold")).pack(pady=10)

    frm = Frame(sub); frm.pack(pady=10)
    path_entry = Entry(frm, width=50)
    path_entry.insert(0, inventory.borrowinglogpath)
    Label(frm, text="Log File Path").grid(row=0, column=0, padx=6, pady=6, sticky="e"); path_entry.grid(row=0, column=1, padx=6, pady=6)

    output = Text(sub, height=18, width=80)
    output.pack(pady=8)

    def browse():
        fp = filedialog.askopenfilename(title="Select Borrowing Log", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if fp:
            path_entry.delete(0, END)
            path_entry.insert(0, fp)

    def handle_load():
        fp = path_entry.get().strip()
        if not fp:
            messagebox.showerror("Error", "Log File Path is required.")
            return
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            output.delete("1.0", END)
            output.insert(END, content if content else "(empty)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    actions = Frame(sub); actions.pack(pady=10)
    Button(actions, text="Browse...", font=("Arial", 12), command=browse).grid(row=0, column=0, padx=6)
    Button(actions, text="Load", font=("Arial", 12), command=handle_load).grid(row=0, column=1, padx=6)
    Button(actions, text="Close", command=sub.destroy).grid(row=0, column=2, padx=6)


# --- Help ---
def open_about_window():
    sub = Toplevel(window); sub.title("About"); sub.geometry("480x260"); sub.transient(window)
    Label(sub, text="About", font=("Arial", 18, "bold")).pack(pady=10)
    Label(sub, text="Public Library Management System\nTkinter GUI linked to backend (lms.py).",
          font=("Arial", 12)).pack(pady=10)
    Button(sub, text="Close", command=sub.destroy).pack(pady=10)


# Run app
if __name__ == "__main__":
    window.mainloop()
