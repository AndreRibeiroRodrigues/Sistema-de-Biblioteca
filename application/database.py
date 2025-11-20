import sqlite3
import os
import datetime
from pymongo import MongoClient
from bson import ObjectId


def get_connection():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, 'schema.sql')
    with open(schema_path) as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


# A função init_db() inicializa o banco de dados executando um script SQL a partir de um arquivo chamado schema.sql.
# Certifique-se de ter um arquivo schema.sql no mesmo diretório com a estrutura do banco

def inserir_dados():
    conn = get_connection()
    cursor = conn.cursor()
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, 'dados.sql')
    with open(schema_path) as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

#alunos
def listar_alunos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM  ALUNOS')
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def cadastrar_aluno(aluno):
    print(aluno)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ALUNOS (NOME, MATRICULA, TURMA, EMAIL, TELEFONE, DATANASCIMENTO) VALUES (?, ?, ?, ?, ?, ?)',
                   (aluno['nome'], aluno['matricula'],  aluno['turma'], aluno['email'], aluno['telefone'], aluno['dataNascimento']))
    conn.commit()
    conn.close()

def atualizarAluno(matricula, nome, turma, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE ALUNOS SET NOME = ?, TURMA = ?, EMAIL = ?, TELEFONE = ? 
                      WHERE MATRICULA = ?''',
                   (nome, turma, email, telefone, matricula))
    conn.commit()
    conn.close()

#livros
def listar_livros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM LIVROS')
    livros = cursor.fetchall()
    conn.close()
    return livros

def add_livro(titulo, autor, isbn, categoria, ano):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO LIVROS (TITULO, AUTOR, ISBN, CATEGORIA, ANO)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, autor, isbn, categoria, ano))
    conn.commit()
    conn.close()

def atualizar_livro(id, titulo, autor, isbn, categoria, ano):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE LIVROS
        SET TITULO = ?, AUTOR = ?, ISBN = ?, CATEGORIA = ?, ANO = ?
        WHERE ID = ?
    """, (titulo, autor, isbn, categoria, ano, id))
    conn.commit()
    conn.close()  
#emprestimos
def get_emprestimos():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            e.ID AS id_emprestimo,
            a.NOME AS Aluno,
            l.TITULO AS Livro,
            e.DATAEMPRESTIMO,
            e.DATADEVOLUCAO
        FROM EMPRESTIMOS e
        JOIN ALUNOS a ON e.ID_ALUNO = a.MATRICULA
        JOIN LIVROS l ON e.ID_LIVRO = l.ID;
    ''')
    emprestimos = cursor.fetchall()
    conn.close()
    return emprestimos

