import mysql.connector


def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="upload_directory",
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()

    return db, cursor
