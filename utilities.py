import random
import string
import database
from flask import request
from datetime import datetime, timedelta


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits

    return "".join(random.choice(letters_and_digits) for i in range(length))


def get_user_ip():
    return request.remote_addr


def get_date_time_now():
    now = datetime.now() + timedelta(minutes=10)
    return now.strftime('%Y-%m-%d %H:%M')


def get_filename_from_gen_link(gen_link):
    db, cursor = database.get_db()

    cursor.execute("SELECT filename FROM upload WHERE gen_link = %s", (gen_link,))
    result = cursor.fetchall()
    print("XXXXX - RESULT: ", result[0][0])

    return str(result[0][0])
