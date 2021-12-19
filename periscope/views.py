import re
from flask import Flask,Blueprint, render_template, jsonify, request, redirect, url_for
import time
from flask_login import login_required,  current_user
from sqlalchemy.sql.functions import user
from . models import Employee, Tasks, Supervisor, Admin, Shift
from . import db
import json
from datetime import datetime, date  
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
@login_required
def home():
    return render_template("employee.html")



@views.route('/em/shifts')
def shifts():
    return render_template("shifts.html")



@views.route('/em/activity')
def activity():
    new_urlViewtime = {k: v for k, v in sorted(url_viewtime.items(), key= lambda v: v[1], reverse=True)}
    site_list = new_urlViewtime.values()
    site_sum = sum(site_list)
    for k, v in new_urlViewtime.items():
        if site_sum > 0:
            new_urlViewtime[k] = round(v / site_sum * 100)

    x = list(new_urlViewtime.keys())
    y = list(new_urlViewtime.values())
    activity = 0
    allowed_urls = ['127.0.0.1:5000','extractor.hubdoc.com','stackoverflow.com']
    for url in allowed_urls:
        if url in x:
            activity += y[x.index(url)]
            if activity > 100:
                activity = 100

    
    return render_template("activity.html",new_urlViewtime=new_urlViewtime, disp = list( new_urlViewtime.items()),x=x, y=y, activity=activity)
    
@views.route('/em/breakdown', methods=['GET', 'POST'])
def breakdown():

    new_urlViewtime = {k: v for k, v in sorted(url_viewtime.items(), key= lambda v: v[1], reverse=True)}
    site_list = new_urlViewtime.values()
    site_sum = sum(site_list)
    for k, v in new_urlViewtime.items():
        if site_sum > 0:
            new_urlViewtime[k] = round(v / site_sum * 100)

    x = list(new_urlViewtime.keys())
    y = list(new_urlViewtime.values())
    activity = 0
    allowed_urls = ['127.0.0.1:5000','extractor.hubdoc.com','stackoverflow.com']
    for url in allowed_urls:
        if url in x:
            activity += y[x.index(url)]
            if activity > 100:
                activity = 100
    disp = list( new_urlViewtime.items())
    today = date.today().isoformat()
    today = datetime.strptime(today, '%Y-%m-%d')



    new_activity = Shift(activity_score=activity, employee_id=int(current_user.get_id()), sites= str(disp))
    # submit = False
    if request.method == 'POST':
            print("We are here!!!!!!!")
            db.session.add(new_activity)
            db.session.commit()
            print(f"added activity {new_activity}")
            return redirect(url_for('views.home'))


    return render_template("shift_breakdown.html")

@views.route('/sup/')
def sup_home():
    return render_template("supervisor.html")



@views.route('/sup/employees')
def sup_employees():
    employees = db.session.query(Employee)

    return render_template("employeeList.html", employees=employees)



@views.route('/sup/tasks', methods=['GET', 'POST'])
def create_tasks():
    employees = db.session.query(Employee)
    if request.method == 'POST':
        task = request.form.get('task')
        employeeId = request.form.get('employeeId')
        # date = datetime(int(request.form.get('date')))
        date = request.form.get('date')
        date = datetime.strptime(date, '%Y-%m-%d')
        

        new_task = Tasks(data=task, user_id=employeeId, date = date)
        
        db.session.add(new_task)
        db.session.commit()
    tasksList = db.session.query(Tasks)

    return render_template("create_tasks.html", employee = current_user, employees = employees, tasksList = tasksList)

@views.route('/em/tasks')
def tasks():
    tasksList = db.session.query(Tasks)
    user_id=current_user.id
    today = date.today().isoformat()

    return render_template("tasks.html", tasksList = tasksList, user_id=user_id, today=today)


@views.route('/sup/activity' )
def sup_activity():
    shiftdata = db.session.query(Shift)
    employee = db.session.query(Employee)

    return render_template("sup_activity.html", shiftdata= shiftdata, employee=employee)


@views.route('/admin/')
def admin_home():
    return render_template("admin.html")


@views.route('/admin/reports')
def admin_reports():
    return render_template("reports.html")


@views.route('/admin/reports/employees')
def employees_report():
    employees = db.session.query(Employee)
    return render_template("employees_reports.html",employees=employees)

@views.route('/admin/reports/activity')
def activity_report():
    shiftdata = db.session.query(Shift)
    employee = db.session.query(Employee)
    return render_template("activity_reports.html",shiftdata= shiftdata, employee=employee)

@views.route('/admin/reports/shift')
def shift_report():
    shiftdata = db.session.query(Shift)
    employee = db.session.query(Employee)
    return render_template("shift_reports.html",shiftdata= shiftdata, employee=employee)


@views.route('/admin/reports/tasks')
def tasks_report():
    tasksList = db.session.query(Tasks)
    employee = db.session.query(Employee)
    return render_template("tasks_reports.html",tasksList=tasksList, employee=employee)



# @views.route('/delete-task', methods=['POST'])
# def delete_task():
#     task = json.loads(request.data)
#     taskId = task['taskId']
#     note = Tasks.query.get(taskId)
#     if task:
#             db.session.delete(task)
#             db.session.commit()
#     return jsonify({})


