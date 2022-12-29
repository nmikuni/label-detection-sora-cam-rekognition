import requests


def notify_to_line(token, label_name, image_bytes):
    """Notify the result to LINE"""
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}

    message = 'Found ' + label_name.lower() + ' in the image.'

    data = {'message': 'message: ' + message}
    files = {'imageFile': image_bytes}
    response = requests.post(
        line_notify_api, headers=headers, data=data, files=files)
    print(response)
