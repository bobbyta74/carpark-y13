#Mr Cressey's car park
import flask, sqlite3, time

#Startup - create 
def initialise_db():
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
    connection.close()
initialise_db()

app = flask.Flask(__name__)

@app.route("/")
def front():
    return flask.redirect("/static/park.html")

@app.route("/park", methods = [ "GET" ])
def park():
    connection = sqlite3.connect("carpark.db")
    cursor = connection.cursor()

    reg = flask.request.args.get("reg")
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
        return {
            "reg" : reg,
            "type" : "entry",
            "time" : entry
        }
    else:
        #Find the time difference between now and entry time
        timedelta = time.time() - result[0]
        cursor.execute("""
            DELETE FROM cars WHERE reg = ?
        """, [ reg ])
        connection.commit()
        return {
            "reg" : reg,
            "type" : "exit",
            "duration" : timedelta
        }

    connection.close()