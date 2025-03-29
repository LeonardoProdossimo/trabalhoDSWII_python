import pymysql
from db_config import connect_db
from flask import flash, request, Blueprint
from flask import jsonify


time_bp = Blueprint('times', __name__)

@time_bp.route('/time')
def time():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM time_futebol")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@time_bp.route('/time/<int:id>')
def timebyid(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM time_futebol WHERE idtime=" + str(id))
        row = cursor.fetchall()
        resp = jsonify(row[0])
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@time_bp.route('/time/pesquisa/<string:pesquisa>')
def timebypesquisa(pesquisa):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM time_futebol WHERE nome LIKE %s", (f"%{pesquisa}%",))
        row = cursor.fetchall()
        resp = jsonify(row[0])
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@time_bp.route('/time', methods=['POST'])
def add_time():
    try:
        _json = request.json
        _nome = _json['nome']
        _cidade = _json['cidade']
        _estado = _json['estado'] 
        _fundacao = _json['fundacao']
        _estadio = _json['estadio']

        if _nome and _cidade and _estado and _fundacao and _estadio and request.method == 'POST':
            sqlQuery = "INSERT INTO time_futebol(nome, cidade, estado, fundacao, estadio) VALUES(%s, %s, %s, %s, %s)"
            data = (_nome, _cidade, _estado, _fundacao, _estadio)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, data)
            conn.commit()
            resp = jsonify('Time de futebol adicionado com sucesso!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@time_bp.route('/time/<int:id>', methods=['PUT'])
def update_time(id):
    try:
        _json = request.json
        _nome = _json['nome']
        _cidade = _json['cidade']
        _estado = _json['estado'] 
        _fundacao = _json['fundacao']
        _estadio = _json['estadio']

        if _nome and _cidade and _estado and _fundacao and _estadio and request.method == 'PUT':
            sqlQuery = "UPDATE time_futebol SET nome=%s, cidade=%s, estado=%s, fundacao=%s, estadio=%s WHERE idtime=%s"
            data = (_nome, _cidade, _estado, _fundacao, _estadio, id)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, data)
            conn.commit()
            resp = jsonify('Time de futebol atualizado com sucesso!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@time_bp.route('/time/<int:id>', methods=['DELETE'])
def delete_time(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM time_futebol WHERE idtime=%s", (id))
        conn.commit()
        resp = jsonify('time deletado com sucesso!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

