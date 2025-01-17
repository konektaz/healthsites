# -*- coding: utf-8 -*-

import logging
import time

from osmapi import (
    OsmApi, ApiError,
    ResponseEmptyApiError, ElementDeletedApiError)
from requests_oauthlib import OAuth2

LOG = logging.getLogger(__name__)


class OAuthTokenMissingError(BaseException):
    """
    Error when oauth token is missing for an authenticated request
    """

    def __init__(self):
        message = 'OAuth token missing'
        super(OAuthTokenMissingError, self).__init__(message)


class OsmApiWrapper(OsmApi, object):

    def __init__(
            self,
            client_key,
            client_secret,
            oauth_token,
            oauth_token_secret,
            api,
            appid):
        """OsmApi wrapper object constructor.
        """
        super(OsmApiWrapper, self).__init__(api=api, appid=appid)
        self._client_key = client_key
        self._client_secret = client_secret
        self._oauth_token = oauth_token
        self._oauth_token_secret = oauth_token_secret

    @staticmethod
    def log_request(method, path):
        """Request logger.

        :param method: HTTP protocol.
        :type method: str

        :param path: Request path.
        :type path: str
        """
        logger_msg = (
            '%s %s %s'
            % (time.strftime('%Y-%m-%d %H:%M:%S'), method, path)
        )
        LOG.info(logger_msg)

    def _http_request(self, method, path, auth, send, return_value=True):
        """
        Returns the response generated by an HTTP request.
        `method` is a HTTP method to be executed
        with the request data. For example: 'GET' or 'POST'.
        `path` is the path to the requested resource relative to the
        base API address stored in self._api. Should start with a
        slash character to separate the URL.
        `auth` is a boolean indicating whether authentication should
        be preformed on this request.
        `send` contains additional data that might be sent in a
        request.
        `return_value` indicates whether this request should return
        any data or not.
        If the oauth token is missing,
        `OAuthTokenMissingError` is raised.
        If the requested element has been deleted,
        `OsmApi.ElementDeletedApiError` is raised.
        If the response status code indicates an error,
        `OsmApi.ApiError` is raised.
        """

        # Add API base URL to path
        path = self._api + path

        user_credentials = None
        if auth:
            try:
                user_credentials = OAuth2(
                    client_id=self._client_key,
                    token={
                        'access_token': self._oauth_token
                    }
                )
            except AttributeError:
                raise OAuthTokenMissingError

        response = self._session.request(
            method, path, auth=user_credentials, data=send
        )
        if response.status_code != 200:
            payload = response.content.strip()
            if response.status_code == 410:
                raise ElementDeletedApiError(
                    response.status_code, response.reason, payload)
            else:
                raise ApiError(response.status_code, response.reason, payload)
        if return_value and not response.content:
            raise ResponseEmptyApiError(
                response.status_code,
                response.reason,
                ''
            )

        self._debug and self.log_request('GET', path)

        return response.content

    @staticmethod
    def changeset_tags(comment, source):
        """Helper to create osm changeset tags.

        :param comment: The changeset comment.
        :type comment: str

        :param comment: The changeset source.
        :type comment: str

        :return: The changeset tags.
        :rtype: dict
        """
        tags = {}
        if not comment:
            raise AssertionError('comment is needed')
        if not source:
            raise AssertionError('source is needed')

        tags.update({
            'comment': comment,
            'source': source
        })
        return tags

    def merge_data(self, current_data, updated_data):
        """ Merging tags from current data to updated data
        if on updated tags is None, delete it

        :param current_data: The current data from OSM
        :type current_data: dict

        :param updated_data: The updated data from HS
        :type updated_data: dict

        :return: merged tags
        :rtype: dict
        """
        if int(current_data['id']) != int(updated_data['id']):
            raise Exception(
                "can't update the healthsite because the data doesn't match with osm")
        current_data['tag'].update(updated_data['tag'])
        updated_data['tag'] = {
            k: v for k, v in current_data['tag'].items() if v is not None
        }
        return updated_data

    def create_node(self, data, comment=None, source=None):
        """Create OSM node data and push it to OSM instance through OSM api.

        :param data: OSM Node data.
        :type data: dict
            example: {
                'lat': latitude of node,
                'lon': longitude of node,
                'tag': {},
            }

        :param comment: Changeset comment.
        :type comment: str

        :param source: Changeset source.
        :type source: str

        :return: OSM changeset data.
        :rtype: dict
            example: {
                'id': id of node,
                'lat': latitude of node,
                'lon': longitude of node,
                'tag': dict of tags,
                'changeset': id of changeset of last change,
                'version': version number of node,
                'user': username of last change,
                'uid': id of user of last change,
                'visible': True|False
            }
        """
        self.ChangesetCreate(
            self.changeset_tags(comment, source))
        changeset = self.NodeCreate(data)
        self.ChangesetClose()

        return changeset

    def update_node(self, data, comment=None, source=None):
        """Update OSM node data and push it to OSM instance through OSM api.

        :param data: OSM Node data.
        :type data: dict
            example: {
                'id': id of node,
                'lat': latitude of node,
                'lon': longitude of node,
                'tag': {},
                'version': version number of node,
            }

        :param comment: Changeset comment.
        :type comment: str

        :param source: Changeset source.
        :type source: str

        :return: OSM changeset data.
        :rtype: dict
            example: {
                'id': id of node,
                'lat': latitude of node,
                'lon': longitude of node,
                'tag': dict of tags,
                'changeset': id of changeset of last change,
                'version': version number of node,
                'user': username of last change,
                'uid': id of user of last change,
                'visible': True|False
            }
        """
        current_data = self.NodeGet(data['id'])
        data = self.merge_data(current_data, data)
        self.ChangesetCreate(
            self.changeset_tags(comment, source))
        changeset = self.NodeUpdate(data)
        self.ChangesetClose()

        return changeset

    def delete_node(self, data, comment=None, source=None):
        """Delete OSM node data through OSM api.

        :param data: OSM Node data.
        :type data: dict
            example: {
                'id': id of node,
                'lat': latitude of node,
                'lon': longitude of node,
                'version': version number of node,
            }

        :param comment: Changeset comment.
        :type comment: str

        :param source: Changeset source.
        :type source: str

        :return: OSM changeset data.
        :rtype: dict
            example: {
                'id': id of node,
                'lat': latitude of node,
                'lon': longitude of node,
                'tag': dict of tags,
                'changeset': id of changeset of last change,
                'version': version number of node,
                'user': username of last change,
                'uid': id of user of last change,
                'visible': True|False
            }
        """
        self.ChangesetCreate(
            self.changeset_tags(comment, source))
        changeset = self.NodeDelete(data)
        self.ChangesetClose()

        return changeset

    def create_way(self, data, comment=None, source=None):
        """Create OSM way data and push it to OSM instance through OSM api.

        :param data: OSM Way data.
        :type data: dict
            example: {
                'nd': [] list of nodes,
                'tag': {} dict of tags,
            }

        :param comment: Changeset comment.
        :type comment: str

        :param source: Changeset source.
        :type source: str

        :return: OSM changeset data.
        :rtype: dict
            example: {
                'id': id of node,
                'nd': [] list of nodes,
                'tag': {} dict of tags,
                'changeset': id of changeset of last change,
                'version': version number of way,
                'user': username of last change,
                'uid': id of user of last change,
                'visible': True|False
            }
        """
        self.ChangesetCreate(
            self.changeset_tags(comment, source))
        changeset = self.WayCreate(data)
        self.ChangesetClose()

        return changeset

    def update_way(self, data, comment=None, source=None):
        """Update OSM way data and push it to OSM instance through OSM api.

        :param data: OSM Way data.
        :type data: dict
            example: {
                'id': id of way,
                'nd': [] list of nodes,
                'tag': {},
                'version': version number of way,
            }

        :param comment: Changeset comment.
        :type comment: str

        :param source: Changeset source.
        :type source: str

        :return: OSM changeset data.
        :rtype: dict
            example: {
                'id': id of node,
                'nd': [] list of nodes,
                'tag': {} dict of tags,
                'changeset': id of changeset of last change,
                'version': version number of way,
                'user': username of last change,
                'uid': id of user of last change,
                'visible': True|False
            }
        """
        current_data = self.WayGet(data['id'])
        data = self.merge_data(current_data, data)
        del data['lat']
        del data['lon']
        self.ChangesetCreate(
            self.changeset_tags(comment, source))
        changeset = self.WayUpdate(data)
        self.ChangesetClose()

        return changeset
