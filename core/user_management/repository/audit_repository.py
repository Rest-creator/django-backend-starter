from django_backend_starter.apps.loan.models import LoginAudit

class AuditRepository:
    def log_event(self, user=None, email=None, event_type="FAILURE", ip=None, ua=None):
        return LoginAudit.objects.create(
            user=user,
            email_attempted=email,
            event_type=event_type,
            ip_address=ip,
            user_agent=ua,
        )
