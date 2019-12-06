import database
import os
import time
import utilities
from datetime import datetime

UPLOAD_FOLDER = "./uploads/"


# (15, '127.0.0.1', 'Employee.java', 'fj5fm3oGNyJXhiMgQVIw6bPrGXdRxO',
# datetime.datetime(2019, 12, 5, 20, 10), datetime.datetime(2019, 12, 5, 20, 10))


def scan_db():
    db, cursor = database.get_db()

    cursor.execute("SELECT * FROM upload")
    results = cursor.fetchall()

    if cursor.rowcount != 0:
        for r in results:
            id = r[0]
            fname = r[2]
            exp_time = r[5]
            if str(exp_time) < datetime.now().strftime('%Y-%m-%d %H:%M'):
                print("Deleting file: {0} - {1} - {2}".format(id, fname, exp_time))
                cursor.execute("DELETE FROM upload WHERE id = %s", (id,))
                db.commit()
                try:
                    os.remove(UPLOAD_FOLDER + fname)
                except IOError:
                    print("Could not delete {0}".format(fname))
    else:
        print("Database has no entries!")


while True:
    timenow = datetime.now().strftime('%Y-%m-%d %H:%M')
    print("Starting a new scan....at: " + timenow)
    scan_db()
    time.sleep(60)  # Waits for 1 minute before rescanning
    print("")
