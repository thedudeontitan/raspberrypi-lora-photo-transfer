from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_detected = db.Column(db.String(255))
    photo_capture = db.Column(db.Text)
    image_name = db.Column(db.String(255))
    time = db.Column(db.String(255))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs', methods=['POST', 'GET'])
def handle_logs():
    if request.method == 'POST':
        data = request.get_json()
        object_detected = data['object_detected']
        photo_capture = data['photo_capture']
        image_name = data['image_name']
        time = data['time']

        log = Log(object_detected=object_detected, photo_capture=photo_capture, image_name=image_name, time=time)
        db.session.add(log)
        db.session.commit()

        return 'Log created successfully'
    elif request.method == 'GET':
        logs = Log.query.all()

        logs_list = []
        for log in logs:
            log_dict = {
                'id': log.id,
                'object_detected': log.object_detected,
                'photo_capture': log.photo_capture,
                'image_name': log.image_name,
                'time': log.time
            }
            logs_list.append(log_dict)

        return {'logs': logs_list}

@app.route('/trigger', methods=['POST'])
def trigger():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Triggered at {current_time}\n"

    try:
        with open('trigger.log', 'a') as file:
            file.write(log_message)
        return 'Triggered successfully'
    except Exception as e:
        return f"An error occurred: {str(e)}"

def initialize_database():
    with app.app_context():
        db.create_all()

def create_trigger_log_file():
    if not os.path.isfile('trigger.log'):
        try:
            with open('trigger.log', 'w') as file:
                file.write('Trigger Log\n')
            print("Created trigger.log file")
        except Exception as e:
            print(f"Failed to create trigger.log file: {str(e)}")

if __name__ == '__main__':
    initialize_database()
    create_trigger_log_file()
    app.run(debug=True)
