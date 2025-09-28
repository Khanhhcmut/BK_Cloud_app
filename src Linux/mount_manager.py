import subprocess
import time
import os
import sys
import tempfile
from secure_json import secure_json_load, secure_json_dump

MOUNT_POINT = os.path.expanduser("~/BKcloud")
rclone_process = None

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_remote_name(user):
    return f"bkcloud_{user}".replace(" ", "_").lower()

def save_rclone_config(user, password, project, auth_url):
    remote_name = get_remote_name(user)
    cleaned_auth_url = auth_url.replace("/auth/tokens", "").rstrip("/")

    config = f"""
[{remote_name}]
type = swift
user = {user}
key = {password}
auth = {cleaned_auth_url}
tenant = {project}
domain = default
tenant_domain = default
endpoint_type = public
region = RegionOne
""".strip()

    secure_json_dump(config, "rclone.sec")

def mount_drive(user, password, project, auth_url):
    global rclone_process
    unmount_drive()

    # Giả định rclone đã có trong PATH (/usr/bin/rclone)
    rclone_bin = "rclone"

    remote_name = get_remote_name(user)
    conf_data = secure_json_load("rclone.sec")

    if not conf_data:
        save_rclone_config(user, password, project, auth_url)
        conf_data = secure_json_load("rclone.sec")

    # Đảm bảo thư mục mount tồn tại
    os.makedirs(MOUNT_POINT, exist_ok=True)

    # Viết config tạm
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".conf") as tmp_conf:
        tmp_conf.write(conf_data)
        tmp_conf_path = tmp_conf.name

    try:
        rclone_process = subprocess.Popen(
            [
                rclone_bin, "mount", f"{remote_name}:", MOUNT_POINT,
                "--config", tmp_conf_path,
                "--vfs-cache-mode", "full",
                "--dir-cache-time", "1s"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
    finally:
        try:
            os.remove(tmp_conf_path)  # Xóa file tạm
        except:
            pass

def unmount_drive():
    global rclone_process
    if os.path.ismount(MOUNT_POINT):
        # Thử fusermount trước, nếu không có thì fallback sang umount
        try:
            subprocess.call(["fusermount", "-u", MOUNT_POINT])
        except FileNotFoundError:
            subprocess.call(["umount", MOUNT_POINT])
    rclone_process = None
