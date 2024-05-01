from flask import Flask, render_template, request, jsonify
import pymysql.cursors

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host':'skillmatch-mysql.mysql.database.azure.com',
    'user':'skillmatch',
    'password':'FDMgroup2024',
    'database':'skillmatch',
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
    score = request.args.get('score')
    sort = request.args.get('sort')

    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:

            #if any academy is selected
            if academy_id == "any":
                academy_id = 't.academy_id'
            else:
                academy_id = "t.academy_id = %s"% academy_id

            #if any stream selected
            if stream_id == "any":
                stream_id = 't.stream_id'
            else:
                stream_id = "t.stream_id = %s"% stream_id

            #if any course selected
            if course_id == "any":
                course_id = 'e.course_id'
            else:
                course_id = "e.course_id = %s"% course_id

            #if no score is selected
            if score == '':
                score=75

            if sort == 'Name':
                sort="ORDER BY t.name ASC"
            elif sort == 'Score':
                sort="HAVING AVG(e.score)\nORDER BY AVG(e.score)"
            else:
                sort=""
            
            sql = """
                    SELECT t.name
                    FROM trainees t
                    INNER JOIN exam_results e ON t.trainee_id = e.trainee_id
                    WHERE %s
                    AND %s
                    AND %s
                    AND e.score >= %s
                    GROUP BY t.name
                    %s
                """% (academy_id, stream_id, course_id, score, sort)
            cursor.execute(sql)
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
