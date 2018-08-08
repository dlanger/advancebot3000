from advance_form import AdvanceForm
from datetime import date

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

with open('newfoo.docx', 'w') as f:
    f.write(rendered_form.getvalue()) 
