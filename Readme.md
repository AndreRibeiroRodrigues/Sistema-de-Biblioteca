
# Sistema de Biblioteca

Uma aplicação simples em Python para gerenciar empréstimos, alunos e livros com persistência em banco SQL.

## Visão geral

Este projeto fornece uma interface web leve para cadastrar alunos, livros e controlar empréstimos. Foi desenvolvido como um exercício/mini-projeto e inclui scripts para criar a base de dados e popular dados de exemplo.

## Recursos

- Cadastro e listagem de alunos
- Cadastro e listagem de livros
- Registro de empréstimos e devoluções
- Páginas HTML com estilos e scripts básicos

## Tecnologias

- Python 3
- SQLite (via scripts SQL locais)
- HTML, CSS, JavaScript

## Requisitos

- Python 3.8+ instalado
- `pip` para instalar dependências

## Instalação rápida

1. Clone o repositório:

```bash
git clone https://github.com/AndreRibeiroRodrigues/Sistema-de-Biblioteca.git
cd Sistema-de-Biblioteca
```

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

## Inicializando o banco de dados

O projeto inclui o arquivo `schema.sql` com a estrutura do banco. Para criar o banco e as tabelas, você pode executar o script Python que usa esse esquema ou rodar manualmente o SQL no seu cliente SQLite.

- Executar script de criação (exemplo):

```bash
python Inserir_Dados.py
```

O script `Inserir_Dados.py` insere dados de exemplo para facilitar testes.

## Executando a aplicação

Você pode rodar a aplicação diretamente com o script principal `run.py` ou usar o script `devserver.sh` se preferir um wrapper de execução.

```bash
python run.py
# ou
./devserver.sh
```

Após iniciar, abra o endereço exibido no terminal (por exemplo `http://127.0.0.1:5000`) para acessar a interface web.

## Estrutura do projeto

- `application/` : código da aplicação (rotas, banco, templates, estáticos)
- `Inserir_Dados.py` : script para popular dados de exemplo
- `schema.sql` : definição das tabelas do banco
- `run.py` : ponto de entrada da aplicação
- `devserver.sh` : script auxiliar para desenvolvimento

## Contribuição

- Abra uma issue descrevendo a melhoria desejada
- Fork e envie um pull request com mudanças claras

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

## Licença

Este projeto não possui uma licença especificada — adicione um arquivo `LICENSE` se desejar torná-lo open-source.
