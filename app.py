from datetime import date, datetime
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import boto3
from flask import Flask
from flask import send_file, render_template, request
from raven.contrib.flask import Sentry

import settings
from advance_form import AdvanceForm, to_decimal, round_decimal
from email_template import message as email_template  

DOCX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

app = Flask(__name__)
app.config.from_object("settings")
sentry = None

if app.config['SENTRY_DSN']:
  sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

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
  filename = _generate_filename(form_data['travel_city'])

  if form_data['email_me'] == '1':
    recipient = _guess_email_address(form_data['full_name'])
    if recipient:
      _email_form(rendered_form, recipient, filename, form_data['travel_city'])

  return send_file(rendered_form, attachment_filename=filename, mimetype=DOCX_MIMETYPE)

def _generate_filename(travel_city):
  short_date = datetime.now().strftime("%Y-%m-%d")
  return "Advance {date} - {city}.docx".format(city=travel_city, date=short_date)

def _guess_email_address(full_name):
  possible_last_name = full_name.split(' ')[-1].lower()
  possible_emails = [e[1] for e in app.config['POSSIBLE_EMAIL_RECIPIENTS'] if possible_last_name in e[0].lower()]

  if len(possible_emails) != 1:
    if sentry:
      sentry.captureMessage("Unable to guess email address address for {0}".format(full_name))
    return None
  else:
    return possible_emails[0]

def _email_form(rendered_form, recipient_email, filename, travel_city):
  msg = MIMEMultipart()
  msg['Subject'] = "Advance Form for {0}".format(travel_city)
  msg['From'] = "Advancebot 3000 <advancebot@flat.af>"
  msg['To'] = recipient_email
  
  msg_body = MIMEText(email_template.format(city=travel_city))
  msg.attach(msg_body)

  attachment = MIMEApplication(rendered_form.read())
  attachment.add_header('Content-Disposition', 'attachment', filename=filename)
  attachment.add_header('Content-Type', DOCX_MIMETYPE)
  msg.attach(attachment)
  rendered_form.seek(0)

  resp = boto3.client('ses', region_name='us-east-1').send_raw_email(
    RawMessage={'Data': msg.as_string()},
    Source=msg['From'],
    Destinations=(msg['To'],),
  )   