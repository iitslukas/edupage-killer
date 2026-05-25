import pytest
from django.db import IntegrityError

from apps.accounts.models import SchoolClass, User


class TestUserFullName:
    def test_full_name_with_both_names(self) -> None:
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        assert user.full_name == "John Doe"

    def test_full_name_with_first_name_only(self) -> None:
        user = User(first_name="John", last_name="", email="john@example.com")
        assert user.full_name == "John"

    def test_full_name_falls_back_to_email(self) -> None:
        user = User(first_name="", last_name="", email="john@example.com")
        assert user.full_name == "john@example.com"


@pytest.mark.django_db
class TestSchoolClass:
    def test_duplicate_name_and_year_raises(self) -> None:
        SchoolClass.objects.create(name="1A", grade=1, year=2024)
        with pytest.raises(IntegrityError):
            SchoolClass.objects.create(name="1A", grade=1, year=2024)

    def test_same_name_different_year_is_allowed(self) -> None:
        SchoolClass.objects.create(name="1A", grade=1, year=2024)
        sc = SchoolClass.objects.create(name="1A", grade=1, year=2025)
        assert sc.pk is not None
