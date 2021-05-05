"""Globally available pytest fixtures."""
from io import StringIO
from tempfile import NamedTemporaryFile
import uuid

from django.contrib.auth.models import Group
from factory.faker import faker
from rest_framework.test import APIClient
import pytest

from tdpservice.reports.test.factories import ReportFileFactory
from tdpservice.stts.test.factories import STTFactory, RegionFactory
from tdpservice.users.test.factories import (
    UserFactory,
    AdminUserFactory,
    StaffUserFactory,
    STTUserFactory,
    InactiveUserFactory
)

_faker = faker.Faker()


@pytest.fixture(scope="function")
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def user():
    """Return a basic, non-admin user."""
    return UserFactory.create()


@pytest.fixture
def stt_user():
    """Return a user without an STT for STT tests."""
    return STTUserFactory.create()


@pytest.fixture
def ofa_admin():
    """Return an ofa admin user."""
    return UserFactory.create(groups=(Group.objects.get(name="OFA Admin"),))


@pytest.fixture
def data_prepper():
    """Return a data prepper user."""
    return UserFactory.create(groups=(Group.objects.get(name="Data Prepper"),))


@pytest.fixture
def admin_user():
    """Return an admin user."""
    return AdminUserFactory.create()


@pytest.fixture
def staff_user():
    """Return a staff user."""
    return StaffUserFactory.create()


@pytest.fixture
def inactive_user():
    """Return an inactive user."""
    return InactiveUserFactory.create()


@pytest.fixture
def stt():
    """Return an STT."""
    return STTFactory.create()


@pytest.fixture
def region():
    """Return a region."""
    return RegionFactory.create()


@pytest.fixture
def fake_file_name():
    """Generate a random, but valid file name ending in .txt."""
    return _faker.file_name(extension='txt')


@pytest.fixture
def fake_file():
    """Generate an in-memory file-like object with random contents."""
    return StringIO(_faker.sentence())


@pytest.fixture
def infected_file():
    """Generate an EICAR test file that will be treated as an infected file.
    https://en.wikipedia.org/wiki/EICAR_test_file
    """
    return StringIO(
        r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
    )


def create_temporary_file(
    file_contents: str,
    suffix: str = '.txt'
) -> NamedTemporaryFile:
    file = NamedTemporaryFile(suffix=suffix)
    file_contents_bytes = str.encode(file_contents)
    file.write(file_contents_bytes)
    file.seek(0)

    return file


@pytest.fixture
def data_file(fake_file):
    return create_temporary_file(fake_file.read())


@pytest.fixture
def other_data_file(fake_file):
    fake_file.seek(0)
    return create_temporary_file(fake_file.read())


@pytest.fixture
def infected_data_file(infected_file):
    return create_temporary_file(infected_file.read())


@pytest.fixture
def report():
    """Return a report file."""
    return ReportFileFactory.create()
