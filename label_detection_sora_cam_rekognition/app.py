import os
import requests

import amazon_rekognition
import line_notify
import soracom_cli


SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
SORACOM_CLI_ARG = ' --auth-key-id ' + SORACOM_AUTH_KEY_ID + \
    ' --auth-key ' + SORACOM_AUTH_KEY

REKOGNITION_REGION = os.environ.get("REKOGNITION_REGION")
TARGET_LABEL_NAME = os.environ.get("TARGET_LABEL_NAME")
TARGET_CONFIDENCE = int(os.environ.get("TARGET_CONFIDENCE"))

LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")


def lambda_handler(event, context):
    print("Begin image export and download.")
    image_url = soracom_cli.export_sora_cam_image_url(
        device_id=DEVICE_ID, arg=SORACOM_CLI_ARG)
    exported_image_bytes = download_image(image_url)
    print("Image downloaded. Detect labels.")
    labels = amazon_rekognition.detect_labels(
        image_bytes=exported_image_bytes, rekognition_region=REKOGNITION_REGION)
    print("label list: " + str(labels))
    target_label = amazon_rekognition.find_target_label(
        labels=labels, target_label_name=TARGET_LABEL_NAME, target_confidence=TARGET_CONFIDENCE)

    if not target_label:
        print("There was no label with target name in the image. Finish the App.")
        return

    if target_label['Instances'] == []:
        notification_image_bytes = exported_image_bytes
    else:
        notification_image_bytes = amazon_rekognition.display_bounding_boxes(
            image_bytes=exported_image_bytes, label=target_label)

    line_notify.notify_to_line(
        token=LINE_NOTIFY_TOKEN, label_name=TARGET_LABEL_NAME, image_bytes=notification_image_bytes)
    return


def download_image(image_url):
    image_data_bytes = requests.get(image_url).content
    return image_data_bytes


if __name__ == '__main__':
    lambda_handler("hoo", "bar")
