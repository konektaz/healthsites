__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/05/19'

from django.conf import settings
from social_core.backends.openstreetmap_oauth2 import OpenStreetMapOAuth2


class OpenStreetMapDevOAuth(OpenStreetMapOAuth2):
    """OpenStreetMap DEV OAuth authentication backend"""

    AUTHORIZATION_URL = f'{settings.OSM_API_URL}/oauth2/authorize'
    ACCESS_TOKEN_URL = f'{settings.OSM_API_URL}/oauth2/token'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""

        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.get_json(
            url=f"{settings.OSM_API_URL}/api/0.6/user/details.json",
            headers=headers,
        )

        return {
            "id": response["user"]["id"],
            "username": response["user"]["display_name"],
            "account_created": response["user"]["account_created"],
            "avatar": response["user"].get("img", {}).get("href"),
        }
