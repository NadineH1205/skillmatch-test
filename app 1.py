from flask import Flask, render_template, request, jsonify
import pymysql.cursors

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': '',
    'cursorclass': pymysql.cursors.DictCursor
}

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle AJAX request for trainee data
@app.route('/api/trainees')
def get_trainees():
    academy_id = request.args.get('academy')
    stream_id = request.args.get('stream')
    course_id = request.args.get('course')

    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT t.name
                FROM trainees t
                INNER JOIN exam_results e ON t.trainee_id = e.trainee_id
                WHERE t.academy_id = %s
                AND t.stream_id = %s
                AND e.course_id = %s
                AND e.score > 75
            """
            cursor.execute(sql, (academy_id, stream_id, course_id))
            trainees = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(trainees)

# Route to handle AJAX request for academies data
@app.route('/api/academies')
def get_academies():
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT academy_id, city FROM academies"
            cursor.execute(sql)
            academies = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(academies)

# Route to handle AJAX request for streams data
@app.route('/api/streams')
def get_streams():
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT stream_id, name FROM streams"
            cursor.execute(sql)
            streams = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(streams)

# Route to handle AJAX request for courses data
@app.route('/api/courses')
def get_courses():
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_id, name FROM courses"
            cursor.execute(sql)
            courses = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(courses)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
