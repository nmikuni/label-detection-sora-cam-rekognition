import os
import requests
import time

import amazon_rekognition
import line_notify
import soracom_api


SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")

REKOGNITION_REGION = os.environ.get("REKOGNITION_REGION")
TARGET_LABEL_NAME = os.environ.get("TARGET_LABEL_NAME")
TARGET_CONFIDENCE = int(os.environ.get("TARGET_CONFIDENCE"))

LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

REQUESTS_TIMEOUT = 5


def lambda_handler(event, context):
    if all([SORACOM_AUTH_KEY_ID, SORACOM_AUTH_KEY,
            DEVICE_ID, REKOGNITION_REGION, TARGET_LABEL_NAME,
            TARGET_CONFIDENCE, LINE_NOTIFY_TOKEN]) is False:
        raise Exception("You didn't set some environment variables")

    print("Begin image export and download.")
    image_url = get_image_url(DEVICE_ID)

    if image_url is None:
        raise Exception("Failed to export image URL.")

    exported_image_bytes = download_image(image_url)
    print("Image downloaded. Detect labels.")
    labels = amazon_rekognition.detect_labels(
        image_bytes=exported_image_bytes,
        rekognition_region=REKOGNITION_REGION)
    print("label list: " + str(labels))
    target_label = amazon_rekognition.find_target_label(
        labels=labels,
        target_label_name=TARGET_LABEL_NAME,
        target_confidence=TARGET_CONFIDENCE)

    if not target_label:
        print("There was no label with target name in the image. Finish the App.")
        return

    if target_label['Instances'] == []:
        notification_image_bytes = exported_image_bytes
    else:
        notification_image_bytes = amazon_rekognition.display_bounding_boxes(
            image_bytes=exported_image_bytes, label=target_label)

    print("Notify to LINE.")
    message_text = 'Found ' + TARGET_LABEL_NAME.lower() + ' in the image.'
    line_notify.notify_to_line_with_image(
        token=LINE_NOTIFY_TOKEN,
        message=message_text,
        image_bytes=notification_image_bytes)
    return


def get_image_url(device_id):
    soracom_api_client = soracom_api.SoracomApiClient(
        coverage_type='jp',
        auth_key_id=SORACOM_AUTH_KEY_ID,
        auth_key=SORACOM_AUTH_KEY)
    export_id = soracom_api_client.export_sora_cam_device_recorded_image(
        device_id=device_id).get("exportId", None)

    if export_id is None:
        print("Failed to export image.")
        return None

    # As the export takes time, need to sleep here
    retry_count = 0
    max_retries = 3
    retry_interval = 1
    while retry_count < max_retries:
        image_url = soracom_api_client.get_sora_cam_device_exported_image(
            device_id=device_id, export_id=export_id).get("url", None)
        if image_url is None:
            retry_count += 1
            time.sleep(retry_interval)
        else:
            return image_url

    print("Failed to export URL.")
    return None


def download_image(image_url):
    image_data_bytes = requests.get(
        image_url, timeout=REQUESTS_TIMEOUT).content
    return image_data_bytes
