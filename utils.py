import os
import platform


# the directory that contains the info about the battery
# should've used `os.path.join` here, but our only target is ubuntu
battery_info_dir = '/sys/class/power_supply/BAT0'


def get_battery_status():
    """Reads the current battery status.
    Returns the capacity and the status of power cord.
    Returns tuple of None if the info is not available.

    :return: tuple of capacity and power cord or tuple of None
    :rtype: tuple
    """
    capacity_file_path = battery_info_dir + '/capacity'
    status_file_path = battery_info_dir + '/status'
    if not os.path.isdir(battery_info_dir) or\
       not os.path.exists(capacity_file_path) or\
       not os.path.exists(status_file_path):
        return (None, None)
    with open(capacity_file_path, 'r') as f:
        capacity = f.read().strip()
    with open(status_file_path, 'r') as f:
        power_cord = f.read().strip().lower()
        if power_cord not in ('charging', 'discharging'):
            power_cord = 'using a power cord'
    return capacity, power_cord


def is_batery_present():
    """Determines whether the battery is plugged in.

    :return: True or False
    :rtype: boolean
    """
    present_file_path = battery_info_dir + '/present'
    if not os.path.isdir(battery_info_dir) or\
       not os.path.exists(present_file_path):
        return False
    with open(present_file_path, 'r') as f:
        present = f.read().strip()
    return bool(int(present))


def is_ubuntu():
    """Whether the current os is Ubuntu.

    :return: True or False
    :rtype: boolean
    """
    return platform.linux_distribution()[0] == 'Ubuntu'
