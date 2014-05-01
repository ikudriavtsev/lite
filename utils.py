import os
import platform
from subprocess import Popen, PIPE
import re


# the directory that contains the info about the battery
# should've used `os.path.join` here, but our only target is ubuntu
battery_info_dir = '/sys/class/power_supply/BAT0'


def get_battery_status():
    """Reads the current battery status.
    Returns the capacity, the status of power cord and the time.
    Returns tuple of None if the info is not available.

    :return: tuple of capacity, power cord and time or tuple of None
    :rtype: tuple
    """
    capacity_file_path = battery_info_dir + '/capacity'
    status_file_path = battery_info_dir + '/status'
    if not os.path.isdir(battery_info_dir) or\
       not os.path.exists(capacity_file_path) or\
       not os.path.exists(status_file_path):
        return (None, None)
    battery_time = None
    with open(capacity_file_path, 'r') as f:
        capacity = f.read().strip()
    with open(status_file_path, 'r') as f:
        power_cord = f.read().strip().lower()
        if power_cord not in ('charging', 'discharging'):
            power_cord = 'using a power cord'
        else:
            t = get_battery_time()
            total_mins = t*60
            hours = int(total_mins)/60
            mins = int(total_mins) - hours*60
            hours_label = 'hour' if hours == 1 else 'hours'
            mins_label = 'minute' if mins == 1 else 'minutes'
            battery_time = '%s %s %s %s' % (
                hours,
                hours_label,
                mins,
                mins_label
            )
    return capacity, power_cord, battery_time


def get_battery_time():
    """Returns battery remaining/charging time.
    Uses `upower` shell command.

    :return: battery time to full or time to empty
    :rtype: float or NoneType
    """
    upower = Popen(
        ['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'],
        stdout=PIPE
    )
    grep = Popen(['grep', '-E', 'time\ to'], stdin=upower.stdout, stdout=PIPE)
    std, err = grep.communicate()
    if not err:
        regexp = '^time to \w+:\s+?(\d+,\d+) hours$'
        match = re.match(regexp, std.strip())
        groups = match.groups()
        if groups:
            return float(groups[0].replace(',', '.'))


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
