import database
import mysql.connector


class Upload:
    def __init__(self, user_ip: object, filename: object, gen_link: object, date_created: object,
                 date_explode: object) -> object:
        self.user_ip = user_ip
        self.filename = filename
        self.gen_link = gen_link
        self.date_created = date_created
        self.date_explode = date_explode

    def save_upload_to_db(self):
        # print(self.__dict__)
        db, cursor = database.get_db()

        try:
            cursor.execute(
                "INSERT INTO upload (user_ip, filename, gen_link, date_created, date_explode) VALUES(%s, %s, %s, %s, %s)",
                (self.user_ip, self.filename, self.gen_link, self.date_created, self.date_explode))
            db.commit()
        except mysql.connector.Error as e:
            print(e)

        print("executed insert object")