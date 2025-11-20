async function devolverEmprestimo(id) {
  if (!confirm("Tem certeza que deseja marcar este empréstimo como devolvido?")) return;

  try {
    const response = await fetch(`/emprestimos/devolver/${id}`, {
      method: "delete",
    });

    const result = await response.json();

    if (response.ok) {
      alert(result.message);
      location.reload();
    } else {
      alert("Erro ao devolver: " + result.message);
    }
    
  } catch (erro) {
    console.error(erro);
    alert("Erro ao conectar com o servidor.");
  }
}
