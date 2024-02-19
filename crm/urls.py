from . import views
from django.urls import path


app_name = "crm"

urlpatterns = [
    # ajax
    path("get/variants/", views.VariantListView.as_view(), name="get_variants"),
    path("get/reasons/", views.ReasonListView.as_view(), name="get_reasons"),
    path("get/chassis/", views.GetChassisListView.as_view(), name="get_chassis"),
    path("get/state/", views.StateListView.as_view(), name="get_state"),
    # general
    path("opportunities/", views.OpportunityListView.as_view(), name="opportunity_list"),
    path("new/opportunity/", views.OpportunityCreateView.as_view(), name="opportunity_create"),
    path("opportunity/<str:pk>/", views.OpportunityDetailView.as_view(), name="opportunity_detail"),
    path("opportunity/<str:pk>/update/", views.OpportunityUpdateView.as_view(), name="opportunity_update"),
    path("opportunity/<str:pk>/delete/", views.OpportunityDeleteView.as_view(), name="opportunity_delete"),
    # opt followup
    path("opt/followup/<str:pk>/new/", views.OpportunityFollowUpCreateView.as_view(), name="followup_create"),
    path("opt/followup/<str:pk>/detail/", views.OpportunityFollowUpDetailView.as_view(), name="followup_detail"),
    path("opt/followup/<str:pk>/update/", views.OpportunityFollowUpUpdateView.as_view(), name="followup_update"),
    path("opt/testdrive/<str:pk>/", views.TestDriveRequestCreateView.as_view(), name="testdrive_create"),
    path("opt/testdrive/<str:pk>/update/", views.TestDriveRequestUpdateView.as_view(), name="testdrive_update"),
    path("opt/testdrive/<str:pk>/delete/", views.TestDriveRequestDeleteView.as_view(), name="testdrive_delete"),
    path("opt/lost-update/<str:pk>/", views.OpportunityLostCreateView.as_view(), name="opt_lost_create"),
    path("opt/lost-update/<str:pk>/update/", views.OpportunityLostUpdateView.as_view(), name="opt_lost_update"),
    path("opt/lost-update/<str:pk>/delete/", views.OpportunityLostDeleteView.as_view(), name="opt_lost_delete"),
    path("opt/booking-request/<str:pk>/", views.BookingRequestCreateView.as_view(), name="booking_request_create"),
    path(
        "opt/booking-request/<str:pk>/update/", views.BookingRequestUpdateView.as_view(), name="booking_request_update"
    ),
    path(
        "opt/booking-request/<str:pk>/delete/", views.BookingRequestDeleteView.as_view(), name="booking_request_delete"
    ),
    path("booking-tracker/", views.BookingTrackerListView.as_view(), name="booking_tracker_list"),
    path("booking-followup/<str:pk>/new/", views.BookingFollowUpCreateView.as_view(), name="booking_followup_create"),
    path(
        "booking-followup/<str:pk>/detail/", views.BookingFollowUpDetailView.as_view(), name="booking_followup_detail"
    ),
    path(
        "booking-followup/<str:pk>/update/", views.BookingFollowUpUpdateView.as_view(), name="booking_followup_update"
    ),
    path("booking/lost-update/<str:pk>/", views.BookingLostCreateView.as_view(), name="booking_lost_create"),
    path("booking/lost-update/<str:pk>/update/", views.BookingLostUpdateView.as_view(), name="booking_lost_update"),
    path("booking/lost-update/<str:pk>/delete/", views.BookingLostDeleteView.as_view(), name="booking_lost_delete"),
    # booking_cancelation_verfy_asm_gm_accounts
    path("booking-lost-list/", views.BookingLostListView.as_view(), name="booking_lost_list"),
    path(
        "booking-lost/dpt-update/<str:pk>/update/",
        views.BookingLostDptUpdateView.as_view(),
        name="booking_lost_dpt_update",
    ),
    path("back-order/<str:pk>/new/", views.BackOrderCreateView.as_view(), name="back_order_create"),
    path("chassis-block/<str:pk>/new/", views.ChassisBlockCreateView.as_view(), name="chassis_block_create"),
    path("invoice-request/<str:pk>/new/", views.BookingInvoiceCreateView.as_view(), name="invoice_request_create"),
    path("invoice-update/<str:pk>/update/", views.BookingInvoiceUpdateView.as_view(), name="invoice_request_update"),
    path("invoice-plan/<str:pk>/detail/", views.InvoicePlanDetailView.as_view(), name="invoice_plan_detail"),
    path("pending-testdrive/", views.PendingTestDriveListView.as_view(), name="pending_testdrive_list"),
    path("pending-testdrive/<str:pk>/update_status/", views.testdrive_status_update, name="testdrive_status_update"),
    path(
        "pending-testdrive/<str:pk>/update/",
        views.PendingTestDriveUpdateView.as_view(),
        name="pending_testdrive_update",
    ),
    path("invoice/discount/<str:pk>/", views.InvoicediscountDetailView.as_view(), name="invoice_discount_detail"),
    path("invoice/discount/<str:pk>/new/", views.InvoiceDiscountCreateView.as_view(), name="invoice_discount_create"),
    path(
        "invoice/discount/<str:pk>/update/", views.InvoiceDiscountUpdateView.as_view(), name="invoice_discount_update"
    ),
    path("invoice/accessory/<str:pk>/", views.InvoiceAccessoryDetailView.as_view(), name="invoice_accessory_detail"),
    path(
        "invoice/accessory/<str:pk>/new/", views.InvoiceAccessoryCreateVIew.as_view(), name="invoice_accessory_create"
    ),
    path(
        "invoice/accessory/<str:pk>/update/",
        views.InvoiceAccessoryUpdateView.as_view(),
        name="invoice_accessory_update",
    ),
    path("invoice/document/<str:pk>/new/", views.InvoiceDocumentUpdateView.as_view(), name="invoice_document_create"),
    # Deliveray list
    path("plan_pending/", views.PlanPendingListView.as_view(), name="plan_pending_list"),
    path("sale_support/", views.SaleSupportListView.as_view(), name="sale_support_list"),
    path("plan_accounts/", views.PlanAccountsListView.as_view(), name="plan_accounts"),
    # department verification
    path("invoice/finance/<str:pk>/update/", views.FinanceStatusUpdateView.as_view(), name="finance_status_update"),
    path("invoice/exchange/<str:pk>/update/", views.ExchangeStatusUpdateView.as_view(), name="exchange_status_update"),
    path(
        "invoice/registration/<str:pk>/update/",
        views.RegistrationStatusUpdateView.as_view(),
        name="registration_status_update",
    ),
    path("invoice/scheme/<str:pk>/update/", views.SchemeStatusUpdateView.as_view(), name="scheme_status_update"),
    path(
        "invoice/insurance/<str:pk>/update/", views.InsuranceStatusUpdateView.as_view(), name="insurance_status_update"
    ),
    path("invoice/pdi/<str:pk>/update/", views.PdiStatusUpdateView.as_view(), name="pdi_status_update"),
    path(
        "invoice/accessory_verification/<str:pk>/update/",
        views.AccessoryStatusUpdateView.as_view(),
        name="accessory_status_update",
    ),
    path(
        "invoice/discount_verification/<str:pk>/update/",
        views.DiscountStatusUpdateView.as_view(),
        name="discount_status_update",
    ),
    path(
        "each-pending-discount/<str:pk>/update_status/",
        views.each_discount_status_update,
        name="each_discount_status_update",
    ),
    path(
        "invoice/accounts_verification/<str:pk>/update/",
        views.AccountsStatusUpdateView.as_view(),
        name="accounts_status_update",
    ),
    # delivary
    path("delivary_pending/", views.DeliveryPendingListView.as_view(), name="delivary_pending_list"),
    path("delivered/", views.DeliveredListView.as_view(), name="delivered_list"),
    path("document_upload_accounts_team/", views.DocumentUploadAccountsTeamView.as_view(), name="document_upload_accounts_team"),
    path(
        "registration_remark/<str:pk>/", views.RegistrationRemarkCreateView.as_view(), name="registration_remark_create"
    ),
    path("invoice_accessory_list/", views.InvoiceAccessoryListView.as_view(), name="invoice_accessory_list"),
    path("accessory_job_card/<str:pk>/", views.JobcardView.as_view(), name="job_card"),
    path("gate_pass/<str:pk>/", views.GatepassView.as_view(), name="gate_pass"),
    path("update_to_deliverd/<str:pk>/", views.UpdatetoDeliverd.as_view(), name="update_to_delivered"),
    path(
        "delivered/followup/<str:pk>/new/",
        views.AfterDeliveryFollowupCreateView.as_view(),
        name="delivered_followup_create",
    ),
    path("after_delivery_followup_print/<str:pk>/", views.AfterDeliveryFollowupPrintView.as_view(), name="after_delivery_followup_print"),

    path("invoiced_requets/", views.InvoiceRejectedListView.as_view(), name="invoice_rejected_list"),
    path(
        "invoice_rejected_update/<str:pk>/update/",
        views.InvoiceRejectedUpdateView.as_view(),
        name="invoice_rejected_update",
    ),
    path(
        "each-pending-discount/<str:pk>/update_status/",
        views.each_discount_status_update,
        name="each_discount_status_update",
    ),
    # document
    path(
        "booking_invoice/document/<str:pk>/new/",
        views.BookingInvoiceDocumentCreateVIew.as_view(),
        name="booking_invoice_document_create",
    ),

    path("dailyreports/", views.DailyReportListView.as_view(), name="daily_report_list"),
    path("new/dailyreport/", views.DailyReportCreateView.as_view(), name="daily_report_create"),


    path("digital_leads/", views.DigitalLeadEnquiryListView.as_view(), name="digital_leads_list"),
    path("new/digital_lead/", views.DigitalLeadEnquiryCreateView.as_view(), name="digital_leads_create"),

    #digital lead followup /lost

    path("digital_lead/followup/<str:pk>/new/", views.DigitalLeadFollowUpCreateView.as_view(), name="digital_lead_followup_create"),
    path("digital_lead/lost-update/<str:pk>/", views.DigitalLeadLostCreateView.as_view(), name="digital_lead_lost_create"),


    path("eventreports/", views.EventReportListView.as_view(), name="event_report_list"),
    path("new/eventreport/", views.EventReportCreateView.as_view(), name="event_report_create"),
    path("event_report/<str:pk>/update/", views.EventReportUpdateView.as_view(), name="event_report_update"),

    path("event_photo/upload/<str:pk>/new/", views.EventPhotoUploadCreateView.as_view(), name="event_photo_create"),
    path("new/event/customer_details/<str:pk>/new/", views.EventCustomerDetailsCreateView.as_view(), name="event_customer_details_create"),
    # path("event/customer_details/list/", views.EventCustomerDetailsListView.as_view(), name="event_customer_details_list"),

    

]
