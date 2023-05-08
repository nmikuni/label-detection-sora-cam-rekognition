import json
import subprocess
import time


def run_cmd(cmd, arg):
    cmd = cmd + arg
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return res


def export_sora_cam_image_url(device_id, arg):
    """
    Return image URL exported from Soracom Cloud Camera Service.
    The program uses soracom-cli.
    If the code run in Lambda, the soracom-cli should be used by Lambda layer.
    """
    photo_shoot_time = int(time.time()) * 1000
    export_sora_cam_image_cmd = "soracom sora-cam devices images export" \
        + " --image-filters 'wide_angle_correction'" \
        + " --device-id " + device_id + " --time " + str(photo_shoot_time)
    exported_image_info = json.loads(
        run_cmd(cmd=export_sora_cam_image_cmd, arg=arg).stdout.decode())
    export_id = exported_image_info.get("exportId")

    # As the export takes time, need to sleep here
    time.sleep(2)
    get_exported_sora_cam_image_cmd = "soracom sora-cam devices images" \
        + " get-exported --device-id " + device_id \
        + " --export-id " + export_id
    updated_exported_image_info = json.loads(
        run_cmd(cmd=get_exported_sora_cam_image_cmd, arg=arg).stdout.decode())
    image_url = updated_exported_image_info.get("url")
    return image_url
