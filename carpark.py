import sqlite3, time

connection = sqlite3.connect("carpark.db")
cursor = connection.cursor()

#Make table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        reg TEXT,
        entry REAL
    )
""")
connection.commit()

#Output entry time of record that matches inputted registration
reg = input("Enter registration: ")
result = cursor.execute("""
    SELECT entry FROM cars
    WHERE reg = ?
""", [ reg ]).fetchone()

if result is None:
    #Add a record if the car isn't in the database
    entry = time.time()
    cursor.execute("""
        INSERT INTO cars(reg, entry)
        VALUES (?, ?)
    """, [ reg, entry ])
    connection.commit()
    print(f"Entered car park at {entry}")
else:
    #Find the time difference between now and entry time
    timedelta = time.time() - result[0]
    print(f"You stayed {timedelta} seconds.")
    print("Goodbye!")
    cursor.execute("""
        DELETE FROM cars WHERE reg = ?
    """, [ reg ])
    connection.commit()

connection.close()