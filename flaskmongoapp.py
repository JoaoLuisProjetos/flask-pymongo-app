# utf-8

from flask import Flask, request, jsonify, Response
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from populate import populate_collections

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'portalnoticias'
app.config['MONGO_URI'] = 'mongodb://localhost/portalnoticias'
client = MongoClient('localhost', 27017)
db = client.portalnoticias

# Indexa Noticias
try:
    db['noticias'].create_index([("titulo", pymongo.TEXT), ("descricao", pymongo.TEXT)])
except:
    pass

# Indexa Autores
try:
    db['autores'].create_index([("nome", pymongo.TEXT)])
except:
    pass

mongo = PyMongo(app)

# Popular o banco na primeira execução
populate_collections(db)

# http://localhost:5000/add/autor - INSERT (Autores)
@app.route('/add/autor', methods=['POST'])
def add_autor():
    # Recebe Dados
    nome = request.json['nome']

    if nome and not nome.isspace():
        id = db['autores'].insert_one({'nome': nome})
        response = {
            'id': str(id),
            'nome': nome
        }
        return response

    return {'message': 'Nome do autor inválido ou em branco'}

# http://localhost:5000/listar/autores - READ ALL (Autores)
@app.route('/listar/autores', methods=['GET'])
def read_autores():
    autores = db['autores'].find()
    response = json_util.dumps(autores)
    return Response(response, mimetype='application/json')

# http://localhost:5000/autor/<id> - READ 1 (Autores)
@app.route('/autor/<id>', methods=['GET'])
def read_autor(id):
    autor = db['autores'].find_one({"_id": ObjectId(id)})
    response = json_util.dumps(autor)
    return Response(response, mimetype='application/json')

# http://localhost:5000/search/autores - SEARCH (AUTORES - por nome)
@app.route('/search/autores', methods=['GET'])
def search_autor():
    nome = request.json['nome']
    dados_autor = db['autores'].find({'$text': {'$search': nome}})
    response = json_util.dumps(dados_autor)
    return Response(response, mimetype='application/json')

# http://localhost:5000/add/noticia - INSERT (Noticias)
@app.route('/add/noticia', methods=['POST'])
def add_noticia():

    titulo = request.json['titulo']
    descricao = request.json['descricao']
    autor = request.json['autor']

    autor_dados = db['autores'].find_one({'nome': autor})

    valida = ''
    if not titulo or titulo.isspace():
        valida = "Título"
    elif not descricao or descricao.isspace():
        valida = "Descrição do Texto"
    elif not autor and autor.isspace() or autor_dados is None:
        valida = "Autor"

    if valida != '':
        return {'message':  valida + ' em branco ou não cadastrado'}

    id = db['noticias'].insert_one({
            'titulo': titulo,
            'descricao': descricao,
            'autor': autor_dados['_id']
            })
    response = {
            'id': str(id),
            'titulo': titulo,
            'descricao': descricao,
            'autor': autor_dados['nome']
        }
    return response

# http://localhost:5000/listar/noticias - READ ALL (Noticias)
@app.route('/listar/noticias', methods=['GET'])
def read_noticias():
    noticias = db['noticias'].find()
    response = json_util.dumps(noticias)
    return Response(response, mimetype='application/json')

# http://localhost:5000/noticia/<id> - READ 1 (Noticias)
@app.route('/noticia/<id>', methods=['GET'])
def read_noticia(id):
    noticia = db['noticias'].find_one({"_id": ObjectId(id)})
    response = json_util.dumps(noticia)
    return Response(response, mimetype='application/json')

# http://localhost:5000/delete/noticia/<id> - DELETE (Noticias)
@app.route('/delete/noticia/<id>', methods=['DELETE'])
def delete_noticia(id):
    db['noticias'].delete_one({"_id": ObjectId(id)})
    response = jsonify({'message': 'Noticia deletada com sucesso'})
    return response

# http://localhost:5000/search/noticia - SEARCH (Noticias - por titulo e descricao)
@app.route('/search/noticia', methods=['GET'])
def search_titulo():
    texto = request.json['texto']
    noticias = db['noticias'].find({'$text': {'$search': texto}})
    response = json_util.dumps(noticias)
    return Response(response, mimetype='application/json')

# http://localhost:5000/update/noticia/<id> - UPDATE Noticias
@app.route('/update/noticia/<id>', methods=['PUT'])
def update_user(id):

    titulo = request.json['titulo']
    descricao = request.json['descricao']
    nome_autor = request.json['nome_autor']

    noticia = db['noticias'].find_one({"_id": ObjectId(id)})
    autor = db['autores'].find_one({'$text': {'$search': nome_autor}})
    valida = ''

    if not titulo or titulo.isspace():
        valida = "Titulo"
    elif not descricao or descricao.isspace():
        valida = "Prefácio"
    elif noticia == [] or noticia is None:
        valida = "Livro"
    elif autor == [] or autor is None:
        valida = "Autor"

    if valida != '':
        return {'message':  valida + ' inválido.'}

    db['noticias'].update_one({"_id": ObjectId(id)},
        {'$set': {
            'titulo': titulo,
            'descricao': descricao,
            'autor': autor['_id']
        }})
    response = jsonify({'message': 'Noticia ' + titulo + ' foi atualizada com sucesso.'})
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Requisicao inválida: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response


if __name__== "__main__":
    app.run(debug=True)
