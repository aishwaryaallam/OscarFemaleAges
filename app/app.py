from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscarData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'OSCAR Data'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarFemale')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, actors=result)


@app.route('/view/<int:actor_id>', methods=['GET'])
def record_view(actor_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarFemale WHERE fldIndex=%s', actor_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', actor=result[0])


@app.route('/edit/<int:actor_id>', methods=['GET'])
def form_edit_get(actor_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarFemale WHERE fldIndex=%s', actor_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', actor=result[0])


@app.route('/edit/<int:actor_id>', methods=['POST'])
def form_update_post(actor_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldIndex'), request.form.get('fldYear'), request.form.get('fldAge'),
                 request.form.get('fldName'), request.form.get('fldMovie'), actor_id)
    sql_update_query = """UPDATE tblOscarFemale t SET t.fldIndex = %s, t.fldYear = %s, t.fldAge = %s, t.fldName = 
    %s, t.fldMovie = %s WHERE t.fldIndex = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/oscar/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='Oscar Male Form')


@app.route('/oscar/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldIndex'), request.form.get('fldYear'), request.form.get('fldAge'),
                 request.form.get('fldName'), request.form.get('fldMovie'))
    sql_insert_query = """INSERT INTO tblOscarFemale (fldIndex,fldYear,fldAge,fldName,fldMovie) VALUES (%s, %s, %s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:actor_id>', methods=['POST'])
def form_delete_post(actor_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarFemale WHERE fldIndex = %s """
    cursor.execute(sql_delete_query, actor_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscars', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarFemale')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/<int:actor_id>', methods=['GET'])
def api_retrieve(actor_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarFemale WHERE fldIndex=%s', actor_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp



@app.route('/api/v1/oscars/add', methods=['POST'])
def api_add() -> str:
    cursor = mysql.get_db().cursor()
    print("reached before fetching input data")
    content = request.json
    inputData = (content["fldIndex"], content["fldYear"], content["fldAge"],
                 content["fldName"], content["fldMovie"])
    sql_insert_query = """INSERT INTO tblOscarFemale (fldIndex,fldYear,fldAge,fldName,fldMovie) VALUES (%s, %s, %s, %s,%s) """

    print("reached before executing the query")
    cursor.execute(sql_insert_query, inputData)
    print("reached before commit")
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/edit/<int:actor_id>', methods=['PUT'])
def api_edit(actor_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldIndex'], content['fldYear'], content['fldAge'],
                 content['fldName'], content['fldMovie'], actor_id)
    sql_update_query = """UPDATE tblOscarFemale t SET t.fldIndex = %s, t.fldYear = %s, t.fldAge = %s, t.fldName = 
       %s, t.fldMovie = %s WHERE t.fldIndex = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/delete/<int:actor_id>', methods=['DELETE'])
def api_delete(actor_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarFemale WHERE fldIndex = %s """
    cursor.execute(sql_delete_query, actor_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)