import re
from flask import Flask,Blueprint, render_template, jsonify, request
import time


views = Blueprint('views', __name__)

url_timestamp = {}
url_viewtime = {}
prev_url = ""


def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '') .replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url


@views.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url

    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps11: ", url_timestamp)
    print("final viewtimes22: ", url_viewtime)
    with open('finalviews.txt','a')as f:
        f.write(str(url_viewtime))
        f.write('\n')

    return jsonify({'message': 'success!'}), 200

@views.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200



@views.route('/em/')
def home():
    return render_template("employee.html")

@views.route('/em/breakdown')
def breakpoint():
    return render_template("shift_breakdown.html")

@views.route('/em/shifts')
def shifts():
    return render_template("shifts.html")

@views.route('/em/tasks')
def tasks():
    return render_template("tasks.html")

@views.route('/em/activity')
def activity():
    new_urlViewtime = {k: v for k, v in sorted(url_viewtime.items(), key= lambda v: v[1], reverse=True)}
    return render_template("activity.html", disp = list( new_urlViewtime.items()))


