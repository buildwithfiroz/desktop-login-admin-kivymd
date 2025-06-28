# # # #for data we will use sqlite3

import sqlite3

# #insert the data base
conn = sqlite3.connect("user.db")


# #Now we have to createa cursor to excute sql quires
cursor = conn.cursor()

# #Now lets create a table


# This is use to create a database
cursor.execute("""
               CREATE TABLE IF NOT EXISTS user_info (  
                   id INTEGER PRIMARY KEY,
                   user_photo LONGBLOB null,
                   username  TEXT,
                   user_pass TEXT,
                   Date_user DATE,
                   Time_user TIME

                   
                   
               )
               """)

# # # #The first cmd wll check if we have the data base if not it will create one
# # # # will add the primary key
# # # # Will add the user
# # # # will add the pass and we have use text which can hold the storage up to 2.1 gigabyte

# # # now lets create a function which will load the img

# def read_img(file_path):
#     with open(file_path , 'rb') as f:
#         photo_data = f.read()

#     return photo_data

# from datetime import datetime
# # now lets add the information
# username = 'Firoz'
# password = 'Takeme@in'

# path = 'pic.png'
# pic = read_img(path)
# current_date = datetime.now().date()

# # Get current time
# current_time= datetime.now().strftime("%I:%M:%S %p")

# #Now we have to insert inside the database
# cursor.execute('INSERT INTO user_info (username, user_photo, user_pass, Date_user, Time_user) VALUES (?, ?, ?, ?, ?)', (username, pic, password, current_date, current_time))
# # # commit the transaction
# conn.commit()

# #now close the connection
# conn.close()


# #below are use to delete the things


# # import sqlite3

# # conn = sqlite3.connect('user.db')
# # cursor = conn.cursor()


# This is use to delete the things
# # # Delete rows from index 3 to the end
# cursor.execute('DELETE FROM user_info ')
# cursor.execute('DROP TABLE user_login')


# This is use to edit the table
# cursor.execute('ALTER TABLE user_login ADD COLUMN log_out TIME')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()


#  # Establish database connection
# conn = sqlite3.connect('user.db')
# cursor = conn.cursor()

# # # Execute query to get count of users
# # cursor.execute("SELECT COUNT(*) FROM user_info")
# # result = cursor.fetchone()[0]  # Fetch the first column of the first row (the count)


# cursor.execute("SELECT username FROM user_info")
# users_data = cursor.fetchall()

# for i in users_data:
#     print(i[0])
# # Close the database connection
# conn.close()
