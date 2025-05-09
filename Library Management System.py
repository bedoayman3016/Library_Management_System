import tkinter as tk
from tkinter import messagebox, simpledialog
import json

books = []

# Load and Save
def load_data_from_json():
    global books
    try:
        with open('library_data.json', 'r') as file:
            books = json.load(file)
    except FileNotFoundError:
        books = []

def save_data_to_json():
    with open('library_data.json', 'w') as file:
        json.dump(books, file, indent=4)

# Clear main content
def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Screens
def show_home():
    clear_frame()
    tk.Label(content_frame, text=f"Welcome {user_type}!", font=("Arial", 16)).pack(pady=20)

def show_all_books():
    clear_frame()
    tk.Label(content_frame, text="All Books", font=("Arial", 14)).pack(pady=10)

    if not books:
        tk.Label(content_frame, text="No books available.").pack()
        return

    text_box = tk.Text(content_frame, width=80, height=20)
    text_box.pack()

    for book in books:
        status = "Available" if book["available"] else f"Borrowed by {book['borrower']}, due {book['due_date']}"
        text_box.insert(tk.END, f"Title: {book['title']}\n")
        text_box.insert(tk.END, f"Author: {book['author']}\n")
        text_box.insert(tk.END, f"Year: {book['year']}\n")
        text_box.insert(tk.END, f"Status: {status}\n")
        text_box.insert(tk.END, "-" * 50 + "\n")


def show_add_book():
    clear_frame()
    tk.Label(content_frame, text="Add New Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Title").pack()
    title_entry = tk.Entry(content_frame)
    title_entry.pack()

    tk.Label(content_frame, text="Author").pack()
    author_entry = tk.Entry(content_frame)
    author_entry.pack()

    tk.Label(content_frame, text="Year").pack()
    year_entry = tk.Entry(content_frame)
    year_entry.pack()

    def add_book_action():
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()

        if title and author and year.isdigit():
            books.append({
                "title": title,
                "author": author,
                "year": int(year),
                "available": True,
                "borrower": None,
                "due_date": None
            })
            save_data_to_json()
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields correctly.")

    tk.Button(content_frame, text="Add Book", command=add_book_action).pack(pady=10)

def show_search_book():
    clear_frame()
    tk.Label(content_frame, text="Search Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Enter title or author:").pack()
    search_entry = tk.Entry(content_frame)
    search_entry.pack()

    result_box = tk.Text(content_frame, height=10, width=50)
    result_box.pack(pady=10)

    def search():
        query = search_entry.get().lower()
        result_box.delete("1.0", tk.END)
        found = False
        for book in books:
            if query in book["title"].lower() or query in book["author"].lower():
                result_box.insert(tk.END, f"{book['title']} by {book['author']} ({book['year']})\n")
                found = True
        if not found:
            result_box.insert(tk.END, "No books found.")

    tk.Button(content_frame, text="Search", command=search).pack(pady=5)

def show_borrow_book():
    clear_frame()
    tk.Label(content_frame, text="Borrow Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Title").pack()
    title_entry = tk.Entry(content_frame)
    title_entry.pack()

    tk.Label(content_frame, text="Borrower Name").pack()
    borrower_entry = tk.Entry(content_frame)
    borrower_entry.pack()

    tk.Label(content_frame, text="Due Date (DD/MM)").pack()
    due_entry = tk.Entry(content_frame)
    due_entry.pack()

    def borrow():
        title = title_entry.get()
        borrower = borrower_entry.get()
        due_date = due_entry.get()

        for book in books:
            if book["title"] == title:
                if book["available"]:
                    book["available"] = False
                    book["borrower"] = borrower
                    book["due_date"] = due_date
                    save_data_to_json()
                    messagebox.showinfo("Success", "Book borrowed.")
                    return
                else:
                    messagebox.showwarning("Unavailable", "Book already borrowed.")
                    return
        messagebox.showerror("Not Found", "Book not found.")

    tk.Button(content_frame, text="Borrow", command=borrow).pack(pady=5)

