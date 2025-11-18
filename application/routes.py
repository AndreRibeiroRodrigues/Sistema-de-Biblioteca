from flask import Blueprint, render_template, redirect, request, jsonify
import application.database as database

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/apresentacao')
def index():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM LIVROS')
    livros = cursor.fetchone()[0]
    conn.close()

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ALUNOS')
    alunos= cursor.fetchone()[0]
    conn.close()

    conn = database.get_connection()
    cursor = conn.cursor() 
    cursor.execute('SELECT COUNT(*) FROM EMPRESTIMOS')
    emprestimos= cursor.fetchone()[0]
    conn.close()

    return render_template('index.html', livros=livros, alunos=alunos, emprestimos=emprestimos)

#aluno
@bp.route('/aluno')
def aluno():
    alunos = database.listar_alunos_mongo()
    return render_template('alunos.html', aluno=alunos)

@bp.route('/aluno/listar', methods=['GET'])
def listar_alunos():
    alunos = database.listar_alunos_mongo()
    return jsonify(alunos)
    
@bp.route('/aluno/cadastrar', methods=['POST']) # type: ignore
def cadastrar_aluno():
    aluno = request.get_json()
    database.cadastrar_aluno_mongo(aluno)
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'})

@bp.route('/atualizar_aluno', methods=['POST'])
def atualizar_aluno():
    dados = request.get_json()
    matricula = dados['matricula']
    nome = dados['nome']
    turma = dados['turma']
    email = dados['email']
    telefone = dados['telefone']
    database.atualizarAluno(matricula, nome, turma, email, telefone)
    

    return jsonify({'mensagem': 'Aluno atualizado com sucesso!'})

@bp.route('/deletar_aluno', methods=['POST'])
def deletar_aluno():
    dados = request.get_json()
    matricula = dados['matricula']
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ALUNOS WHERE MATRICULA = ?', (matricula,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Aluno deletado com sucesso!'})

#livro
@bp.route('/livros')
def livros():
    livros = database.listar_livros()
    return render_template('livros.html', livros=livros)

@bp.route('/post_livro', methods=['POST'])
def adicionar_livro():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    isbn = request.form.get('isbn')
    categoria = request.form.get('categoria')
    ano = request.form.get('ano')
    database.add_livro(titulo, autor, isbn, categoria, ano)
    return redirect('/livros')

@bp.route('/livros/editar/<int:id>', methods=['PUT'])
def editar_livro(id):
    dados = request.get_json()
    titulo = dados['titulo']
    autor = dados['autor']
    isbn = dados['isbn']
    categoria = dados['categoria']
    ano = dados['ano']
    database.atualizar_livro(id, titulo, autor, isbn, categoria, ano)
    return jsonify({"message": "Livro atualizado com sucesso!"})

@bp.route('/livros/excluir/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM LIVROS WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Livro excluído com sucesso!"})

#Emprestimo
@bp.route('/emprestimos')
def emprestimos():
    alunos = database.listar_alunos()
    livros = database.listar_livros()
    emprestimos = database.get_emprestimos()

    return render_template('emprestimos.html', emprestimos=emprestimos,livros=livros, alunos=alunos)

@bp.route('/emprestimos/adicionar', methods=['POST'])
def post_emprestimo():
    matricula = request.form.get('aluno')
    idlivro = request.form.get('livro')
    dataEmprestimo = request.form.get('dataEmprestimo')
    dataDevolucao = request.form.get('dataDevolucao')
    acao = request.form.get('acao')
    if acao == 'inserir':
        database.inserir_emprestimo(matricula, idlivro)
        return redirect('/emprestimos')
    else:
        return redirect('/emprestimos')

@bp.route('/emprestimos/devolver/<int:id>', methods=['PUT'])
def devolver_livro(id):
    database.devolver_livro(id)
    return jsonify({"message": "Livro devolvido com sucesso!"})




