import os
import platform


# the directory that contains the info about the battery
# should've used `os.path.join` here, but our only target is ubuntu
battery_info_dir = '/sys/class/power_supply/BAT0'


def get_battery_status():
    """Reads the current battery status.
    Returns the capacity and if using a power cord.
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
        power_cord = f.read().strip() != 'Discharging'
    return capacity, power_cord


def is_ubuntu():
    """Whether the current os is Ubuntu.

    :return: True or False
    :rtype: boolean
    """
    return platform.linux_distribution()[0] == 'Ubuntu'
