import sqlite3

#connect to sqllite
connection = sqlite3.connect('student.db')

# Create a cursor object using the connection
cursor = connection.cursor()

# Create a table
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

# Execute the table creation query
cursor.execute(table_info)

# Insert data into the table
cursor.execute("INSERT INTO STUDENT VALUES('Jeswin', 'Data Science', 'A', 85)")
cursor.execute("INSERT INTO STUDENT VALUES('John', 'Data Science', 'B', 90)")
cursor.execute("INSERT INTO STUDENT VALUES('Jane', 'Data Science', 'A', 95)")
cursor.execute("INSERT INTO STUDENT VALUES('Doe', 'Devops', 'B', 80)")
cursor.execute("INSERT INTO STUDENT VALUES('Alice', 'Devops', 'A', 88)")

#Display the data
print("Data in the STUDENT table:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# Commit the changes
connection.commit()
# Close the connection
connection.close()