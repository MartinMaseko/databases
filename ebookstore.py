import sqlite3

ebook_db = sqlite3.connect('ebookstore_database.db') # Connect to database

cursor = ebook_db.cursor() # Get cursor()


# Execute cursor to create table if it does not exist.
cursor.execute(
        '''CREATE TABLE IF NOT EXISTS book(
            id INTEGER, title TEXT, author TEXT, qty INTEGER)'''
    )
    
ebook_db.commit()

# Execute cursor to count the values in the table.
cursor.execute('''SELECT COUNT(*) FROM book''')

count = cursor.fetchone()[0] 

# Populate table with values.
# If Else statement to check if table has values already to handle 
# duplicate errors. 
if count == 0:

    cursor.execute('''INSERT INTO book (id, title, author, qty)
                   VALUES(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                   (3002, 'Harry Potter and the Philosophers Stone', 
                   'J.K. Rowling', 40),
                   (3003, 'The Lion the Witch and the Wardrobe', 'C. S. Lewis',
                   25),
                   (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                   (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)''')
            
    ebook_db.commit()
    
    print("Values added successfully!\n")
else:
    
    print("Values Already Exist.\n")

# Create a function 'add_newbook' that creates variables to be passed 
# as parameters in cursor.
# Function uses a try-except to handle value errors.
# Cursor executes a INSERT INTO function and adds input variables as 
# parameters.
# Cursor is used again to find the new book id and display to the user 
# the new recorded book using the input variable 'book_id'.  
def add_newbook():
    
    """Create variables within function and pass them as parameters in
    cursor execution to insert new book."""
    
    try:
        book_id = int(input("Please enter the number of book id: "))
        
    except ValueError as error:
        print("invalid input!. Try again & Enter a number.\n")
        exit()
    
    title = input("Please enter the title of the book: ").capitalize()
    
    author = input("Please enter the author: ").capitalize()
    
    try:
        qty = int(input("Please enter the book quantity: "))
        
    except ValueError as error:
        print("invalid input!. Try again & Enter a number.\n")
        exit()
    
    cursor.execute('''INSERT INTO book (id, title, author, qty)
                   VALUES(?,?,?,?)''',(book_id,title,author,qty))
    
    cursor.execute('''SELECT * FROM book WHERE id = ?''', (book_id,))
        
    updated_book = cursor.fetchone()
        
    print(f"You Successfully added:\n{updated_book}")
    
    ebook_db.commit()

# User is asked to enter the book id to be updated.
# Cursor first checks to see if the book id exists before asking for 
# other input variables.
# If-else statement is used to handle update error if the book does not exist.
# In the event the book exists the user is prompted for more variables 
# which are then passed as parameters in the cursor execution.
def update_book():
    
    """Function checks if book id exists, if it does the function
    allows user to enter new values and passes them into cursor to
    update values."""
    
    try:
        book_id = int(input("Please enter the id of the book to update: "))
        
    except ValueError as error:
        print("invalid input!. Try again & Enter a number.\n")
        exit()
        
    cursor.execute(
        '''SELECT EXISTS (SELECT id FROM book WHERE id = ?)''',(book_id,)
    )
    book_update = cursor.fetchone()[0]
    
    if book_update == 1:
    
        title = input("Please enter the title update of the book: ").capitalize()
        
        author = input("Please enter the update name of author: ").capitalize()
        
        try:
            qty = int(input("Please confirm the update book quantity: "))
            
        except ValueError as error:
            print("invalid input!. Try again & Enter a number.\n")
            exit()
        
        cursor.execute(
        '''UPDATE book SET title = ?, author = ?, qty = ? WHERE id = ? ''',
        (title,author,qty,book_id))
        
        ebook_db.commit()
        
        cursor.execute('''SELECT * FROM book WHERE id = ?''', (book_id,))
        
        updated_book = cursor.fetchone()
        
        print(f"You Successfully Updated:\n {updated_book}")
        
    elif book_update == 0:
        print("Sorry, There is no book with the id number entered")  

# Delete book function deletes the book with the matching 
# input variable 'book_id'.
# The function will first ensure the book exists using a counter 
# 'search_result'.
# An if statement is used to handle the event of the book not existing 
# and if the books exists, the variable is passed into the cursor to 
# delete the book with the matching id.
def delete_book():

    """Function checks if book id exists, if it does the function
    deletes the value using the input variable as a parameter in
    the cursor."""
    
    try:
        book_id = int(input("Please enter the id of the book to delete: "))
            
    except ValueError as error:
        print("invalid input!. Try again & Enter a number.")
        exit()
        
    cursor.execute(
        '''SELECT EXISTS (SELECT id FROM book WHERE id = ?)''',(book_id,)
    )
    
    search_result = cursor.fetchone()[0]
        
    if search_result == 1:
        
        cursor.execute('''DELETE FROM book WHERE id = ?''', (book_id,))
    
        ebook_db.commit()
        
    elif search_result == 0:
        print("Sorry, The book does not exist! ")

# Search_book function asks user for the 'title' of the book.
# a try-except block is used to pass variables into the cursor 
# if the book exists and prints out the searched book.
# If the book does not exist, a print message notifies the user
# the book does not exist in the database. 
def search_book():
    
    """Function checks the title exists in the table,if it does
    a print out of the searched book will display."""
    
    title = input("Please enter the title of the book: ")
    
    try:
        cursor.execute(
            '''SELECT * FROM book WHERE title = ?''', (title,)
        )
        search_result = cursor.fetchone()
    
        print(*search_result)
        
    except TypeError as error:
        print("Sorry, There is no book with that title!")
        exit()

# Cursor is used to select all fields
# A variable that stores all the values if created
# A for loop is used to print out each value.
def display_books(): 
    
    """Function displays all the values in the table."""
      
    cursor.execute('''SELECT id, title, author, qty FROM book''')

    data = cursor.fetchall() # Store data in variable 'data'

    print("\nBook table")
    for row in data: # Print Table Data for user
        print(*row)

while True:
    
    print(
        "Welcome to your ebookstore database application!\n"
    )
    
    menu = input('''Select one of the following options:
a - Enter new book
u - Update book
d - Delete book
s - Search books
ds - Display books    
e - exit             
: ''').lower()
    
    if menu == 'a':
        
        add_newbook()
    
    elif menu == 'u':
        
        update_book()
        
    elif menu == 'd':
        
        delete_book()
        
    elif menu == 's':
        
        search_book()
    
    elif menu == 'ds':
        
        display_books()
        
    elif menu == 'e':
        
        print("Thank you for using the application. Goodbye! ")
        exit()
        
    else:
        print("invalid input. Please try again")
