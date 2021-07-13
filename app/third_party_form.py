from abc import ABC
import requests
from lxml import html

from config import Config

CONFIG = Config()


class ThirdPartyForm(ABC):
    def __init__(
            self, flask_form, form_name, next_form=None):
        """
        Adaptor for multipart third-party complaint submission form
        :param flask_form: Flask-WTF instance
        :param form_name: indicates where in config to get various details and mappings
        :param next_form: if present, continue to next form and repeat process again
        """
        self.flask_form = flask_form
        self.form_name = form_name
        self.url = CONFIG.remote_form_urls[form_name]
        if next_form is not None:
            self.next_form = next_form(flask_form)
        else:
            self.next_form = None
        self.static_fields = CONFIG.remote_form_hardcoded.get(form_name, {})
        self.mapping = CONFIG.remote_form_mapping.get(form_name, {})
        self.field_id_map = CONFIG.remote_form_by_id.get(form_name, {})

    def get_confirmation(self, tree):
        return tree.xpath("//span[@id='complaintNumber']")[0].text

    def construct_post_data(self, tree):
        post_data = self.static_fields or {}
        for field_name, value in self.map_from_form().items():
            post_data[field_name] = value
        for field_name, value in self.map_from_tree(tree).items():
            post_data[field_name] = value
        return post_data

    def map_from_tree(self, tree):
        data = {}
        for field_name, field_id in self.field_id_map.items():
            data[field_name] = str(tree.xpath(f"//input[@id='{field_id}']/@value")[0])
        return data

    def map_from_form(self):
        data = {}
        for local_name, remote_name in self.mapping.items():
            if not isinstance(remote_name, list):
                remote_name = [remote_name]
                for rn in remote_name:
                    form_response = self.flask_form.data[local_name]
                    if isinstance(form_response, bool) and local_name != "anonymous":
                        form_response = "on" if form_response else "off"
                    if isinstance(form_response, float):
                        form_response = round(form_response, 4)
                    data[rn] = form_response
        return data

    def get_response(self, post_data=None):
        if post_data is None:
            response = requests.get(self.url)
        else:
            response = requests.post(self.url, post_data)
        tree = html.fromstring(response.content)
        if self.next_form is None:
            return self.get_confirmation(tree)
        new_post_data = self.construct_post_data(tree)
        return self.next_form.get_response(new_post_data)


class ThirdPartyContactForm(ThirdPartyForm):
    def __init__(self, flask_form):
        super(ThirdPartyContactForm, self).__init__(
            flask_form, form_name="complaint_contact"
        )


class ThirdPartyDetailForm(ThirdPartyForm):
    def __init__(self, flask_form):
        super(ThirdPartyDetailForm, self).__init__(
            flask_form,
            form_name="complaint_detail",
            next_form=ThirdPartyContactForm,
        )


class ThirdPartyPollutionTypeForm(ThirdPartyForm):
    def __init__(self, flask_form):
        super(ThirdPartyPollutionTypeForm, self).__init__(
            flask_form,
            form_name="choose_air",
            next_form=ThirdPartyDetailForm
        )


class ThirdPartyReport(ThirdPartyForm):
    def __init__(self, flask_form):
        super(ThirdPartyReport, self).__init__(
            flask_form,
            form_name="start_complaint",
            next_form=ThirdPartyPollutionTypeForm
        )
