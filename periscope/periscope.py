# import re
# from flask import Flask, render_template, jsonify, request
# import time

# app = Flask(__name__)

# url_timestamp = {}
# url_viewtime = {}
# prev_url = ""


# def url_strip(url):
#     if "http://" in url or "https://" in url:
#         url = url.replace("https://", '').replace("http://", '') .replace('\"', '')
#     if "/" in url:
#         url = url.split('/', 1)[0]
#     return url


# @app.route('/send_url', methods=['POST'])
# def send_url():
#     resp_json = request.get_data()
#     params = resp_json.decode()
#     url = params.replace("url=", "")
#     print("currently viewing: " + url_strip(url))
#     parent_url = url_strip(url)

#     global url_timestamp
#     global url_viewtime
#     global prev_url

#     print("initial db prev tab: ", prev_url)
#     print("initial db timestamp: ", url_timestamp)
#     print("initial db viewtime: ", url_viewtime)

#     if parent_url not in url_timestamp.keys():
#         url_viewtime[parent_url] = 0

#     if prev_url != '':
#         time_spent = int(time.time() - url_timestamp[prev_url])
#         url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

#     x = int(time.time())
#     url_timestamp[parent_url] = x
#     prev_url = parent_url
#     print("final timestamps: ", url_timestamp)
#     print("final viewtimes: ", url_viewtime)
#     with open('finalviews.txt','a')as f:
#         f.write(str(url_viewtime))
#         f.write('\n')

#     return jsonify({'message': 'success!'}), 200

# @app.route('/quit_url', methods=['POST'])
# def quit_url():
#     resp_json = request.get_data()
#     print("Url closed: " + resp_json.decode())
#     return jsonify({'message': 'quit success!'}), 200




# @app.route("/")
# def employeeHome():
#     return render_template("employee.html")


# @app.route("/shift_breakdown/")
# def employmentShifts():
#     return render_template("shift_breakdown.html")



# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)