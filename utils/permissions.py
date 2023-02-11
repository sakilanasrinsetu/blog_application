from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models import UserAccount
from utils.response_wrapper import ResponseWrapper
from django.db.models import Q

User = get_user_model()

class IsCustomAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = 'User Is Not Login'

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False
        # return bool(request.user and request.user.is_authenticated)



class IsSuperAdmin(BasePermission):

    message = 'You Are Not a SuperAdmin.'

    def has_permission(self, request, view):
        if not bool(request.user.is_superuser):
            return False
        else:
            return True


class IsEmployeeOrSuperAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'You Have Not Enough Permission for This Action.'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            qs = UserAccount.objects.filter(Q(is_superuser=True)
                                            or Q(username=request.user, is_employee=True))
        else:
            return False

        if not qs:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            qs = UserAccount.objects.filter(Q(is_superuser=True)
                                            or Q(username=request.user, is_employee=True))
        else:
            return False
        if qs:
            return True
        else:
            return False