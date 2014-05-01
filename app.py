from flask import Flask, render_template, request, abort
from utils import get_battery_status


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
    capacity, time_left = get_battery_status()
    return render_template(
        'index.html',
        capacity=capacity,
        time_left=time_left
    )


@app.route('/battery/')
def battery():
    if request.is_xhr:
        capacity, time_left = get_battery_status()
        return render_template(
            'battery.html',
            capacity=capacity,
            time_left=time_left
        )
    return abort(404)


if __name__ == '__main__':
    app.run()
