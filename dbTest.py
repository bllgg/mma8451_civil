import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")



conn.execute('''CREATE TABLE IF NOT EXISTS MMA4851
         (ID           INT     NOT NULL,
         X             INT    NOT NULL,
         Y             INT     NOT NULL,
         Z             INT NOT NULL,
        Batch_No       INT NOT NULL);''')
print ("Table created successfully")

conn.execute("INSERT INTO MMA4851 (ID, X, Y, Z,Batch_No) VALUES (?, ?, ?, ?,?)",
          (1,45,54, 54,45))


conn.commit()
print ("Records created successfully")
conn.close()