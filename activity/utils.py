import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from activity.models import Action


def create_action(user, verb, target=None):
    # Define a shortcut method to create new action and set target to none by default since it is needed in only generic
    now = timezone.now()
    last_minute = now = datetime.timedelta(seconds=60)
    # Prevent repetitive actions within short period of time
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created_at__gte=last_minute)
    if target:
        target_content_type = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_content_type=target_content_type, target_id=target.id)
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
