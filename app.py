from datetime import date, datetime

from flask import Flask
from flask import send_file, render_template, request

from advance_form import AdvanceForm, to_decimal, round_decimal


DOCX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True # FIXME

@app.route("/", methods=['GET'])
def ui():
    return render_template('index.html')

@app.route("/api/advance_form", methods=['POST'])
def renter_advance_form():
  form_data = request.get_json()
  hotel_cost = round_decimal(to_decimal(form_data['hotel_cost']) * int(form_data['hotel_nights']))

  def convert_date(date_txt):
    return datetime.strptime(date_txt, '%Y-%m-%d').date()

  form = AdvanceForm(
    full_name=form_data['full_name'],
    phone_number=form_data['phone_num'],
    trip_purpose=form_data['trip_purpose'],
    departure_date=convert_date(form_data['dep_date']),
    return_date=convert_date(form_data['ret_date']),
    travel_city=form_data['travel_city'],
    accom_amt=hotel_cost,
    rental_amt=form_data['rental_amount'],
    transport_amt=form_data['transport_amount'],
    num_breakfast=form_data['num_breakfasts'],
    num_lunch=form_data['num_lunches'],
    num_dinner=form_data['num_dinners'],
    num_incidental=form_data['num_incidentals'],
  )
  
  rendered_form = form.render()
  return send_file(rendered_form, attachment_filename="advance.docx", mimetype=DOCX_MIMETYPE)
