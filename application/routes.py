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
    return render_template('alunos.html')

@bp.route('/aluno/listar', methods=['GET'])
def listar_alunos():
    alunos = database.alunoListarMongo()
    return jsonify(alunos)
    
@bp.route('/aluno/cadastrar', methods=['POST']) # type: ignore
def cadastrar_aluno():
    aluno = request.get_json()
    database.alunoCadastrarMongo(aluno)
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'})

@bp.route('/aluno/atualizar', methods=['POST'])
def atualizar_aluno():
    dados = request.get_json()
    database.alunoAtualizarMongo(dados)
    

    return jsonify({'mensagem': 'Aluno atualizado com sucesso!'})

@bp.route('/aluno/deletar', methods=['POST'])
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
    livros = database.livroListarMongo()
    return render_template('livros.html', livros=livros)

@bp.route('/livros/listar')
def listar_livros():
    livros = database.livroListarMongo()
    return jsonify(livros)

@bp.route('/livro/adicionar', methods=['POST'])
def adicionar_livro():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    isbn = request.form.get('isbn')
    categoria = request.form.get('categoria')
    ano = request.form.get('ano')
    database.livroAdicionarMongo(titulo, autor, isbn, categoria, ano)
    return redirect('/livros')

@bp.route('/livros/editar', methods=['PUT'])
def editar_livro():
    alteracao = request.get_json()
    database.livroAtualizarMongo(alteracao)
    return jsonify({"message": "Livro atualizado com sucesso!"})

@bp.route('/livros/excluir/<string:id>', methods=['DELETE'])
def excluir_livro(id):
    database.livroDelertarMongo(id)
    return jsonify({"message": "Livro excluído com sucesso!"})

#Emprestimo
@bp.route('/emprestimos')
def emprestimos():
    alunos = database.alunoListarMongo()
    livros = database.livroListarMongo()
    emprestimos = database.get_emprestimos()

    return render_template('emprestimos.html', emprestimos=emprestimos,livros=livros, alunos=alunos)

@bp.route('/emprestimos/adicionar', methods=['POST'])
def post_emprestimo():
    matricula = request.form.get('aluno')
    idlivro = request.form.get('livro')
    database.emprestimoAdicionarMongo(matricula, idlivro)
    return redirect('/emprestimos')

@bp.route('/emprestimos/devolver/<int:id>', methods=['PUT'])
def devolver_livro(id):
    database.devolver_livro(id)
    return jsonify({"message": "Livro devolvido com sucesso!"})




