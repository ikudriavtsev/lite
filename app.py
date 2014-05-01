from flask import Flask, render_template, request, abort
from utils import get_battery_status, is_batery_present


app = Flask(__name__)
app.config.from_object(__name__)
# default config
app.config.update(dict(
    # common settings
    DEBUG=True,
    # battery status update period, in ms
    BATTERY_STATUS_UPDATE_PERIOD=2*60*1000,  # 2 mins
))


@app.route('/')
def index():
    present = is_batery_present()
    if not present:
        capacity, power_cord, battery_time = None, None, None
    else:
        capacity, power_cord, battery_time = get_battery_status()
    return render_template(
        'index.html',
        capacity=capacity,
        power_cord=power_cord,
        present=present,
        battery_time=battery_time
    )


@app.route('/battery/')
def battery():
    if request.is_xhr:
        present = is_batery_present()
        if not present:
            capacity, power_cord, battery_time = None, None, None
        else:
            capacity, power_cord, battery_time = get_battery_status()
        return render_template(
            'battery.html',
            capacity=capacity,
            power_cord=power_cord,
            present=present,
            battery_time=battery_time
        )
    return abort(404)


if __name__ == '__main__':
    app.run()
