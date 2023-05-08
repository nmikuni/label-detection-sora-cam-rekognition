import requests


def notify_to_line_with_image(token, message, image_bytes):
    """Notify the result to LINE"""
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}

    data = {'message': 'message: ' + message}
    files = {'imageFile': image_bytes}
    response = requests.post(
        line_notify_api, headers=headers, data=data, files=files, timeout=5)
    print(response)
