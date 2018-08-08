from advance_form import render_advance_form

from flask import Flask
from flask import send_file

DOCX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
app = Flask(__name__)

@app.route("/")
def hello():
    return "hello from Flask"

@app.route("/t1")
def test_word():
  rendered_form = render_advance_form(
    full_name="james joyce"
    )
  return send_file(rendered_form, attachment_filename="advance.docx", mimetype=DOCX_MIMETYPE)
