"""Validator functions which may be assigned to model fields."""
import logging
import re

from django.core.exceptions import ValidationError
from inflection import pluralize

from tdpservice.clients import ClamAVClient

logger = logging.getLogger(__name__)

# The default set of Extensions allowed for an uploaded file
# Supports regex patterns as defined by standard library
# https://docs.python.org/3/library/re.html#regular-expression-syntax
ALLOWED_FILE_EXTENSIONS = [
    r'^(ms\d{2})$',  # Files ending in .MS## where # is a digit 0-9
    r'^(ts\d{2,3})$',  # Files ending in .TS## or .TS### where # is a digit 0-9
    'txt',  # plain text files
]

# The default set of Content Types allowed for an uploaded file
ALLOWED_FILE_CONTENT_TYPES = [
    'text/plain',
]


def _get_unsupported_msg(_type, value, supported_options):
    """Construct a message to convey an unsupported operation."""
    return (
        f'Unsupported {_type}: {value}, supported {pluralize(_type)} '
        f'are: {supported_options}'
    )


def validate_file_content_type(file):
    """Validate the content type of a file is in our supported list."""
    file_content_type = file.content_type

    if file_content_type not in ALLOWED_FILE_CONTENT_TYPES:
        msg = _get_unsupported_msg(
            'file content type',
            file_content_type,
            ALLOWED_FILE_CONTENT_TYPES
        )
        raise ValidationError(msg)


def validate_file_extension(file_name: str):
    """Validate the file extension of a file is in our supported list."""
    file_extension = (
        file_name.split('.')[-1].lower() if '.' in file_name else None
    )

    allowed_ext_patterns = '|'.join(ALLOWED_FILE_EXTENSIONS)
    if (
        file_extension is not None
        and not re.match(allowed_ext_patterns, file_extension)
    ):
        msg = _get_unsupported_msg(
            'file extension',
            file_extension,
            ALLOWED_FILE_EXTENSIONS
        )
        raise ValidationError(msg)


def validate_file_infection(file):
    """Validate file is not infected by scanning with ClamAV."""
    av_client = ClamAVClient()
    try:
        is_file_clean = av_client.scan_file(file, file.name)
    except ClamAVClient.ServiceUnavailable:
        raise ValidationError(
            'Unable to complete security inspection, please try again or '
            'contact support for assistance'
        )

    if not is_file_clean:
        raise ValidationError(
            'Rejected: uploaded file did not pass security inspection'
        )


def validate_data_file(file):
    """Perform all validation steps on a given file."""
    validate_file_extension(file.name)
    validate_file_content_type(file)
    validate_file_infection(file)
