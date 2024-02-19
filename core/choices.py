import calendar
import datetime

import pytz


BOOL_CHOICES = ((True, "Yes"), (False, "No"))

GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))

RATING_CHOICES = ((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"))

STATUS_CHOICES = (("on_hold", "On hold"), ("rejected", "Rejected"), ("approved", "Approved"))

SALUTATION_CHOICES = (("Dr.", "Dr."), ("Miss", "Miss"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Prof.", "Prof."))

TAX_CHOICES = ((0, "0 %"), (5, "5 %"), (10, "10 %"), (12, "12 %"), (15, "15 %"), (18, "18 %"), (20, "20 %"))

YEAR_CHOICES = [(y, y) for y in range(1950, datetime.date.today().year + 2)]

MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]

TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]

ENQUIRY_TYPE = (
    ("Additional Buyer", "Additional Buyer"),
    ("Exchange Buyer", "Exchange Buyer"),
    ("First Time Buyer", "First Time Buyer"),
)

OPPORTUNITY_STATUS = (("Cold", "Cold"), ("Hot", "Hot"), ("Warm", "Warm"))

FOLLOWUP_VIA = (("Personal_Visit", "Personal Visit"), ("Telephonic", "Telephonic"))

FINANCE_APPLICATION_STATUS = [
    ("All paper submitted", "All paper submitted"),
    ("Approved", "Approved"),
    ("DD received", "DD received"),
    ("DO received", "DO received"),
    ("Logged", "Logged"),
    ("No paper collected", "No paper collected"),
    ("Partial paper collected", "Partial paper collected"),
    ("To be cancel", "To be cancel"),
]

BOOKING_STATUS = (("live", "Live"), ("non_live", "Non Live"))


ACCESSORY_STAGE = [("requested", "requested"), ("approved", "Approved"), ("rejected", "Rejected")]

INVOICE_PAYMENT_TYPE = (("PAID", "PAID"), ("FOC", "FOC"))


REVIEW_STATUS = (("pending", "Pending"), ("ok", "OK"), ("not_ok", "NOT OK"))

DISCOUNT__INVOICE_STATUS = (("pending", "Pending"), ("forward", "Forward"), ("ok", "Ok"), ("not_ok", "Not OK"))

REGISTRATION_TYPE_CHOICE = (
    ("perment", "Permanent"),
    ("temp_no_reservation", "Number Reservation TP"),
    ("temp_other_state", "Other State TP"),
)

ANY_TYPE_EXEMPTION_CHOICE = (("no", "No"), ("handicaped", "Handicaped"), ("others", "Others"))

INSURANCE_TYPE_CHOICE = (("in_house", "In House"), ("out_side", "Out Side"))

LOST_STAGE = (("approve", "Approve"), ("forward", "Forward"), ("refund", "Refund"))

SEPARATE_DISCOUNT_STATUS = (
    ("pending", "Pending"),
    ("approve", "Approve"),
    ("escalate", "Escalate"),
    ("reject", "Reject"),
)

MODE_OF_PAIMENT_CHOICE = (("Bank", "Bank"), ("Cash", "Cash"))


SELECTION_CHOICES = (("", "Select"),("yes", "Yes"), ("no", "No"))

SELECTION_CHOICES_FINANCE = (("", "Yes or Cash"),("yes", "Yes"), ("cash", "Cash"))

ANSWER_CHOICES = (("yes", "Yes"), ("no", "No"),)

ANSWER_OUT_OF_CHOICES = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"))