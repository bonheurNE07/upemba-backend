import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class AlertService:
    @staticmethod
    def trigger_critical_alert(equipment_name, score, timestamp):
        """
        Sends an email alert to the configured park rangers/admins
        regarding a CRITICAL equipment health status, using both
        plain-text and rich HTML formatting.
        """
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning("SMTP credentials not provided. Skipping email dispatch.")
            return

        subject = f"CRITICAL ALERT: {equipment_name} Failure Predicted"

        # Plain-text fallback message
        message = (
            f"URGENT: Upemba Predictive Maintenance System has flagged "
            f"a Critical Health Status for '{equipment_name}'.\n\n"
            f"Detection Timestamp: {timestamp}\n"
            f"Anomaly Score: {score}\n\n"
            f"Immediate physical inspection by field rangers is heavily recommended."
        )

        # Render the rich HTML responsive email template
        context = {
            "equipment_name": equipment_name,
            "score": score,
            "timestamp": timestamp,
        }
        html_message = render_to_string("telemetry/email/critical_alert.html", context)

        # Default to ADMINS if available
        recipient_list = [admin[1] for admin in settings.ADMINS]
        if not recipient_list:
            logger.warning("No ADMINS configured to receive critical alerts.")
            return

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Critical HTML alert email successfully dispatched to {recipient_list}")
        except Exception as e:
            logger.exception(f"Failed to send critical HTML alert email: {e}")
