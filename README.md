# To-Dos (Flask)

Aplicação web moderna de gerenciamento de tarefas com kanban board estilo Trello, construída com Flask e SQLite.

## Visão geral

Este projeto implementa um gerenciador de tarefas completo com autenticação e visualização em kanban:

- Cadastro e login de usuários com segurança
- **Kanban Board com 3 colunas**: Started → Developing → Finished
- Drag-and-drop para mover tarefas entre colunas
- Auto-save de status sem recarregar página
- Criação, edição e exclusão de tarefas
- Controle de autorização (cada usuário gerencia apenas as próprias tarefas)
- Interface web moderna e responsiva
- Tema claro/escuro com sincronização em tempo real
- Design limpo e profissional (sem emojis)
- Testes automatizados com `pytest`

## Stack

- Python 3
- Flask
- SQLite
- Jinja2 (templates)
- Pytest (testes)
- Flit (`pyproject.toml`) para empacotamento
- Drag-and-drop API nativa do JavaScript

## Estrutura do projeto

```text
app/
  __init__.py           # factory da aplicação Flask
  auth.py               # rotas de autenticação
  task.py               # rotas de tarefas (CRUD + kanban status)
  db.py                 # conexão com banco e comando init-db
  schema.sql            # esquema do banco SQLite
  templates/
    base.html           # template base com navegação
    task/
      index.html        # kanban board (principal)
      create.html       # criar nova tarefa
      update.html       # editar tarefa e deletar
    auth/
      login.html        # login
      register.html     # cadastro
  static/
    style.css           # estilos modernos (tema claro/escuro)
    theme.js            # toggle de tema
    kanban.js           # lógica de drag-and-drop
instance/               # banco SQLite local (app.sqlite)
tests/                  # testes automatizados
pyproject.toml          # metadados e configuração do projeto
```

## Pré-requisitos

- Python 3.10+
- `pip`

## Como executar localmente

### 1. Criar e ativar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 2. Instalar dependências

```bash
pip install flask pytest build
```

### 3. Inicializar banco de dados

```bash
flask --app app init-db
```

O banco é criado automaticamente com as tabelas de usuários e tarefas. Se você tiver um banco existente, a coluna `status` é adicionada automaticamente.

### 4. Rodar aplicação

```bash
flask --app app run --debug
```

Acesse em: `http://127.0.0.1:5000`

## Funcionalidades Principais

### Kanban Board

Na página principal (após fazer login), você verá um kanban board com 3 colunas:

- **Started**: Novas tarefas são criadas aqui
- **Developing**: Tarefas em progresso
- **Finished**: Tarefas concluídas

**Como usar:**
1. Arraste tarefas entre colunas para mudar o status
2. O status é salvo automaticamente no banco de dados
3. Clique no ícone ✎ para editar título e descrição
4. Clique em "New Task" para criar uma nova tarefa

### Tema Claro/Escuro

- Clique no botão "Dark/Light" na navegação para alternar temas
- A preferência é salva automaticamente no navegador
- Responde ao tema do sistema operacional

### Interface Responsiva

- **Desktop**: 3 colunas do kanban lado a lado
- **Tablet**: 2 colunas por linha
- **Mobile**: 1 coluna por linha (scrollável)

## Base de Dados

### Schema

A tabela `task` contém:

```sql
CREATE TABLE task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  status TEXT DEFAULT 'Started',  -- novo: Started, Developing, Finished
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

### Migração Automática

Ao iniciar a aplicação, se você tiver um banco de dados existente, a coluna `status` é adicionada automaticamente com o valor padrão `'Started'` para todas as tarefas antigas.

## API - Rotas Principais

### Autenticação

- `GET|POST /auth/register` - Cadastro de novo usuário
- `GET|POST /auth/login` - Fazer login
- `GET /auth/logout` - Fazer logout

### Tarefas

- `GET /` - Lista todas as tarefas no kanban board
- `GET|POST /create` - Criar nova tarefa (requer login)
- `GET|POST /<id>/update` - Editar tarefa (autor apenas)
- `POST /<id>/delete` - Exclui tarefa (autor apenas)
- `POST /<id>/status` - Atualiza o status da tarefa via API JSON (drag-and-drop)

#### Exemplo: Atualizar Status via API

```bash
curl -X POST http://127.0.0.1:5000/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Developing"}'
```

Resposta:
```json
{
  "success": true,
  "status": "Developing"
}
```

Status válidos: `Started`, `Developing`, `Finished`

## Testes

Executar toda a suíte de testes:

```bash
pytest
```

Para ver cobertura:

```bash
pytest --cov=app
```

## Empacotamento (wheel)

Gerar wheel do projeto:

```bash
python -m build --wheel
```

O artefato será criado em `dist/`.

## Deploy na Vercel

Este projeto está configurado para deploy na Vercel com os arquivos:

- `vercel.json`
- `api/index.py`
- `requirements.txt`

### Passo a passo

1. Suba o projeto para um repositório GitHub
2. Na Vercel, clique em **Add New Project** e importe o repositório
3. Em **Environment Variables**, configure:
   - `SECRET_KEY` - valor forte para produção (recomendado)

4. Faça o deploy

### Observação importante sobre banco de dados

Atualmente o app usa SQLite. Na Vercel (serverless), o SQLite em `/tmp` é **efêmero**:

- Os dados podem ser perdidos entre reinicializações (cold starts)
- Não é adequado para produção com persistência

**Para produção**, recomenda-se migrar para um banco externo como PostgreSQL, MySQL ou MongoDB.

## Design & UX

### Paleta de Cores

**Light Mode:**
- Fundo: Branco puro (`#ffffff`)
- Texto primário: Cinza escuro (`#1d1d1f`)
- Acentos: Roxo (`#667eea` → `#764ba2`)

**Dark Mode:**
- Fundo: Cinza muito escuro (`#1a1a1e`)
- Texto primário: Cinza claro (`#f5f5f7`)
- Acentos: Roxo (mantém a mesma paleta)

### Tipografia

- Font Family: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- Hierarquia clara com pesos 400, 500, 600, 700
- Excelente contraste e acessibilidade

### Efeitos

- Transições suaves (0.25s - 0.3s)
- Sombras sutis e realistas
- Hover states claros e responsivos
- Animações de drag-and-drop fluidas

## Boas Práticas de Segurança

- ✅ Não comitar segredos no repositório (`.env`, chaves, certificados)
- ✅ Usar `.env.example` como modelo de variáveis
- ✅ Em produção, sempre definir `SECRET_KEY` via variável de ambiente
- ✅ Verificação de autorização em todas as rotas (cada usuário só acessa suas tarefas)
- ✅ Validação de entrada em formulários
- ✅ CSRF protection via Flask (Jinja2)
- ✅ Senhas hasheadas com werkzeug

## Observações

- O banco SQLite padrão fica em `instance/app.sqlite`
- O comando `init-db` recria as tabelas definidas em `app/schema.sql`
- Em desenvolvimento, a `SECRET_KEY` está definida como `dev`
- Todas as tarefas antigas recebem automaticamente o status `'Started'` na primeira execução

## Tecnologias & Técnicas

- **Drag-and-Drop**: HTML5 Drag and Drop API nativa (sem jQuery)
- **HTTP**: REST API com JSON
- **Persistência**: SQLite3 com migrações seguras
- **Autenticação**: Session-based (cookies)
- **Frontend**: Jinja2 templates + CSS customization properties (CSS variables)

## Licença

MIT
