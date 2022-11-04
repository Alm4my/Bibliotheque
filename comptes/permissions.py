def is_staff(user):
    return user.is_active and user.is_staff
