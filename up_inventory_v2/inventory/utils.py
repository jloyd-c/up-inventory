from django.contrib.auth import get_user_model
from inventory.models import HistoryLog
from django.utils import timezone
from ipware import get_client_ip

CustomUser = get_user_model()

def log_action(request, action, model_name, object_id=None, details=""):
    """
    Log an action to the history log
    """
    user = request.user if request.user.is_authenticated else None
    ip_address, _ = get_client_ip(request)
    
    HistoryLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        details=details,
        ip_address=ip_address,
        timestamp=timezone.now()
    )