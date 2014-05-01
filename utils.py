import os
import platform


# the directory that contains the info about the battery
# should've used `os.path.join` here, but our only target is ubuntu
battery_info_dir = '/sys/class/power_supply/BAT0'


def get_battery_status():
    """Reads the current battery status.
    Returns the capacity and time left.
    Returns None as time left if using a power cord.
    Returns None if the info is not available.

    :return: tuple of capacity and time left or None
    :rtype: tuple or None
    """
    capacity_file_path = battery_info_dir + '/capacity'
    if not os.path.isdir(battery_info_dir) or not os.path.exists(capacity_file_path):
        return
    with open(capacity_file_path, 'r') as f:
        capacity = f.read().strip()
    return capacity, None


def is_ubuntu():
    """Whether the current os is Ubuntu.

    :return: True or False
    :rtype: boolean
    """
    return platform.linux_distribution()[0] == 'Ubuntu'
