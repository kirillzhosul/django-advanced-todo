from django.contrib.auth.models import User


def get_asignee_by_id_or_none(req, asignee_id: int) -> tuple[User | None, bool]:
    asignee = None
    if asignee_id == 0:
        asignee = req.user
    elif asignee_id != -1:
        try:
            asignee = User.objects.get(id=asignee_id)
        except User.DoesNotExist:
            return None, False
    return asignee, True
