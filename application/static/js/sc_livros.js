function editarLivro(id,titulo, autor, isbn, categoria, ano) {
  document.getElementById("edit-id").value = id;
  document.getElementById("edit-titulo").value = titulo;
  document.getElementById("edit-autor").value = autor;
  document.getElementById("edit-isbn").value = isbn;
  document.getElementById("edit-categoria").value = categoria;
  document.getElementById("edit-ano").value = ano;

  document.getElementById("livroModal").style.display = "block";
}

function fecharModal() {
  document.getElementById("livroModal").style.display = "none";
}

// Fechar clicando fora
window.onclick = function(event) {
  const modal = document.getElementById("livroModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

async function salvarEdicao() {
  const livro = {
    _id: document.getElementById("edit-id").value,
    titulo: document.getElementById("edit-titulo").value,
    autor: document.getElementById("edit-autor").value,
    isbn: document.getElementById("edit-isbn").value,
    categoria: document.getElementById("edit-categoria").value,
    ano: document.getElementById("edit-ano").value,
  };

  const response = await fetch(`/livros/editar`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(livro)
  });

  const result = await response.json();
  if (response.ok) {
    alert(result.message);
    location.reload();
    // atualizarLinhaTabela(livro);
    fecharModal();
  } else {
    alert("Erro ao editar livro!");
  }
}

// Atualiza visualmente a tabela
function atualizarLinhaTabela(livro) {
  const linha = document.querySelector(`#livro-${livro._id}`);
  if (!linha) return;

  linha.cells[1].textContent = livro.titulo;
  linha.cells[2].textContent = livro.autor;
  linha.cells[3].textContent = livro.isbn;
  linha.cells[4].textContent = livro.categoria;
  linha.cells[5].textContent = livro.ano;
//   linha.cells[6].textContent = livro.status;
}
async function excluirLivro(id) {
    if (!confirm("Tem certeza que deseja excluir este livro?")) {
        return;
    }
    const response = await fetch(`/livros/excluir/${id}`, {
        method: "DELETE"
    });
    const result = await response.json();
    if (response.ok) {
        alert(result.message);
        location.reload();
        document.querySelector(`#livro-${id}`).remove();
    } else {
        alert("Erro ao excluir livro!");
    }
}