from advance_form import AdvanceForm

from flask import Flask
from flask import send_file, render_template

from datetime import date


DOCX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods=['GET'])
def ui():
    return render_template('index.html')

@app.route("/api/advance_form", methods=['POST'])
def renter_advance_form():
  form = AdvanceForm(
    full_name='Dan Langer',
    phone_number='(416) 999 8888',
    trip_purpose="Advance and execute PM's visit to Latvia",
    departure_date=date(2018, 1, 1),
    return_date=date(2018, 3, 1),
    travel_city="Orlando",
    accom_amt="1800",
    num_lunch=4,
    num_dinner=2
  )
  
  rendered_form = form.render()
  return send_file(rendered_form, attachment_filename="advance.docx", mimetype=DOCX_MIMETYPE)
