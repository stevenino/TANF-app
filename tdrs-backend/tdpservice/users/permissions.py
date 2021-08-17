"""Set permissions for users."""
from collections import ChainMap
from typing import TYPE_CHECKING

from django.apps import apps
from django.db.models import QuerySet
from rest_framework import permissions

if TYPE_CHECKING:
    from django.contrib.auth.models import Permission


def get_permissions_for_model(
    app_label: str,
    model_name: str
) -> QuerySet['Permission']:
    """Retrieve the permissions associated with a given model."""
    # NOTE: We must use the historical version of the model from `apps` to
    #       assert deterministic behavior in both migrations and runtime code.
    return apps.get_model('auth', 'Permission').objects.filter(
        content_type__app_label=app_label,
        content_type__model=model_name
    )


def is_own_stt(request, view):
    """Verify user belongs to requested STT."""
    is_data_analyst = is_in_group(request.user, 'Data Analyst')

    # Depending on the request, the STT could be found in three different places
    # so we will merge all together and just do one check
    request_parameters = ChainMap(
        view.kwargs,
        request.query_params,
        request.data
    )
    requested_stt = request_parameters.get('stt')
    user_stt = request.user.stt_id if hasattr(request.user, 'stt_id') else None

    return bool(
        is_data_analyst and
        user_stt is not None and
        (requested_stt in [None, str(user_stt)])
    )


def is_in_group(user, group_name):
    """Take a user and a group name, and returns `True` if the user is in that group."""
    return user.groups.filter(name=group_name).exists()


class IsUser(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """Check if user has required permissions."""
        return obj == request.user


class IsAdmin(permissions.BasePermission):
    """Permission for admin-only views."""

    def has_object_permission(self, request, view, obj):
        """Check if a user is admin or superuser."""
        return request.user.is_authenticated and request.user.is_admin

    def has_permission(self, request, view):
        """Check if a user is admin or superuser."""
        return request.user.is_authenticated and request.user.is_admin


class IsOFAAdmin(permissions.BasePermission):
    """Permission for OFA Analyst only views."""

    def has_permission(self, request, view):
        """Check if a user is a OFA Admin."""
        return is_in_group(request.user, "OFA Admin")


class IsDataAnalyst(permissions.BasePermission):
    """Permission for Data Analyst only views."""

    def has_permission(self, request, view):
        """Check if a user is a data analyst."""
        return is_in_group(request.user, "Data Analyst")


class DataFilePermissions(permissions.BasePermission):
    """Permission for data file downloads & uploads."""

    def has_permission(self, request, view):
        """Check if a user is a data analyst or an admin.

        If they are a data analyst, ensures the STT is their own.
        """
        return (
            is_in_group(request.user, "OFA Admin") or
            is_own_stt(request, view)
        )

    def has_object_permission(self, request, view, obj):
        """Check if a user can interact with a specific file, based on STT.

        This is used in cases where we call .get_object() to retrieve a data_file
        and do not have the STT available in the request, ie. data file was
        requested for download via the ID of the data_file. This is not called
        on POST requests (creating new data_files) or for a list of data_files.
        """
        is_ofa_admin = is_in_group(request.user, "OFA Admin")
        is_data_analyst = is_in_group(request.user, 'Data Analyst')
        user_stt = request.user.stt_id if hasattr(request.user, 'stt_id') else None

        return is_ofa_admin or (is_data_analyst and user_stt == obj.stt_id)
