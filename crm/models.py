from core.base import BaseModel
from core.choices import (
    ANSWER_OUT_OF_CHOICES,
    ANSWER_CHOICES,
    DISCOUNT__INVOICE_STATUS,
    ANY_TYPE_EXEMPTION_CHOICE,
    BOOKING_STATUS,
    BOOL_CHOICES,
    INSURANCE_TYPE_CHOICE,
    INVOICE_PAYMENT_TYPE,
    LOST_STAGE,
    MODE_OF_PAIMENT_CHOICE,
    REGISTRATION_TYPE_CHOICE,
    REVIEW_STATUS,
    SELECTION_CHOICES,
    SELECTION_CHOICES_FINANCE,
)
from core.choices import ENQUIRY_TYPE
from core.choices import FINANCE_APPLICATION_STATUS
from core.choices import FOLLOWUP_VIA
from core.choices import OPPORTUNITY_STATUS
from core.choices import SALUTATION_CHOICES, SEPARATE_DISCOUNT_STATUS

from django.db import models
from django.urls import reverse_lazy


class Opportunity(BaseModel):
    STAGE_CHOICES = [
        ("opportunity_open", "Opportunity Open"),
        ("opportunity_lost", "Opportunity Lost"),
        ("booking_requested", "Booking Requested"),
    ]
    opt_date = models.DateField("Opportunity Date", blank=True, null=True)
    opt_id = models.CharField("Opportunity ID", max_length=128, blank=True, null=True)
    opportunity_source = models.ForeignKey(
        "masters.OpportunitySource", related_name="opportunity_source", on_delete=models.PROTECT
    )
    dse = models.ForeignKey(
        "accounts.User",
        related_name="branch_user",
        on_delete=models.PROTECT,
        limit_choices_to={"usertype": "customer_advisor"},
        verbose_name="DSE",
    )
    customer_salutation = models.CharField("Mr/Mrs", choices=SALUTATION_CHOICES, max_length=128)
    customer_name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=128)
    phone = models.CharField("Alternate Mobile", max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    place = models.CharField(max_length=128, blank=True, null=True)
    district = models.ForeignKey(
        "masters.District", on_delete=models.PROTECT, blank=True, null=True, verbose_name="District"
    )
    email = models.EmailField(max_length=128, blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    profession = models.ForeignKey(
        "masters.Profession", related_name="profession", on_delete=models.PROTECT, blank=True, null=True
    )
    profession_detail = models.CharField("Profession Details", max_length=128, blank=True, null=True)
    guardian_salutation = models.CharField(
        "Guardian Salutation (Mr/Mrs)", choices=SALUTATION_CHOICES, max_length=128, blank=True, null=True
    )
    guardian_name = models.CharField(max_length=128, blank=True, null=True)
    opt_type = models.CharField("Enquiry Type", choices=ENQUIRY_TYPE, max_length=128)
    exchange_vehicle_make = models.CharField(max_length=128, blank=True, null=True)
    exchange_vehicle_model = models.CharField(max_length=128, blank=True, null=True)
    exchange_reg_no = models.CharField(max_length=128, blank=True, null=True)
    exchange_mfg_year = models.CharField(max_length=128, blank=True, null=True)
    owner_name = models.CharField(max_length=128, blank=True, null=True)
    relation = models.CharField(max_length=128, blank=True, null=True)
    variant = models.ForeignKey("masters.Variant", related_name="variant", on_delete=models.PROTECT)
    opt_status = models.CharField("Opportunity Status", choices=OPPORTUNITY_STATUS, max_length=128)
    next_followup_date = models.DateField()
    stage = models.CharField(max_length=128, choices=STAGE_CHOICES, blank=True, null=True, default="opportunity_open")

    class Meta:
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return f"{self.customer_salutation} {self.customer_name}"

    def get_absolute_url(self):
        return reverse_lazy("crm:opportunity_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:opportunity_list")

    def get_update_url(self):
        return reverse_lazy("crm:opportunity_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:opportunity_delete", kwargs={"pk": self.pk})

    def last_followup(self):
        return OpportunityFollowUp.objects.filter(opportunity=self).first()


class OpportunityFollowUp(BaseModel):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.PROTECT)
    followup_date = models.DateField(auto_now_add=True, blank=True, null=True)
    followup_via = models.CharField("Follow up Via", choices=FOLLOWUP_VIA, max_length=128, blank=True, null=True)
    opt_status = models.CharField(
        "Opportunity Status", choices=OPPORTUNITY_STATUS, max_length=128, blank=True, null=True
    )
    exp_booking_date = models.DateField(blank=True, null=True)
    exp_retail_date = models.DateField(blank=True, null=True)
    next_followup_date = models.DateField(blank=True, null=True)
    finance = models.ForeignKey(
        "masters.FinancingCategory", related_name="finance", on_delete=models.PROTECT, blank=True, null=True
    )
    branch = models.CharField(max_length=128, blank=True, null=True)
    finance_status = models.CharField(
        "Finance Status", choices=FINANCE_APPLICATION_STATUS, max_length=128, blank=True, null=True
    )
    logged_date = models.DateField(blank=True, null=True)
    loan_amount = models.CharField(max_length=128, blank=True, null=True)
    exp_do_receiving_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    finance_executive_status = models.CharField(max_length=128, choices=REVIEW_STATUS, default="pending")
    finance_executive_remark = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Opportunity Follow-ups"
        ordering = ["-followup_date"]

    def __str__(self):
        return f"Follow-up for {self.opportunity.customer_name}"

    def get_absolute_url(self):
        return reverse_lazy("crm:followup_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:followup_create")

    def get_update_url(self):
        return reverse_lazy("crm:followup_update", kwargs={"pk": self.pk})

    def get_success_url(self):
        return reverse_lazy("crm:followup_create", kwargs={"pk": self.kwargs["pk"]})


class TestDriveRequest(BaseModel):
    TESTDRIVE_STAGE_CHOICES = [("from_opportunity", "From Opportunity"), ("after_booking", "From After Booking")]
    TESTDRIVE_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scheduled", "Scheduled"),
        ("rescheduled", "Rescheduled"),
        ("test_drived", "Test Drived"),
        ("cancelled", "Cancelled"),
    ]
    opportunity = models.ForeignKey(Opportunity, on_delete=models.PROTECT)
    variant = models.ForeignKey("masters.Variant", on_delete=models.PROTECT)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    testdrive_stage = models.CharField(max_length=128, choices=TESTDRIVE_STAGE_CHOICES, blank=True, null=True)
    status = models.CharField(
        max_length=128, choices=TESTDRIVE_STATUS_CHOICES, blank=True, null=True, default="pending"
    )
    starting_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    testdrive_given_by = models.CharField(max_length=128, blank=True, null=True)
    remarks = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Test Drive Requests"

    def get_list_url(self):
        return reverse_lazy("crm:testdrive_create", kwargs={"pk": self.opportunity.pk})

    def get_update_url(self):
        return reverse_lazy("crm:testdrive_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:testdrive_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Test Drive Request for {self.opportunity.customer_name}"

    def calculate_total_kilometers(self):
        return self.end_km - self.starting_km if self.starting_km is not None and self.end_km is not None else None


class OpportunityLost(BaseModel):
    opportunity = models.OneToOneField(Opportunity, on_delete=models.PROTECT)
    reason = models.ForeignKey(
        "masters.LostReason", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Sub Reason"
    )
    sub_reason = models.TextField("Lost Sub Reason", max_length=128, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Opportunity Losts"

    def get_list_url(self):
        return reverse_lazy("crm:opt_lost_create", kwargs={"pk": self.opportunity.pk})

    def get_update_url(self):
        return reverse_lazy("crm:opt_lost_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:opt_lost_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Opportunity Lost for {self.opportunity.customer_name}"


class BookingRequest(BaseModel):
    STAGE_CHOICES = [
        ("booking_requested", "Booking Requested"),
        ("booking_request_approved", "Booking Request Approved"),
        ("back_order_requested", "Back Order Requested"),
        ("back_order_created", "Back Order Created"),
        ("invoice_requested", "Invoice Requested"),
        ("chassis_alloted", "Chassis Alloted"),
        ("chassis_reject", "Chassis Reject"),
        ("invoice_accepted", "Invoice Accepted"),
        ("chassis_blocked", "Chassis Blocked"),
        ("booking_request_lost_with_refund", "Booking Request Lost With Refund"),
        ("booking_request_lost_without_refund", "Booking Request Lost Without Refund"),
    ]

    opportunity = models.OneToOneField(Opportunity, on_delete=models.PROTECT)
    variant = models.ForeignKey("masters.Variant", on_delete=models.PROTECT)
    order_date = models.DateField(null=True)
    order_time = models.TimeField(null=True)
    order_no = models.CharField("Order Number", max_length=128, null=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    obf = models.FileField("OBF", upload_to="Booking Request/", blank=True, null=True)
    obf_no = models.CharField("OBF No", max_length=128, blank=True, null=True)
    aadhar_card = models.FileField("Aadhar Card", upload_to="Booking Request/", blank=True, null=True)
    aadhar_card_no = models.CharField("Aadhar Card No", max_length=128, blank=True, null=True)
    scheme = models.ForeignKey("masters.CorpScheme", on_delete=models.PROTECT, blank=True, null=True)
    scheme_name = models.CharField(max_length=128, blank=True, null=True)
    institution_name = models.CharField(max_length=128, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yono_scheme_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stage = models.CharField(max_length=128, choices=STAGE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Booking Request"

    def __str__(self):
        return f"Booking Request of {self.opportunity.customer_name}"

    def get_absolute_url(self):
        return reverse_lazy("dms:booking_request_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("dms:booking_request_list")

    def get_update_url(self):
        return reverse_lazy("crm:booking_request_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:booking_request_delete", kwargs={"pk": self.pk})

    def last_followup_finance(self):
        return BookingFollowUp.objects.filter(booking_request=self).first()


class BookingFollowUp(BaseModel):
    booking_request = models.ForeignKey(BookingRequest, on_delete=models.PROTECT)
    booking_followup_date = models.DateField("Date", blank=True, null=True)
    booking_status = models.CharField("Booking Status", choices=BOOKING_STATUS, max_length=128, blank=True, null=True)
    exp_billing_date = models.DateField("Expected Billing Date", blank=True, null=True)
    exp_delivery_date = models.DateField("Expected Delivery Date", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    finance = models.ForeignKey(
        "masters.FinancingCategory", related_name="booking_finance", on_delete=models.PROTECT, blank=True, null=True
    )
    branch = models.CharField(max_length=128, blank=True, null=True)
    finance_status = models.CharField(
        "Finance Status", choices=FINANCE_APPLICATION_STATUS, max_length=128, blank=True, null=True
    )
    logged_date = models.DateField(blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    exp_do_receiving_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    finance_executive_status = models.CharField(max_length=128, choices=REVIEW_STATUS, default="pending")
    finance_executive_remark = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Booking Follow-ups"
        ordering = ["-booking_followup_date"]

    def __str__(self):
        return f"Follow-up for {self.booking_request}"

    def get_absolute_url(self):
        return reverse_lazy("crm:booking_followup_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:booking_followup_create")

    def get_update_url(self):
        return reverse_lazy("crm:booking_followup_update", kwargs={"pk": self.pk})

    def get_success_url(self):
        return reverse_lazy("crm:booking_followup_create", kwargs={"pk": self.kwargs["pk"]})


class BookingLost(BaseModel):
    CANCELLATION_CHOICES = [
        ("cancellation_with_refund", "Cancellation With Refund"),
        ("cancellation_without_refund", "Cancellation Without Refund"),
    ]
    booking_request = models.OneToOneField(BookingRequest, on_delete=models.PROTECT)
    reason = models.ForeignKey(
        "masters.LostSubReason", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Sub Reason"
    )
    remarks = models.TextField(blank=True, null=True)
    cancellation_type = models.CharField(max_length=128, choices=CANCELLATION_CHOICES, blank=True, null=True)
    obf_copy = models.FileField("OBF Copy", upload_to="Booking Lost/", blank=True, null=True)
    passbook_copy = models.FileField("Pass Book Copy", upload_to="Booking Lost/", blank=True, null=True)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    account_no = models.CharField("Account Number", max_length=128, blank=True, null=True)
    branch_name = models.CharField(max_length=128, blank=True, null=True)
    ifsc_code = models.CharField("IFSC Code", max_length=128, blank=True, null=True)
    stage = models.CharField(max_length=128, choices=LOST_STAGE, null=True)

    class Meta:
        verbose_name_plural = "Booking Losts"

    def get_list_url(self):
        return reverse_lazy("crm:booking_lost_create", kwargs={"pk": self.booking_request.pk})

    def get_update_url(self):
        return reverse_lazy("crm:booking_lost_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:booking_lost_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Booking Lost for {self.booking_request.opportunity.customer_name}"


class BackOrder(BaseModel):
    booking_request = models.OneToOneField(BookingRequest, on_delete=models.PROTECT)
    back_order_need = models.CharField(max_length=5, choices=[("Yes", "Yes"), ("No", "No")])
    remarks = models.TextField(blank=True, null=True)
    back_order_no = models.CharField(max_length=128, blank=True, null=True)
    back_order_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Booking Back Orders"

    def __str__(self):
        return f"Back Order for {self.booking_request}"

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:back_order_create")

    def get_success_url(self):
        return reverse_lazy("crm:back_order_create", kwargs={"pk": self.kwargs["pk"]})


class ChassisBlock(BaseModel):
    booking_request = models.ForeignKey(BookingRequest, on_delete=models.PROTECT)
    variant = models.ForeignKey("masters.Variant", on_delete=models.PROTECT)
    stock = models.OneToOneField("masters.Stock", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Chassis Block"

    def __str__(self):
        return str(self.booking_request)


class BookingInvoice(BaseModel):
    ACTION_CHOICES = (
        ("requested", "Requested"),
        ("rejected_stock_team", "Rejected Stock Team"),
        ("rejected_invoice_team", "Rejected Invoice Team"),
        ("alloted", "Alloted"),
        ("invoiced", "Invoiced"),
        ("plan_pending", "Plan Pending"),
        ("delivered", "Delivered"),
    )

    EXCHANGE_STATUS_CHOICES = (("genuine", "Genuine"), ("routing", "Routing"))

    CONSUMER_OFFER_CHOICES = (("green bonus", "Green Bonus"), ("consumer offer", "Consumer Offer"))

    booking_request = models.OneToOneField(BookingRequest, on_delete=models.PROTECT)
    dse = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, limit_choices_to={"usertype": "customer_advisor"}, null=True
    )

    customer_salutation = models.CharField("Mr/Mrs", max_length=128, choices=SALUTATION_CHOICES, null=True)
    customer_name = models.CharField(max_length=128, null=True)
    mobile = models.CharField(max_length=128, null=True)
    email = models.EmailField(null=True)
    guardian_salutation = models.CharField("Mr/Mrs", max_length=128, choices=SALUTATION_CHOICES, null=True)
    guardian_name = models.CharField(max_length=128, null=True)
    dob = models.DateField()
    house_name = models.CharField("House Name", max_length=128, null=True)
    place = models.CharField(max_length=128, null=True)
    village = models.CharField(max_length=128, null=True)
    pin = models.CharField("PIN", max_length=128, null=True)
    panchayath = models.CharField(max_length=128, null=True)
    post = models.CharField(max_length=128, null=True)
    district = models.ForeignKey("masters.District", related_name="perm_address", on_delete=models.PROTECT, null=True)
    # temp address
    is_temp_address = models.CharField( max_length=128, choices=SELECTION_CHOICES, null=True)

    temp_house_name = models.CharField("House Name", max_length=128, blank=True, null=True)
    temp_place = models.CharField("Place", max_length=128, blank=True, null=True)
    temp_village = models.CharField("Village", max_length=128, blank=True, null=True)
    temp_pin = models.CharField("PIN", max_length=128, blank=True, null=True)
    temp_panchayath = models.CharField("Panchayath", max_length=128, blank=True, null=True)
    temp_post = models.CharField("Post", max_length=128, blank=True, null=True)
    temp_district = models.ForeignKey(
        "masters.District", on_delete=models.PROTECT, verbose_name="District", blank=True, null=True
    )
    chassis = models.ForeignKey("masters.Stock", on_delete=models.PROTECT)
    # exchange vehicle
    is_exchange = models.CharField( max_length=128, choices=SELECTION_CHOICES, null=True)
    exchange_vehicle_make = models.CharField(max_length=128, blank=True, null=True)
    exchange_vehicle_model = models.CharField(max_length=128, blank=True, null=True)
    exchange_reg_no = models.CharField(max_length=128, blank=True, null=True)
    exchange_mfg_year = models.CharField(max_length=128, blank=True, null=True)
    owner_name = models.CharField(max_length=128, blank=True, null=True)
    relation = models.CharField(max_length=128, blank=True, null=True)
    exchange_vehicle_status = models.CharField(choices=EXCHANGE_STATUS_CHOICES, max_length=10, blank=True, null=True)
    old_car_purchase_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exchange_bonus = models.DecimalField("Any Other Deduction", max_digits=10, decimal_places=2, default=0)
    deduction_remarks = models.CharField("Deduction Remark",max_length=128, null=True)
    total_value_to_new_car = models.DecimalField("Total Value Transfred to New Car", max_digits=10, decimal_places=2, default=0)
    
    tml_share = models.CharField("TML Share", max_length=128, blank=True, null=True)
    exchange_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    dealer_share = models.CharField("Dealer Share", max_length=128, blank=True, null=True)
    total_eligible_bonus = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    exchange_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    exchange_remarks = models.CharField(max_length=128, null=True)
    # finance
    is_finance = models.CharField( max_length=128, choices=SELECTION_CHOICES_FINANCE, null=True)

    finance = models.ForeignKey("masters.FinancingCategory", on_delete=models.PROTECT, blank=True, null=True)
    branch = models.CharField(max_length=128, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    executive = models.CharField(max_length=128, blank=True, null=True)
    do_date_expecting = models.DateField("Do Recieved Date", blank=True, null=True)
    do_date = models.DateField(blank=True, null=True)
    payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan_amount_receipt_no = models.CharField("Loan Amount receipt No", max_length=128, blank=True, null=True)
    loan_amount_receipt_date = models.DateField("Loan Amount receipt Date", blank=True, null=True)
    upload_finance_letter = models.FileField(upload_to="invoice_documents/", blank=True, null=True)

    finance_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    finance_remarks = models.CharField("Remarks", max_length=128, null=True)
    # accessory
    accessory_status = models.CharField(default="pending", max_length=10, choices=REVIEW_STATUS)
    accessory_remarks = models.CharField(max_length=128, blank=True, null=True)
    # scheme
    is_scheme = models.CharField( max_length=128, choices=SELECTION_CHOICES, null=True)

    scheme = models.ForeignKey("masters.CorpScheme", on_delete=models.PROTECT, blank=True, null=True)
    scheme_name = models.CharField(max_length=128, blank=True, null=True)
    scheme_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    institution_name = models.CharField(max_length=128, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_yono_scheme = models.CharField( max_length=128, choices=SELECTION_CHOICES, null=True)
    yono_scheme_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yono_scheme_status = models.CharField(
        choices=REVIEW_STATUS, default="pending", max_length=10, blank=True, null=True
    )
    yono_scheme_remark = models.CharField("Yono Remarks", max_length=128, blank=True, null=True)
    scheme_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    scheme_remark = models.CharField("Remarks", max_length=128, null=True)
    # registration
    reg_type = models.CharField(max_length=128, null=True, choices=REGISTRATION_TYPE_CHOICE, default="perment")
    reg_remarks = models.CharField(max_length=128, null=True, blank=True)
    any_tax_exemption = models.CharField(max_length=128, null=True, choices=ANY_TYPE_EXEMPTION_CHOICE)
    tax_remarks = models.CharField(max_length=128, null=True, blank=True)
    rto = models.ForeignKey("masters.Rto", on_delete=models.PROTECT, null=True)
    reg_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    # insurance
    insurance_type = models.CharField(max_length=128, null=True, choices=INSURANCE_TYPE_CHOICE)
    ncb_eligibility = models.BooleanField(max_length=128, null=True, choices=BOOL_CHOICES)
    ncb_percentage = models.CharField(max_length=128, null=True, blank=True)
    any_other_discount = models.CharField(max_length=128, null=True, blank=True)
    insurance_remarks = models.CharField("Remarks", max_length=128, null=True, blank=True)
    nominee_name = models.CharField(max_length=128, null=True, blank=True)
    dob_of_nominee = models.DateField(null=True, blank=True)
    nominee_relation = models.CharField(max_length=128, null=True, blank=True)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    insurance_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    # discount
    discount_status = models.CharField(choices=DISCOUNT__INVOICE_STATUS, default="pending", max_length=10)
    discount_remarks = models.CharField("Remarks", max_length=128, null=True, blank=True)
    # accounts
    accounts_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    accounts_remarks = models.CharField("Remarks", max_length=128, null=True)
    # PDI
    suggested_delivery_date = models.DateField(blank=True, null=True)
    pdi_status = models.CharField(choices=REVIEW_STATUS, default="pending", max_length=10)
    pdi_remarks = models.CharField("Remarks", max_length=128, null=True, blank=True)

    # invoice
    invoice_date = models.DateField(null=True)
    invoice_no = models.CharField(max_length=128, null=True)
    
    consumer_offer = models.CharField(choices=CONSUMER_OFFER_CHOICES, max_length=128, null=True, blank=True)
    consumer_offer_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    consumer_offer_amount = models.DecimalField("Amount", max_digits=10, decimal_places=2, default=0)
    consumer_dealer_share = models.DecimalField("Dealer Share", max_digits=10, decimal_places=2, default=0)
    consumer_tml_share = models.DecimalField("TML Share", max_digits=10, decimal_places=2, default=0)
    
    isl_scheme = models.CharField(max_length=128, null=True, blank=True)
    isl_offer_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    isl_share = models.DecimalField("ISL Share", max_digits=10, decimal_places=2, default=0)
    isl_dealer_share = models.DecimalField("ISL Dealer Share", max_digits=10, decimal_places=2, default=0)
    total_isl_amount = models.DecimalField("Total ISL", max_digits=10, decimal_places=2, default=0)

    invoice_scheme_name = models.CharField(max_length=128, null=True, blank=True)
    invoice_scheme_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    invoice_scheme_dealer_share = models.DecimalField("Scheme Dealer Share", max_digits=10, decimal_places=2, default=0)
    invoice_scheme_tml_share = models.DecimalField("Scheme TML Share", max_digits=10, decimal_places=2, default=0)
    invoice_scheme_total_amount = models.DecimalField("Total Scheme Amount", max_digits=10, decimal_places=2, default=0)

    invoice_yono_name = models.CharField(max_length=128, null=True, blank=True)
    invoice_yono_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    invoice_yono_dealer_share = models.DecimalField("YONO Dealer Share", max_digits=10, decimal_places=2, default=0)
    invoice_yono_tml_share = models.DecimalField("YONO TML Share", max_digits=10, decimal_places=2, default=0)
    invoice_yono_total_amount = models.DecimalField("Total YONO Amount", max_digits=10, decimal_places=2, default=0)

    invoice_exchange_name = models.CharField(max_length=128, null=True, blank=True)
    invoice_exchange_campaign_code = models.CharField("Campaign Code", max_length=128, null=True, blank=True)
    invoice_exchange_dealer_share = models.DecimalField("Exchange Dealer Share", max_digits=10, decimal_places=2, default=0)
    invoice_exchange_tml_share = models.DecimalField("Exchange TML Share", max_digits=10, decimal_places=2, default=0)
    invoice_exchange_total_amount = models.DecimalField("Total Exchange Amount", max_digits=10, decimal_places=2, default=0)

    remarks = models.CharField(max_length=128, null=True)
    status = models.CharField(max_length=25, choices=ACTION_CHOICES, default="requested")
    other_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_remark = models.CharField(max_length=128, null=True, blank=True)
    # price
    showroom_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    road_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registration_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tcs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rsa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    p2p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extended_warranty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # discount prices
    # green_bonous = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    # consumer_offer = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    # date
    plan_ok_date = models.DateField(null=True, blank=True)
    # documents delivary pending registration dep
    form20 = models.FileField(null=True, upload_to="invoice/documents/")
    disclimer = models.FileField(null=True, upload_to="invoice/documents/")
    under_taking_letter = models.FileField(null=True, upload_to="invoice/documents/")
    # documents delivary pending Accounts dep
    invoice = models.FileField(null=True, upload_to="invoice/documents/")
    settlement = models.FileField(null=True, upload_to="invoice/documents/")
    receipts = models.FileField(null=True, upload_to="invoice/documents/")
    # documents delivared TL
    signed_form20 = models.FileField(null=True, upload_to="invoice/documents/")
    signed_disclimer = models.FileField(null=True, upload_to="invoice/documents/")
    signed_under_taking_letter = models.FileField(null=True, upload_to="invoice/documents/")
    signed_invoice = models.FileField(null=True, upload_to="invoice/documents/")
    signed_settlement = models.FileField(null=True, upload_to="invoice/documents/")
    delivary_photo = models.FileField(null=True, upload_to="invoice/documents/")    
    signed_gate_pass = models.FileField(null=True, upload_to="invoice/documents/")
    
    #accounts_amounts_additional_fields - dicount
    ac_consumer_offer_amount = models.DecimalField("Consumer Offer Amount", max_digits=10, decimal_places=2, default=0)
    #accounts_amounts_additional_fields - vehicle price details(vd)
    vd_other_amount_one = models.DecimalField("Other Amount", max_digits=10, decimal_places=2, default=0)
    vd_other_amount_two = models.DecimalField("Other Amount", max_digits=10, decimal_places=2, default=0)

    #accounts_amounts_additional_fields - reciepts amount details(rd)
    rd_other_amount_one = models.DecimalField("Other Amount", max_digits=10, decimal_places=2, default=0)
    rd_other_amount_two = models.DecimalField("Other Amount", max_digits=10, decimal_places=2, default=0)
    

    vehicle_delivered_date = models.DateField("Date Of Delivery",null=True,blank=True)

    #doc accesory bill
    accessory_bill = models.FileField("Upload Accessory Bill",null=True,blank=True, upload_to="invoice/documents/")
    front_image = models.FileField("Upload Front View Image",null=True,blank=True, upload_to="invoice/pdi_images/")
    rear_image = models.FileField("Upload Rear View Image",null=True,blank=True, upload_to="invoice/pdi_images/")
    rh_image = models.FileField("Upload Right Side Image",null=True,blank=True, upload_to="invoice/pdi_images/")
    lh_image = models.FileField("Upload Left Side Image",null=True,blank=True, upload_to="invoice/pdi_images/")
    engine_room = models.FileField("Upload Engine Room Image",null=True,blank=True, upload_to="invoice/pdi_images/")

    class Meta:
        verbose_name_plural = "Booking Invoice"

    def __str__(self):
        return f"Invoice Request of {self.booking_request.opportunity.customer_name}"

    def get_absolute_url(self):
        return reverse_lazy("crm:invoice_plan_detail", kwargs={"pk": self.pk})

    def get_discounts(self):
        return InvoiceDiscount.objects.filter(invoice=self, discount_status="approve", is_active=True)

    def get_registration_remarks(self):
        return RegistrationRemark.objects.filter(invoice=self)

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:booking_tracker_list")

    def get_success_url(self):
        return reverse_lazy("crm:booking_tracker_list", kwargs={"pk": self.kwargs["pk"]})

    def get_invoice_team_reject_url(self):
        return reverse_lazy("stock:invoice_reject_invoice_team", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("stock:billing_request_update", kwargs={"pk": self.pk})

    def get_invoice_update_url(self):
        return reverse_lazy("crm:invoice_request_update", kwargs={"pk": self.pk})

    def get_discount_create_url(self):
        return reverse_lazy("crm:invoice_discount_create", kwargs={"pk": self.pk})

    def get_accessory_create_url(self):
        return reverse_lazy("crm:invoice_accessory_create", kwargs={"pk": self.pk})

    def get_document_create_url(self):
        return reverse_lazy("crm:invoice_document_create", kwargs={"pk": self.pk})

    def get_finance_status_update_url(self):
        return reverse_lazy("crm:finance_status_update", kwargs={"pk": self.pk})

    def get_exchange_status_update_url(self):
        return reverse_lazy("crm:exchange_status_update", kwargs={"pk": self.pk})

    def get_registration_status_update_url(self):
        return reverse_lazy("crm:registration_status_update", kwargs={"pk": self.pk})

    def get_scheme_status_update_url(self):
        return reverse_lazy("crm:scheme_status_update", kwargs={"pk": self.pk})

    def get_insurance_status_update_url(self):
        return reverse_lazy("crm:insurance_status_update", kwargs={"pk": self.pk})

    def get_pdi_status_update_url(self):
        return reverse_lazy("crm:pdi_status_update", kwargs={"pk": self.pk})

    def get_accessory_status_update_url(self):
        return reverse_lazy("crm:accessory_status_update", kwargs={"pk": self.pk})

    def get_discount_status_update_url(self):
        return reverse_lazy("crm:discount_status_update", kwargs={"pk": self.pk})

    def get_accounts_status_update_url(self):
        return reverse_lazy("crm:accounts_status_update", kwargs={"pk": self.pk})

    def registration_remark_create_url(self):
        return reverse_lazy("crm:registration_remark_create", kwargs={"pk": self.pk})

    def booking_invoice_document_create_url(self):
        return reverse_lazy("crm:booking_invoice_document_create", kwargs={"pk": self.pk})

    def get_discount_total_amount(self):
        discount_total = sum([i.amount for i in self.get_discounts()])
        return discount_total + self.amount + self.yono_scheme_amount + self.ac_consumer_offer_amount

    def on_road_price(self):
        return (
            self.showroom_price
            + self.insurance
            + self.road_tax
            + self.registration_charge
            + self.tcs
            + self.rsa
            + self.p2p
            + self.extended_warranty
            + self.vd_other_amount_one
            + self.vd_other_amount_two
        )

    def get_accessory_total(self):
        accessory_qs = InvoiceAccessory.objects.filter(is_active=True, invoice=self)
        return sum(i.amount for i in accessory_qs)

    def total_price(self):
        return self.on_road_price() + self.get_accessory_total()

    def to_pay(self):
        return self.total_price() - self.get_discount_total_amount()

    def get_total_receipt_amount(self):
        topups = InvoiceTopUp.objects.filter(is_active=True, invoice=self)
        topup_amount_total = sum([i.top_up_amount for i in topups])
        return topup_amount_total + self.loan_amount + self.booking_request.order_amount

    def get_balance(self):
        return self.to_pay() - self.get_total_receipt_amount()


class InvoiceDiscount(BaseModel):
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.PROTECT)
    discount = models.ForeignKey("masters.Discount", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_remark = models.CharField(max_length=120,blank=True, null=True)
    discount_status = models.CharField(
        choices=SEPARATE_DISCOUNT_STATUS, default="pending", max_length=10, blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse_lazy("crm:invoice_discount_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("crm:invoice_discount_update", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.invoice} - {self.discount}"


class InvoiceAccessory(BaseModel):
    ACCESSORY_CHOICES = [("TMGA", "TMGA"), ("VAS", "VAS")]
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.PROTECT)
    accessory_type = models.CharField(max_length=20, choices=ACCESSORY_CHOICES)
    accessory_name = models.CharField(max_length=128)
    payment_type = models.CharField(max_length=20, choices=INVOICE_PAYMENT_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("accessory_type",)

    def __str__(self):
        return f"{self.invoice} - {self.accessory_name}"

    def get_absolute_url(self):
        return reverse_lazy("crm:invoice_accessory_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("crm:invoice_accessory_update", kwargs={"pk": self.pk})


class InvoiceDocument(BaseModel):
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.PROTECT)
    document = models.ForeignKey("masters.Document", on_delete=models.PROTECT)
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return f"{self.invoice} - {self.document}"


class RegistrationRemark(BaseModel):
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.CASCADE)
    remark = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.invoice} {self.remark}"


class AfterDeliveryFollowup(BaseModel):
    
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.CASCADE, limit_choices_to={"status": "delivered"})
    dcall_date = models.DateField("D+7 Call Date",blank=True, null=True)
    

    question_1 = models.CharField("At the time of booking, did the Customer Advisor handover the Order booking & Commitment form* with all the booking and deal details?",
                                  max_length=128, blank=True, null=True)
    answer_1 = models.CharField("Answer",choices=ANSWER_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_1 = models.TextField("Remark",blank=True, null=True)

    question_2 = models.CharField("Did the Sales Consultant proactively keep you informed about your vehicle's delivery status?",max_length=128, blank=True, null=True)
    answer_2 = models.CharField("Answer",choices=ANSWER_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_2 = models.TextField("Remark",blank=True, null=True)


    question_3 = models.CharField("How would you like to rate the dealership facility in terms of cleanliness, comfort & Amenities available at the dealership (Ex: Parking Facility, Air conditioning, Ambience, Beverages, Snacks, Wi-Fi etc.)?",max_length=128, blank=True, null=True)
    answer_3 = models.CharField("Answer",choices=ANSWER_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_3 = models.TextField("Remark",blank=True, null=True)

    question_4 = models.CharField("How would you like to rate your Sales Consultant on Grooming, Communication Skills and Courtesy?",max_length=128, blank=True, null=True)
    answer_4 = models.CharField("Answer",choices=ANSWER_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_4 = models.TextField("Remark",blank=True, null=True)

    question_5 = models.CharField("Keeping in consideration, the features explanation provided by the Sales Consultant and ability to answer your queries, How would you like to rate the Sales Consultant on his/her Knowledge/ Expertise about Vehicles?",max_length=128, blank=True, null=True)
    answer_5 = models.CharField("Answer",choices=ANSWER_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_5 = models.TextField("Remark",blank=True, null=True)

    question_6 = models.CharField("How would you like to rate the paperwork process in terms of clarity of explanation and timeliness of completion?",max_length=128, blank=True, null=True)
    answer_6 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_6 = models.TextField("Remark",blank=True, null=True)

    question_7 = models.CharField("How would you like to rate the condition of your vehicle on the day of delivery (Ex: clean and perfect condition)?",max_length=128, blank=True, null=True)
    answer_7 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_7 = models.TextField("Remark",blank=True, null=True)

    question_8 = models.CharField("How would you like to rate the vehicle delivery ceremony?",max_length=128, blank=True, null=True)
    answer_8 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_8 = models.TextField("Remark",blank=True, null=True)

    question_9 = models.CharField("How would you like to rate the quality of explanations done by Sales consultant for your vehicle's features, operations and controls on the day of delivery?",max_length=128, blank=True, null=True)
    answer_9 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_9 = models.TextField("Remark",blank=True, null=True)

    question_10 = models.CharField("On the day of delivery, How would you like to rate the timeliness of completing the final delivery (ex: Going over features, owner's manual etc)?",max_length=128, blank=True, null=True)
    answer_10 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_10 = models.TextField("Remark",blank=True, null=True)

    question_11 = models.CharField("On the day of delivery, how long did it take from the moment you arrived at the dealership to driving out in the new vehicle?",max_length=128, blank=True, null=True)
    answer_11 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_11 = models.TextField("Remark",blank=True, null=True)

    question_12 = models.CharField("Sir/Ma'am, is anything pending to be received from the dealership which you want us to inform them about?",max_length=128, blank=True, null=True)
    answer_12 = models.CharField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10, blank=True, null=True)
    answer_remark_12 = models.TextField("Remark",blank=True, null=True)

    question_13 = models.CharField("How would you like to rate your overali vehicle Purchase experience?",max_length=128, blank=True, null=True)
    answer_13 = models.TextField("Answer",choices=ANSWER_OUT_OF_CHOICES, max_length=10,blank=True, null=True)
    answer_remark_13 = models.TextField("Remark",blank=True, null=True)

    question_14 = models.CharField("Dealer Staff: Gave overview of Z Connect App",max_length=128, blank=True, null=True)
    answer_14 = models.TextField("Answer",choices=ANSWER_OUT_OF_CHOICES,max_length=10,blank=True, null=True)
    answer_remark_14 = models.TextField("Remark",blank=True, null=True)

    question_15 = models.CharField("Dealer Staff: Gave overview of charging process",max_length=128, blank=True, null=True)
    answer_15 = models.TextField("Answer",choices=ANSWER_OUT_OF_CHOICES,max_length=10,blank=True, null=True)
    answer_remark_15 = models.TextField("Remark",blank=True, null=True)

    customer_voice = models.TextField("Customer Voice",blank=True, null=True)
    d15_calling_remark = models.TextField("D+15 Calling Remark",blank=True, null=True)


    def __str__(self):
        return f"{self.invoice} {self.remarks}"


class InvoiceTopUp(BaseModel):
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.PROTECT)
    receipt_no = models.CharField(max_length=128)
    receipt_date = models.DateField()
    top_up_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_payment = models.CharField(max_length=20, choices=MODE_OF_PAIMENT_CHOICE)
    receipt_document = models.FileField(upload_to="invoice_top_up/documents", null=True, blank=True)

    def __str__(self):
        return f"Invoice Receipt of {self.invoice.customer_name}"


# documents in stage delivarypending
class BookingInvoiceDocument(BaseModel):
    invoice = models.ForeignKey(BookingInvoice, on_delete=models.PROTECT)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        limit_choices_to={"usertype__in": ("team_lead", "registration_bo", "accounts")},
    )
    document_name = models.CharField(max_length=128)
    document = models.FileField(upload_to="invoice/documents", null=True, blank=True)

    def __str__(self):
        return f"{self.document_name} document of {self.invoice.customer_name}"

    def get_update_url(self):
        return reverse_lazy("crm:booking_invoice_document_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:booking_invoice_document_delete", kwargs={"pk": self.pk})

    def get_list_url(self):
        return reverse_lazy("crm:booking_invoice_document_create", kwargs={"pk": self.invoice.pk})



class DailyReport(BaseModel):
    customer_advisor = models.ForeignKey(
        "accounts.User",
        related_name="dr_branch_user",
        on_delete=models.PROTECT,
        limit_choices_to={"usertype": "customer_advisor"},
        verbose_name="Customer Advisor",
    )
    customer_name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    place = models.CharField(max_length=128, blank=True, null=True)
    profession = models.CharField(max_length=128, blank=True, null=True)
    segment = models.CharField(max_length=128, blank=True, null=True)
    existing_vehicle_details = models.CharField(max_length=128, blank=True, null=True)
    interested_in_new_car = models.CharField(max_length=128, blank=True, null=True)
    
    def __str__(self):
        return self.customer_name
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:daily_report_list")
    

class DigitalLeadEnquiry(BaseModel):
    STAGE_CHOICES = [
        ("lead_open", "Lead Open"),
        ("lead_lost", "Lead Lost"),
        
    ]
    customer_name = models.CharField(max_length=128, blank=True, null=True)
    phone_1 = models.CharField("Phone 1",max_length=128, blank=True, null=True)
    phone_2 = models.CharField("Phone 2",max_length=128, blank=True, null=True)
    vehicle_interested = models.CharField(max_length=128, blank=True, null=True)
    opportunity_source = models.ForeignKey(
        "masters.OpportunitySource", related_name="digital_lead_source", on_delete=models.PROTECT,blank=True, null=True
    )
    initial_remark = models.TextField(blank=True, null=True)
    attended_by = models.ForeignKey(
        "masters.Tellecaller", related_name="attended_tellecaller", on_delete=models.PROTECT,blank=True, null=True
    )
    remark_by_tellecaller = models.TextField(blank=True, null=True)
    expected_buying_date = models.DateField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        "accounts.User",
        related_name="dl_branch_user",
        on_delete=models.PROTECT,
        limit_choices_to={"usertype": "team_lead"},
        verbose_name="Assigned to Team Lead",
    )
    stage = models.CharField(max_length=128, choices=STAGE_CHOICES, blank=True, null=True, default="lead_open")
    
    class Meta:
        verbose_name_plural = "Dgital Leads"
    
    def __str__(self):
        return self.customer_name
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:digital_leads_list")
    


class DigitalLeadFollowUp(BaseModel):
    digital_lead = models.ForeignKey(DigitalLeadEnquiry, on_delete=models.PROTECT)
    followup_date = models.DateField(auto_now_add=True, blank=True, null=True)
    followup_via = models.CharField("Follow up Via", choices=FOLLOWUP_VIA, max_length=128, blank=True, null=True)
    opt_status = models.CharField(
        "Lead Status", choices=OPPORTUNITY_STATUS, max_length=128, blank=True, null=True
    )
    exp_booking_date = models.DateField(blank=True, null=True)
    exp_retail_date = models.DateField(blank=True, null=True)
    next_followup_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Dgital Follow-ups"
        ordering = ["-followup_date"]

    def __str__(self):
        return f"Dgital Followup for {self.digital_lead.customer_name}"

    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:digital_lead_followup_create")
    

class DigitalLeadEnquiryLost(BaseModel):
    digital_lead = models.OneToOneField(DigitalLeadEnquiry, on_delete=models.PROTECT)
    reason = models.ForeignKey(
        "masters.LostReason", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Reason"
    )
    sub_reason = models.TextField("Lost Sub Reason", max_length=128, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Digital Lead Enquiry Losts"

   
    def __str__(self):
        return f"Lead Lost for {self.digital_lead.customer_name}"


    def get_list_url(self):
        return reverse_lazy("crm:digital_lead_lost_create", kwargs={"pk": self.digital_lead.pk})



class EventReport(BaseModel):
    event_id = models.CharField(max_length=128,null=True)
    event_date = models.DateField(blank=True, null=True)
    event_location = models.CharField(max_length=128, blank=True, null=True)
    model_displayed = models.CharField(max_length=128, blank=True, null=True)
    total_footfall = models.DecimalField("Total Footfall", max_digits=10, decimal_places=2, default=0)
    prospects = models.DecimalField("Prospects", max_digits=10, decimal_places=2, default=0)
    total_booking = models.DecimalField("Total Booking", max_digits=10, decimal_places=2, default=0)
    total_retail = models.DecimalField("Total Retail", max_digits=10, decimal_places=2, default=0)
    responsible_ca = models.ForeignKey(
        "accounts.User",
        related_name="event_branch_user",
        on_delete=models.PROTECT,
        limit_choices_to={"usertype": "customer_advisor"},
        verbose_name="Customer Advisor",
    )
    event_expense = models.DecimalField("Event Expense", max_digits=10, decimal_places=2, default=0)
    cost_per_enquiry = models.DecimalField("Cost Per Enquiry", max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.customer_name
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("crm:event_report_list")
    
    def get_update_url(self):
        return reverse_lazy("crm:event_report_update", kwargs={"pk": self.pk})
    
class EventPhoto(BaseModel):
    event = models.ForeignKey(EventReport, on_delete=models.PROTECT)
    file = models.FileField(upload_to="event-images/")

    def __str__(self):
        return f"{self.event}"
    
class EventCustomerDetails(BaseModel):
    event = models.ForeignKey(EventReport, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField("Phone",max_length=128, blank=True, null=True)
    enquiry_model = models.CharField("Enquiry Model",max_length=128, blank=True, null=True)
    existing_model = models.CharField("Existing Model",max_length=128, blank=True, null=True)
    enquiry_status = models.CharField("Enquiry Status", choices=OPPORTUNITY_STATUS, max_length=128)
    customer_profile = models.CharField("Customer Profile",max_length=128, blank=True, null=True)
    exp_booking_date = models.DateField(blank=True, null=True)
    ca_name = models.CharField("CA Name",max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name}"