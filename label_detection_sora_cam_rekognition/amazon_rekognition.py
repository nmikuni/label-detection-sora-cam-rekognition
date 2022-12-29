import io

import boto3
from PIL import Image, ImageDraw


def detect_labels(image_bytes, rekognition_region):
    """Returns detected labels in an image using Amazon Rekognition"""
    client = boto3.client('rekognition', rekognition_region)
    response = client.detect_labels(Image={'Bytes': image_bytes})
    return response['Labels']


def find_target_label(labels, target_label_name, target_confidence):
    """Returns a label with a specific name and high confidence from a list of labels"""
    for label in labels:
        if label['Name'] == target_label_name and label['Confidence'] > target_confidence:
            print("Found " + target_label_name + " in the image")
            return label
    print("There was no " + target_label_name + " in the image")
    return


def display_bounding_boxes(image_bytes, label):
    """Returns a image with bounding boxes using detected label"""
    image = Image.open(io.BytesIO(image_bytes))
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    for instance in label['Instances']:
        box = instance["BoundingBox"]
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']
        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)

        )
        draw.line(points, fill='#00d400', width=2)
    image_with_boxes_jpg = io.BytesIO()
    image.save(image_with_boxes_jpg, format='JPEG')
    image_with_boxes_bytes = image_with_boxes_jpg.getvalue()

    return image_with_boxes_bytes
