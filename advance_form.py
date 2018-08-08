import io
from datetime import date
from decimal import Decimal

import attr
from mailmerge import MailMerge

WORD_TEMPLATE = 'template.travel-advance.docx' 

# Per PCO guidelines
PERCENTAGE_TO_CLAIM = Decimal('0.8')

# https://www.njc-cnm.gc.ca/directive/d10/v238/s659/en
# Effective Date: April 1, 2018
PD_BREAKFAST = Decimal("19.45")
PD_LUNCH = Decimal("19.20")
PD_DINNER = Decimal("48.15")
PD_INCIDENTAL = Decimal("17.30")

@attr.s
class AdvanceForm(object):
    full_name = attr.ib()
    phone_number = attr.ib()
    trip_purpose = attr.ib()
    departure_date = attr.ib(validator=attr.validators.instance_of(date))
    return_date = attr.ib(validator=attr.validators.instance_of(date))
    travel_city = attr.ib()
    accom_amt = attr.ib(default=0, converter=Decimal)
    rental_amt = attr.ib(default=0, converter=Decimal)
    num_breakfast = attr.ib(default=0, validator=attr.validators.instance_of(int))
    num_lunch = attr.ib(default=0, validator=attr.validators.instance_of(int))
    num_dinner = attr.ib(default=0, validator=attr.validators.instance_of(int))
    num_incidental = attr.ib(default=0, validator=attr.validators.instance_of(int))
    transport_amt = attr.ib(default=Decimal(0), converter=Decimal)
    date_submitted = attr.ib(default=attr.Factory(lambda: date.today()), validator=attr.validators.instance_of(date))

    @property
    def total_amt(self):
        amount = sum((self.accom_amt, self.rental_amt, self.meals_amt, self.transport_amt)) 
        return self._round_decimal(amount)

    @property
    def claimed_amt(self):
        return self._round_decimal(PERCENTAGE_TO_CLAIM * self.total_amt)
    
    @property
    def meals_amt(self):
        return sum(map(self._round_decimal, (
            self.num_breakfast * PD_BREAKFAST,
            self.num_lunch * PD_LUNCH,
            self.num_dinner * PD_DINNER,
            self.num_incidental * PD_INCIDENTAL
        )))

    def _round_decimal(self, number):
        return number.quantize(Decimal('0.01'))

    def render(self):
        template_vals = {
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'purpose': self.trip_purpose,
            'dep_date': self.departure_date.strftime("%-d-%b"),
            'ret_date': self.return_date.strftime("%-d-%b"),
            'travel_city': self.travel_city,
            'amt_accom': str(self._round_decimal(self.accom_amt)),
            'amt_transport': str(self._round_decimal(self.transport_amt)),
            'amt_rental': str(self._round_decimal(self.rental_amt)),
            'amt_meals': str(self.meals_amt),
            'amt_total': str(self.total_amt),
            'amt_claimed': str(self.claimed_amt),
            'date_submitted': self.date_submitted.strftime("%Y-%m-%d")
        }

        output_buffer = io.BytesIO()

        with MailMerge(WORD_TEMPLATE) as template:
            template.merge(**template_vals)
            template.write(output_buffer)
        
        output_buffer.seek(0)
        return output_buffer