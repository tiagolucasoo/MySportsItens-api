# MySportItens API

API REST desenvolvida com **FastAPI** para o projeto **MySportItens**, responsável pelo gerenciamento de usuários, produtos, categorias, pedidos e carrinho de compras.

## Tecnologias

- Python
- FastAPI
- MongoDB
- JWT

## Como executar

Clone o repositório:

```bash
git clone https://github.com/tiagolucasoo/mysportsitens-api.git
cd mysportsitens-api
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env`:

```env
MONGO_URI=
JWT_SECRET=
```

Execute a aplicação:

```bash
fastapi dev api/main.py
```

A documentação estará disponível em:

```
http://localhost:8000/docs
```

## Estrutura

```
api/
├── models/
├── routes/
├── services/
├── database.py
├── controller.py
└── main.py
```

## Funcionalidades

- Cadastro e login de usuários
- Autenticação com JWT
- Gerenciamento de produtos
- Gerenciamento de categorias
- Gerenciamento de pedidos
- Gerenciamento de carrinho

## Projeto

Projeto desenvolvido para a disciplina de **Desenvolvimento de Aplicações para Dispositivos Móveis** do **IFPR - Campus Londrina**.

Aplicação desenvolvida em conjunto com:
- **App:** https://github.com/mribeirom/my-sport-itens
