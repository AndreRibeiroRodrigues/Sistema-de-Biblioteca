import sqlite3
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# 1. Conectar ao SQLite
sqlite_conn = sqlite3.connect("banco_de_dados.db")
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# 2. Conectar ao MongoDB
# crie seu arquivo .env com a variável MONGO_URI
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client["biblioteca"]  # nome do banco novo

# Criar coleções
col_alunos = mongo_db["aluno"]
col_livros = mongo_db["livro"]
col_emprestimos = mongo_db["emprestimo"]

print("Migrando ALUNOS...")

cursor.execute("SELECT * FROM ALUNOS")
alunos = cursor.fetchall()
for aluno in alunos:
    doc = dict(aluno)
    col_alunos.insert_one(doc)

print("Alunos migrados:", len(alunos))

print("Migrando LIVROS...")

cursor.execute("SELECT * FROM LIVROS")
livros = cursor.fetchall()
for livro in livros:
    doc = dict(livro)
    col_livros.insert_one(doc)

print("Livros migrados:", len(livros))

print("Migrando EMPRESTIMOS...")

cursor.execute("SELECT * FROM EMPRESTIMOS")
emprestimos = cursor.fetchall()
for emprestimo in emprestimos:
    doc = dict(emprestimo)
    col_emprestimos.insert_one(doc)

print("Empréstimos migrados:", len(emprestimos))

print("MIGRAÇÃO COMPLETA COM SUCESSO!")
