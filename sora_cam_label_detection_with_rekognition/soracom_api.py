import json
import os
import time
from urllib.parse import urljoin

import requests

REQUESTS_TIMEOUT = 5


class SoracomApiClient(object):
    def __init__(self, coverage_type, auth_key_id, auth_key):
        self.request_headers = {'Content-type': 'application/json'}
        # coverage_type should be 'jp' or 'g'.
        self.api_endpoint = "https://%s.api.soracom.io/" % coverage_type
        auth_api_response = self.auth(auth_key_id, auth_key)
        self._api_key = auth_api_response.get("apiKey")
        self._token = auth_api_response.get("token")

        if not self._api_key:
            raise RuntimeError("SORACOM API authentication failed.")

    def auth(self, auth_key_id, auth_key):
        url = urljoin(self.api_endpoint, 'v1/auth')
        payload = json.dumps({
            "authKeyId": auth_key_id,
            "authKey": auth_key
        })

        headers = {"Content-type": "application/json"}

        try:
            response = requests.post(
                url=url, headers=headers, data=payload, timeout=REQUESTS_TIMEOUT)
        except Exception as error:
            print(error)
            raise error

        return response.json()

    def export_sora_cam_device_recorded_image(self, device_id):
        """
        Start the process of exporting still images from recorded video saved by cloud continuous recording
        """
        path = os.path.join('v1/sora_cam/devices/',
                            device_id, 'images/exports')
        url = urljoin(self.api_endpoint, path)
        photo_shoot_time = int(time.time()) * 1000

        headers = {
            "Content-type": "application/json",
            "X-Soracom-API-Key": self._api_key,
            "X-Soracom-Token": self._token,
        }

        payload = {
            "imageFilters": [
                "wide_angle_correction"
            ],
            "time": photo_shoot_time
        }

        try:
            response = requests.post(
                url=url, headers=headers, json=payload, timeout=REQUESTS_TIMEOUT)
        except Exception as error:
            print(error)
            raise error
        return response.json()

    def get_sora_cam_device_exported_image(self, device_id, export_id):
        """
        Get the current status of the process of exporting still images from recorded video taken with a compatible camera device.
        """
        path = os.path.join('v1/sora_cam/devices/',
                            device_id, 'images/exports', export_id)
        url = urljoin(self.api_endpoint, path)

        headers = {
            "Content-type": "application/json",
            "X-Soracom-API-Key": self._api_key,
            "X-Soracom-Token": self._token,
        }

        try:
            response = requests.get(
                url=url, headers=headers, timeout=REQUESTS_TIMEOUT)
        except Exception as error:
            print(error)
            raise error
        return response.json()
