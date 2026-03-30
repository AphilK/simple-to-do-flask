# To-Dos (Flask)

Aplicação web simples de gerenciamento de tarefas, construída com Flask e SQLite.

## Visão geral

Este projeto implementa um CRUD de tarefas com autenticação de usuários:

- Cadastro e login de usuários
- Criação, listagem, edição e exclusão de tarefas
- Controle de autorização (cada usuário gerencia apenas as próprias tarefas)
- Interface web responsiva com suporte a tema claro/escuro
- Testes automatizados com `pytest`

## Stack

- Python 3
- Flask
- SQLite
- Jinja2 (templates)
- Pytest (testes)
- Flit (`pyproject.toml`) para empacotamento

## Estrutura do projeto

```text
app/
  __init__.py      # factory da aplicação Flask
  auth.py          # rotas de autenticação
  task.py          # rotas de tarefas (CRUD)
  db.py            # conexão com banco e comando init-db
  schema.sql       # esquema do banco SQLite
  templates/       # páginas HTML
  static/          # CSS e JS
instance/          # banco SQLite local (app.sqlite)
tests/             # testes automatizados
pyproject.toml     # metadados e configuração do projeto
```

## Pré-requisitos

- Python 3.10+
- `pip`

## Como executar localmente

1. Criar e ativar ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install flask pytest build
```

3. Inicializar banco de dados:

```bash
flask --app app init-db
```

4. Rodar aplicação:

```bash
flask --app app run --debug
```

Acesse em: `http://127.0.0.1:5000`

## Testes

Executar toda a suíte:

```bash
pytest
```

## Empacotamento (wheel)

Gerar wheel do projeto:

```bash
python -m build --wheel
```

O artefato será criado em `dist/`.

## Rotas principais

- `GET /` Lista tarefas
- `GET|POST /create` Cria tarefa (requer login)
- `GET|POST /<id>/update` Edita tarefa (autor apenas)
- `POST /<id>/delete` Exclui tarefa (autor apenas)
- `GET|POST /auth/register` Cadastro
- `GET|POST /auth/login` Login
- `GET /auth/logout` Logout

## Observações

- O banco SQLite padrão fica em `instance/app.sqlite`.
- O comando `init-db` recria as tabelas definidas em `app/schema.sql`.
- Em ambiente de desenvolvimento, a `SECRET_KEY` está definida como `dev`.