def devolver_livro(id):
    conn = get_connection()
    cursor = conn.cursor()
    dataDevolucao = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        UPDATE EMPRESTIMOS
        SET DATADEVOLUCAO = ?
        WHERE ID = ?
    ''', (dataDevolucao, id))
    conn.commit()
    conn.close()


def inserir_emprestimo(matricula, idlivro):
    dataEmprestimo = datetime.datetime.now().strftime('%Y-%m-%d')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO EMPRESTIMOS (ID_ALUNO, ID_LIVRO, DATAEMPRESTIMO) VALUES (?, ?, ?)',
                    (matricula, idlivro, dataEmprestimo))
    conn.commit()
    conn.close()

#Mongodb
aluno_validator = {
    "validator" :{
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Aluno Document Validation",
            "required": [
                "MATRICULA",
                "NOME",
                "TURMA",
                "EMAIL",
                "TELEFONE",
                "DATANASCIMENTO"
            ],
            "properties": {
                "MATRICULA": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "'MATRICULA' deve ser um inteiro positivo e é obrigatória"
                },
                "NOME": {
                    "bsonType": "string",
                    "description": "'NOME' deve ser string e é obrigatório"
                },
                "TURMA": {
                    "bsonType": "string",
                    "description": "'TURMA' deve ser string e é obrigatório"
                },
                "EMAIL": {
                    "bsonType": "string",
                    "pattern": "^.+@.+$",
                    "description": "'EMAIL' deve ser um e-mail válido e é obrigatório"
                },
                "TELEFONE": {
                    "bsonType": "string",
                    "description": "'TELEFONE' deve ser string e é obrigatório"
                },
                "DATANASCIMENTO": {
                    "bsonType": "date",
                    "description": "'DATANASCIMENTO' deve ser uma data (MongoDB Date) e é obrigatório"
                }
            }
        }
    }
}
livro_validator = {
    "validator" :{
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Livro Document Validation",
            "required": [
                "ID",
                "TITULO",
                "AUTOR",
                "ISBN",
                "CATEGORIA",
                "ANO"
            ],
            "properties": {
                "ID": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "'ID' deve ser um inteiro positivo e é obrigatório"
                },
                "TITULO": {
                    "bsonType": "string",
                    "description": "'TITULO' deve ser string e é obrigatório"
                },
                "AUTOR": {
                    "bsonType": "string",
                    "description": "'AUTOR' deve ser string e é obrigatório"
                },
                "ISBN": {
                    "bsonType": "string",
                    "description": "'ISBN' deve ser string e é obrigatório"
                },
                "CATEGORIA": {
                    "bsonType": "string",
                    "description": "'CATEGORIA' deve ser string e é obrigatório"
                },
                "ANO": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "'ANO' deve ser inteiro não negativo e é obrigatório"
                }
            }
        }
    }
}
emprestimo_validator = {
    "validator" :{
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Emprestimo Document Validation",
            "required": [
                "ID",
                "ID_ALUNO",
                "ID_LIVRO",
                "DATAEMPRESTIMO"
            ],
            "properties": {
                "ID": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "'ID' deve ser um inteiro positivo e é obrigatório"
                },
                "ID_ALUNO": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "'ID_ALUNO' deve ser inteiro positivo e é obrigatório (ref. ALUNOS.MATRICULA)"
                },
                "ID_LIVRO": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "'ID_LIVRO' deve ser inteiro positivo e é obrigatório (ref. LIVROS.ID)"
                },
                "DATAEMPRESTIMO": {
                    "bsonType": "date",
                    "description": "'DATAEMPRESTIMO' deve ser uma data (MongoDB Date) e é obrigatória"
                },
                "DATADEVOLUCAO": {
                    "bsonType": ["date", "null"],
                    "description": "'DATADEVOLUCAO' pode ser data ou null"
                },
                "STATUS": {
                    "bsonType": ["string", "null"],
                    "description": "'STATUS' é opcional; se existir deve ser string"
                }
            }
        }
    }
}


def get_mongo_connection():
    uri = "mongodb+srv://gamesandre77_db_user:Um.emel2@rayjirmongodb.k4qsfcn.mongodb.net/?appName=RayjirMongodb"
    client = MongoClient(uri)
    db = client['biblioteca']
    print('conectado')
    return db

mongo_conn = get_mongo_connection()

def init_mongodb():
    
    if 'aluno' not in mongo_conn.list_collection_names():
        mongo_conn.create_collection(
            'aluno',
            validator=aluno_validator
        )
    if 'livro' not in mongo_conn._list_collection_names():
        mongo_conn.create_collection(
            'livro',
            validator=livro_validator
        )
    if 'emprestimo' not in mongo_conn.list_collection_names():
        mongo_conn.create_collection(
            'emprestimo',
            validator=emprestimo_validator
        )

# def inserir_dados_mongo():
#     #função que insere dados de teste no banco de dados
#     return

# #alunos
def alunoListarMongo():
    alunos = list(mongo_conn.aluno.find({}))

    # converter ObjectId para string
    for aluno in alunos:
        aluno["_id"] = str(aluno["_id"])
        
    return alunos

def alunoCadastrarMongo(aluno):
    mongo_conn.aluno.insert_one(aluno)
    

def alunoAtualizarMongo(dado):
    mogno_conn.livro.update_one(dado["id"],dado)

#livros
def livroListarMongo():

    livros = list(mongo_conn.livro.find({}))

    for livro in livros:
        livro["_id"] = str(livro["_id"])

    return livros


def livroAdicionarMongo(titulo, autor, isbn, categoria, ano):
    livro = {
        'titulo': titulo,
        'autor': autor,
        'isbn': isbn,
        'categoria': categoria,
        'ano': ano
    }
    mongo_conn.livro.insert_one(livro) 

def livroAtualizarMongo(dados):
    mongo_conn.livro.update_one(dados["id"], dados)

# #emprestimos
# def get_emprestimos():
#     return

# def devolver_livro(id):
#     return


def emprestimoAdicionarMongo(matricula, idlivro):
    dataEmprestimo = datetime.datetime.now().strftime('%Y-%m-%d')
    emprestimo = {
        'matricula': matricula,
        'idlivro': idlivro,
        'dataEmprestimo': dataEmprestimo
    }
    mongo_conn.emprestimo.insert_one(emprestimo)