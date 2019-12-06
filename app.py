import os

from flask import Flask, flash, request, redirect, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
import Upload
from Upload import Upload
import utilities
from datetime import datetime, timedelta

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "java", "py", "jpg", "jpeg", "png", "gif"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            random_string = utilities.generate_random_string(30)
            # create upload object and save to db
            upload_obj = Upload(utilities.get_user_ip(), filename, random_string,
                                datetime.now().strftime('%Y-%m-%d %H:%M'), utilities.get_date_time_now())
            upload_obj.save_upload_to_db()
            print("saved")
            return "Your link is: " + random_string + "\n\n" + "Expires: " + utilities.get_date_time_now()

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/link/<gen_link>", methods=["GET"])
def download_file(gen_link):
    results = utilities.get_filename_from_gen_link(gen_link)
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=results, as_attachment=True)
    except FileNotFoundError:
        #abort(404)
        return "no file dumdum"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/upload")
def render_upload():
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