def show_return_book():
    clear_frame()
    tk.Label(content_frame, text="Return Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Title").pack()
    title_entry = tk.Entry(content_frame)
    title_entry.pack()

    def return_book():
        title = title_entry.get()
        for book in books:
            if book["title"] == title:
                if not book["available"]:
                    book["available"] = True
                    book["borrower"] = None
                    book["due_date"] = None
                    save_data_to_json()
                    messagebox.showinfo("Returned", "Book returned.")
                    return
                else:
                    messagebox.showwarning("Available", "Book was not borrowed.")
                    return
        messagebox.showerror("Not Found", "Book not found.")

    tk.Button(content_frame, text="Return", command=return_book).pack(pady=5)

def show_edit_book():
    if user_type != "Admin":
        messagebox.showerror("Permission Denied", "Only Admin can edit books.")
        return

    clear_frame()
    tk.Label(content_frame, text="Edit Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Enter title of book to edit:").pack()
    title_entry = tk.Entry(content_frame)
    title_entry.pack()

    def edit():
        title = title_entry.get().lower()
        for book in books:
            if book["title"].lower() == title:
                new_title = simpledialog.askstring("Edit", "New title (leave blank to keep):")
                new_author = simpledialog.askstring("Edit", "New author (leave blank to keep):")
                new_year = simpledialog.askstring("Edit", "New year (leave blank to keep):")

                if new_title:
                    book["title"] = new_title
                if new_author:
                    book["author"] = new_author
                if new_year and new_year.isdigit():
                    book["year"] = int(new_year)

                save_data_to_json()
                messagebox.showinfo("Updated", "Book info updated.")
                return
        messagebox.showerror("Not Found", "Book not found.")

    tk.Button(content_frame, text="Edit", command=edit).pack(pady=5)

def show_delete_book():
    if user_type != "Admin":
        messagebox.showerror("Permission Denied", "Only Admin can delete books.")
        return

    clear_frame()
    tk.Label(content_frame, text="Delete Book", font=("Arial", 14)).pack(pady=10)

    tk.Label(content_frame, text="Enter title to delete:").pack()
    title_entry = tk.Entry(content_frame)
    title_entry.pack()

    def delete():
        title = title_entry.get()
        for i, book in enumerate(books):
            if book["title"] == title:
                del books[i]
                save_data_to_json()
                messagebox.showinfo("Deleted", "Book deleted.")
                return
        messagebox.showerror("Not Found", "Book not found.")

    tk.Button(content_frame, text="Delete", command=delete).pack(pady=5)

# Navigation + Main setup
def show_main_screen():
    clear_frame()
    for widget in sidebar_frame.winfo_children():
        widget.destroy()

    tk.Button(sidebar_frame, text="Home", width=20, command=show_home).pack(pady=5)
    tk.Button(sidebar_frame, text="Show All Books", width=20, command=show_all_books).pack(pady=5)
    tk.Button(sidebar_frame, text="Add Book", width=20, command=show_add_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Search Book", width=20, command=show_search_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Borrow Book", width=20, command=show_borrow_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Return Book", width=20, command=show_return_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Edit Book", width=20, command=show_edit_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Delete Book", width=20, command=show_delete_book).pack(pady=5)
    tk.Button(sidebar_frame, text="Exit", width=20, command=root.quit).pack(pady=5)

    show_home()

def handle_admin_login():
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')

    if username == "admin" and password == "181222":
        global user_type
        user_type = "Admin"
        show_main_screen()
    else:
        messagebox.showerror("Error", "Invalid admin credentials.")

def start_as_user():
    global user_type
    user_type = "User"
    show_main_screen()

def show_start_screen():
    clear_frame()
    tk.Label(content_frame, text="Are you Admin or User?", font=("Arial", 14)).pack(pady=10)
    tk.Button(content_frame, text="Admin", width=15, command=handle_admin_login).pack(pady=5)
    tk.Button(content_frame, text="User", width=15, command=start_as_user).pack(pady=5)

# Main GUI setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x500")

sidebar_frame = tk.Frame(root, width=150, bg="#f0f0f0")
sidebar_frame.pack(side="left", fill="y")

content_frame = tk.Frame(root, bg="white")
content_frame.pack(side="right", expand=True, fill="both")

user_type = None
load_data_from_json()
show_start_screen()
root.mainloop()

