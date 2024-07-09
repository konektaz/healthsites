__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/05/19'

from xml.dom import minidom

from django.conf import settings
from social_core.backends.openstreetmap_oauth2 import OpenStreetMapOAuth2


class OpenStreetMapDevOAuth(OpenStreetMapOAuth2):
    """OpenStreetMap DEV OAuth authentication backend"""
    AUTHORIZATION_URL = '%s/oauth2/authorize' % settings.OSM_API_URL
    REQUEST_TOKEN_URL = '%s/oauth2/request_token' % settings.OSM_API_URL
    ACCESS_TOKEN_URL = '%s/oauth2/access_token' % settings.OSM_API_URL

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        response = self.oauth_request(
            access_token, '%s/api/0.6/user/details' % settings.OSM_API_URL
        )
        try:
            dom = minidom.parseString(response.content)
        except ValueError:
            return None
        user = dom.getElementsByTagName('user')[0]
        try:
            avatar = dom.getElementsByTagName('img')[0].getAttribute('href')
        except IndexError:
            avatar = None
        return {
            'id': user.getAttribute('id'),
            'username': user.getAttribute('display_name'),
            'account_created': user.getAttribute('account_created'),
            'avatar': avatar
        }
