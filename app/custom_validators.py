import phonenumbers
import zipcodes

from wtforms.validators import ValidationError
from abc import ABC, abstractmethod


class CustomValidator(ABC):
    def __init__(self, message=None):
        self.message = message or self.default_message

    @property
    @abstractmethod
    def default_message(self):
        raise NotImplementedError

    @abstractmethod
    def is_validated(self, form, field):
        return False

    def __call__(self, form, field):
        if not self.is_validated(form, field):
            raise ValidationError(self.message)


class ConfirmEmail(CustomValidator):

    def __init__(self, message=None, email_field_name=None):
        super(ConfirmEmail, self).__init__(message)
        self.email_field_name = email_field_name or "email"

    @property
    def default_message(self):
        return "The emails must match"

    def is_validated(self, form, confirm_email):
        email = form.__getattribute__(self.email_field_name)
        return email.data == confirm_email.data


class Zip(CustomValidator):
    @property
    def default_message(self):
        return "Invalid ZIP Code"

    def is_validated(self, form, zipcode):
        return zipcodes.is_real(zipcode.data)


class Phone(CustomValidator):
    def __init__(self, message=None, region_code="US"):
        super(Phone, self).__init__(message)
        self.region_code = region_code

    @property
    def default_message(self):
        return "Invalid Phone Number"

    def is_validated(self, form, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number.data, self.region_code)
            if not phonenumbers.is_valid_number_for_region(parsed, self.region_code):
                raise ValueError()
        except(ValueError, phonenumbers.phonenumberutil.NumberParseException):
            return False
        return True
