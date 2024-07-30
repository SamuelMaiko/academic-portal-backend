from a_userauth.models import CustomUser


def get_admins():
    return CustomUser.objects.filter(role='Admin').all()