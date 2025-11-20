async function cadastrarAluno(){
  
  const  aluno = {
    nome: document.getElementsByName("nome")[0].value,
    matricula: document.getElementsByName("matricula")[0].value,
    turma: document.getElementsByName("turma")[0].value,
    email: document.getElementsByName("email")[0].value,
    telefone: document.getElementsByName("telefone")[0].value,
    dataNascimento: document.getElementsByName("dataN")[0].value
  }

  aluno.matricula = Math.floor(100000 + Math.random() * 900000);
  const [num1, num2, num3] = aluno.dataNascimento.split('-');
  aluno.dataNascimento = `${num1}/${num2}/${num3}`;
  const [numero, letra] = aluno.turma.split('-');
  aluno.turma = `${numero}º Ano ${letra.toUpperCase()}`;

  try{
    const resposta = await fetch('/aluno/cadastrar',{
      method: 'POST',
      headers: { 'content-type': 'application/json'},
      body: JSON.stringify(aluno)
    });
    const resultado = await resposta.json();
    alert(resultado.mensagem);

    }catch(erro){
      console.error('Erro ao cadastrar:', erro);
      alert('Erro ao cadastrar o aluno.');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    carregarAlunos();
});

async function carregarAlunos() {
    const tbody = document.querySelector('#tabelaAlunos tbody');
    tbody.innerHTML = ''; // limpa qualquer coisa anterior

    try {
        // Ajuste a URL para o endpoint correto da sua API Flask
        const resposta = await fetch('/aluno/listar');

        if (!resposta.ok) {
            throw new Error('Erro ao buscar alunos: ' + resposta.status);
        }

        const dados = await resposta.json();

        // Se sua API retornar { alunos: [...] } use isso:
        const alunos = Array.isArray(dados) ? dados : dados.alunos;

        alunos.forEach(aluno => {
            const tr = document.createElement('tr');

            // Cria as células
            const tdMatricula = document.createElement('td');
            tdMatricula.textContent = aluno.matricula;

            const tdNome = document.createElement('td');
            tdNome.textContent = aluno.nome;

            const tdTurma = document.createElement('td');
            tdTurma.textContent = aluno.turma;

            const tdEmail = document.createElement('td');
            tdEmail.textContent = aluno.email;

            const tdTelefone = document.createElement('td');
            tdTelefone.textContent = aluno.telefone;

            const tdAcoes = document.createElement('td');

            // Botão Editar
            const btnEditar = document.createElement('button');
            btnEditar.classList.add('action-btn');
            btnEditar.textContent = '✏️ Editar';
            btnEditar.addEventListener('click', () => {
                abrirModal(
                    aluno._id,
                    aluno.matricula,
                    aluno.nome,
                    aluno.turma,
                    aluno.email,
                    aluno.telefone
                );
            });

            // Botão Deletar
            const btnDeletar = document.createElement('button');
            btnDeletar.classList.add('action-btn');
            btnDeletar.textContent = '🗑️ Deletar';
            btnDeletar.addEventListener('click', () => {
                deletarAluno(aluno.matricula);
            });

            tdAcoes.appendChild(btnEditar);
            tdAcoes.appendChild(btnDeletar);

            // Monta a linha
            tr.appendChild(tdMatricula);
            tr.appendChild(tdNome);
            tr.appendChild(tdTurma);
            tr.appendChild(tdEmail);
            tr.appendChild(tdTelefone);
            tr.appendChild(tdAcoes);

            // Adiciona ao tbody
            tbody.appendChild(tr);
        });

    } catch (erro) {
        console.error(erro);
        // Se quiser, você pode mostrar uma mensagem na tela:
        tbody.innerHTML = `
            <tr>
                <td colspan="6">Erro ao carregar alunos.</td>
            </tr>
        `;
    }
}

function abrirModal(id,matricula, nome, turma, email, telefone) {
    document.getElementById('id').value = id;
    document.getElementById("matricula").value = matricula;
    document.getElementById("nome").value = nome;
    document.getElementById("modal-turma").value = turma;
    document.getElementById("email").value = email;
    document.getElementById("telefone").value = telefone;

    document.getElementById("alunoModal").style.display = "block";
  }

  // Fecha o modal
function fecharModal() {
    document.getElementById("alunoModal").style.display = "none";
  }

  // Salva (exemplo)
  function salvarAluno() {
    const aluno = {
      _id: document.getElementById("id").value,
      matricula: document.getElementById("matricula").value,
      nome: document.getElementById("nome").value,
      turma: document.getElementById("modal-turma").value,
      email: document.getElementById("email").value,
      telefone: document.getElementById("telefone").value,
    };

    console.log("Aluno atualizado:", aluno);
    alert("Dados salvos (simulação).");
    fecharModal();
  }

  // Fecha ao clicar fora
  window.onclick = function(event) {
    let modal = document.getElementById("alunoModal");
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  async function salvarAluno() {
    const aluno = {
      _id: document.getElementById("id").value,
      matricula: document.getElementById("matricula").value,
      nome: document.getElementById("nome").value,
      turma: document.getElementById("modal-turma").value,
      email: document.getElementById("email").value,
      telefone: document.getElementById("telefone").value,
    };

    try {
      const resposta = await fetch('/aluno/atualizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(aluno)
      });

      const resultado = await resposta.json();
      alert(resultado.mensagem);

      location.reload();
      // 🔹 Atualiza visualmente a linha da tabela (sem recarregar)
      // atualizarTabela(aluno);
      fecharModal();
    } catch (erro) {
      console.error('Erro ao atualizar:', erro);
      alert('Erro ao salvar as alterações.');
    }
  }

  // Atualiza a tabela HTML diretamente com os novos valores
  function atualizarTabela(aluno) {
    const linhas = document.querySelectorAll("table tr");
    linhas.forEach(linha => {
      const celulaMatricula = linha.querySelector("td:first-child");
      if (celulaMatricula && celulaMatricula.textContent.trim() === aluno.matricula) {
        linha.cells[1].textContent = aluno.nome;
        linha.cells[2].textContent = aluno.turma;
        linha.cells[3].textContent = aluno.email;
        linha.cells[4].textContent = aluno.telefone;
      }
    });
  }
  async function deletarAluno(matricula) {
    if (!confirm(`Confirma a exclusão do aluno com matrícula ${matricula}?`)) {
      return;
    }
    try {
      const resposta = await fetch('/deletar_aluno', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ matricula })
      });
      const resultado = await resposta.json();
      alert(resultado.mensagem);
      // Remove a linha da tabela
      removerLinhaTabela(matricula);
    } catch (erro) {
      console.error('Erro ao deletar:', erro);
      alert('Erro ao deletar o aluno.');
    }
  }

  // Remove a linha da tabela HTML
  function removerLinhaTabela(matricula) {
    const linhas = document.querySelectorAll("table tr");
    linhas.forEach(linha => {
      const celulaMatricula = linha.querySelector("td:first-child");
      if (celulaMatricula && celulaMatricula.textContent.trim() === matricula) {
        linha.remove();
      }
    });
  }
