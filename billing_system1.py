from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
def initialize_db():
    conn = sqlite3.connect('billing_system.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

initialize_db()

# Function to fetch all items from the SQLite database
def fetch_items():
    conn = sqlite3.connect('billing_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    rows = c.fetchall()
    conn.close()
    return rows

# Function to remove an item from the SQLite database
def remove_item(item_id):
    conn = sqlite3.connect('billing_system.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Item removed successfully!")
    refresh_items()

# Function to add a new item to the SQLite database
def add_item(book_name, author, price):
    conn = sqlite3.connect('billing_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (book_name, author, price) VALUES (?, ?, ?)", (book_name, author, price))
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Item added successfully!")
    refresh_items()
    clear_add_update_fields()

# Function to update an existing item in the SQLite database
def update_item(item_id, book_name, author, price):
    conn = sqlite3.connect('billing_system.db')
    c = conn.cursor()
    c.execute("UPDATE items SET book_name=?, author=?, price=? WHERE id=?", (book_name, author, price, item_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Item updated successfully!")
    refresh_items()
    clear_add_update_fields()

# Function to refresh the item table in the GUI
def refresh_items():
    for row in item_table.get_children():
        item_table.delete(row)
    items = fetch_items()
    for item in items:
        item_table.insert('', 'end', values=(item[0], item[1], item[2], item[3]))

# Function to handle the "Order Now" button click
def order_now():
    messagebox.showinfo("Info", "Order placed successfully!")



# Create the main window
root = Tk()
root.title("Billing System")
root.geometry("1000x600")
root.iconbitmap('login.ico')


# Frame for the selected item
frame_selected = Frame(root, width=200, bg='lightblue')
frame_selected.place(x=10, y=20, width=450, height=500)

Label(frame_selected, text="Your Selected Item", bg = "lightblue", fg = "black", font = 'arial 20 bold').place(x=150, y=9)

# Define columns for the Treeview
columns = ('id', 'Book Name', 'Author', 'Price')

# Create the Treeview widget with reduced column widths
item_table = ttk.Treeview(frame_selected, columns=columns, show='headings')
item_table.heading('id', text='ID')
item_table.heading('Book Name', text='Book Name')
item_table.heading('Author', text='Author')
item_table.heading('Price', text='Price')

item_table.column('id', width=30)
item_table.column('Book Name', width=150)
item_table.column('Author', width=120)
item_table.column('Price', width=80)

item_table.place(x=10, y=40, width=430, height=400)

# Populate the Treeview with initial data
refresh_items()

# Function to handle the "Remove" button click
def on_remove_button_click():
    selected_item = item_table.selection()
    if selected_item:
        item_id = item_table.item(selected_item)['values'][0]
        remove_item(item_id)
    else:
        messagebox.showwarning("Warning", "Please select an item to remove.")

remove_button = Button(frame_selected, text="Remove", font = 'arial 10 bold',  bg = "dark blue", fg = "white",command=on_remove_button_click)
remove_button.place(x=170, y=450)


# Frame for the order details
frame_order = Frame(root, width=200, bg='lightblue')
frame_order.place(x=500, y=20, width=450, height=500)

Label(frame_order, text="Your Details for Order", font = 'arial 20 bold', bg = 'lightblue', fg = "black").place(x=10, y=0)



# Create entry fields for user details
Label(frame_order, text="Name", bg = 'lightblue',font = 'arial 10 bold').place(x=10, y=50)
entry_name = Entry(frame_order)
entry_name.place(x=10, y=70, width=200)



Label(frame_order, text="Email", font = 'arial 10 bold', bg = 'lightblue').place(x=220, y=50)
entry_email = Entry(frame_order)
entry_email.place(x=220, y=70, width=200)

Label(frame_order, text="Phone Number", font = 'arial 10 bold', bg = 'lightblue').place(x=10, y=100)
entry_phone = Entry(frame_order)
entry_phone.place(x=10, y=120, width=200)

Label(frame_order, text="Address", font = 'arial 10 bold', bg = 'lightblue').place(x=220, y=100)
entry_address = Entry(frame_order)
entry_address.place(x=220, y=120, width=200)


Label(frame_order, text="Landmark", font = 'arial 10 bold', bg = 'lightblue').place(x=10, y=150)
entry_landmark = Entry(frame_order)
entry_landmark.place(x=10, y=175, width=200)


Label(frame_order, text="City", font = 'arial 10 bold', bg = 'lightblue').place(x=220, y=150)
entry_city = Entry(frame_order)
entry_city.place(x=220, y=175, width=200)


Label(frame_order, text="State", font = 'arial 10 bold', bg = 'lightblue').place(x=10, y=200)
entry_state = Entry(frame_order)
entry_state.place(x=10, y=220, width=200)

Label(frame_order, text="Pin code", font = 'arial 10 bold', bg = 'lightblue').place(x=220, y=200)
entry_pincode = Entry(frame_order)
entry_pincode.place(x=220, y=220, width=200)


Label(frame_order, text="Payment Mode", font = 'arial 15 bold', bg = 'lightblue').place(x=10, y=260)
payment_mode = StringVar(value="Select")
payment_option = OptionMenu(frame_order, payment_mode, "Cash", "Card", "UPI")
payment_option.place(x=200, y=260, width=200)

order_button = Button(frame_order, text="Order Now", font = 'arial 12 bold', command=order_now)
order_button.place(x=250, y=320)


# Frame for adding/updating items
frame_add_update = Frame(root, bg="lightblue")
frame_add_update.place(x=10, y=530, width=940, height=60)

Label(frame_add_update, text="Add Item\n update items ", bg = "lightblue", font = 'arial 10 bold').place(x=10, y=10)

Label(frame_add_update, text="Book Name", bg = "lightblue", font = 'arial 10 bold').place(x=100, y=10)
entry_add_book_name = Entry(frame_add_update)
entry_add_book_name.place(x=180, y=10, width=150)

Label(frame_add_update, text="Author", bg = "lightblue", font = 'arial 10 bold').place(x=340, y=10)
entry_add_author = Entry(frame_add_update)
entry_add_author.place(x=400, y=10, width=150)

Label(frame_add_update, text="Price", bg = "lightblue", font = 'arial 10 bold').place(x=560, y=10)
entry_add_price = Entry(frame_add_update)
entry_add_price.place(x=620, y=10, width=80)

def clear_add_update_fields():
    entry_add_book_name.delete(0, END)
    entry_add_author.delete(0, END)
    entry_add_price.delete(0, END)

def on_add_button_click():
    book_name = entry_add_book_name.get()
    author = entry_add_author.get()
    price = entry_add_price.get()
    if book_name and author and price:
        try:
            price = float(price)
            add_item(book_name, author, price)
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid price.")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

add_button = Button(frame_add_update, text="Add Item", font = 'arial 10 bold', command=on_add_button_click)
add_button.place(x=710, y=10)

def on_update_button_click():
    selected_item = item_table.selection()
    if selected_item:
        item_id = item_table.item(selected_item)['values'][0]
        book_name = entry_add_book_name.get()
        author = entry_add_author.get()
        price = entry_add_price.get()
        if book_name and author and price:
            try:
                price = float(price)
                update_item(item_id, book_name, author, price)
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid price.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")
    else:
        messagebox.showwarning("Warning", "Please select an item to update.")

update_button = Button(frame_add_update, text="Update Item", font = 'arial 10 bold', command=on_update_button_click)
update_button.place(x=780, y=10)

# Run the application
root.mainloop()