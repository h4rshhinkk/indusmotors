from core import mixins
from crm.models import BookingInvoice, BookingRequest, Opportunity, TestDriveRequest


class HomeView(mixins.HybridTemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usertype = self.request.user.usertype
        
        if usertype in ("customer_advisor", "team_lead", "finance_executive"):
            context["opportunity_open_count"] = Opportunity.objects.filter(stage="opportunity_open").count()
            context["opportunity_lost_count"] = Opportunity.objects.filter(stage="opportunity_lost").count()
            context["total_invoiced_count"] = BookingInvoice.objects.filter(status="invoiced").count()
            context["total_plan_pending_count"] = BookingInvoice.objects.filter(status="plan_pending").count()
            context["is_dashboard"] = True

        elif usertype in ("deo",):
            context["total_order_pending"] = BookingRequest.objects.filter(stage="booking_requested").count()
            context["is_dashboard"] = True
            
        elif usertype in ("test_drive_operator",):
            context["total_testdrive_pending"] = TestDriveRequest.objects.filter(status="pending").count()
            context["total_testdrive_scheduled"] = TestDriveRequest.objects.filter(status="scheduled").count()
            context["total_testdrive_rescheduled"] = TestDriveRequest.objects.filter(status="rescheduled").count()
            context["total_testdrive_done"] = TestDriveRequest.objects.filter(status="test_drived").count()
            context["total_cancelled"] = TestDriveRequest.objects.filter(status="cancelled").count()
            context["is_dashboard"] = True

        elif usertype in ("stock",):
            context["total_billing_request"] = BookingInvoice.objects.filter(status="requested").count()
            context["total_backorder_request"] = BookingRequest.objects.filter(stage="back_order_requested").count()
            context["is_dashboard"] = True

        elif usertype in ("invoice_team",):
            context["total_stock_invoice_request"] = BookingInvoice.objects.filter(status="alloted").count()
            context["is_dashboard"] = True

        elif usertype in ("finance_bo",):
            context["total_finance_approval_pending_request"] = BookingInvoice.objects.filter(
                finance_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("tmga",):
            context["total_accessory_approval_pending_request"] = BookingInvoice.objects.filter(
                accessory_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("exchange_bo",):
            context["total_exchange_approval_pending_request"] = BookingInvoice.objects.filter(
                exchange_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("registration_bo",):
            context["total_registration_approval_pending_request"] = BookingInvoice.objects.filter(
                reg_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("scheme",):
            context["total_scheme_approval_pending_request"] = BookingInvoice.objects.filter(
                scheme_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("insurance",):
            context["total_insurance_approval_pending_request"] = BookingInvoice.objects.filter(
                insurance_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("accounts",):
            context["total_accounts_approval_pending_request"] = BookingInvoice.objects.filter(
                accounts_status="pending"
            ).count()
            context["is_dashboard"] = True

        elif usertype in ("pdi",):
            context["total_pdi_approval_pending_request"] = BookingInvoice.objects.filter(pdi_status="pending").count()
            context["is_dashboard"] = True
        
        elif usertype in ("cre",):
            context["total_delivered_count"] = BookingInvoice.objects.filter(status="delivered").count()
            context["is_dashboard"] = True


        return context
