---
sidebar_position: 1
---

# Instalação

Este guia irá ajudá-lo a instalar o Planify em seu ambiente de desenvolvimento ou produção.

## Requisitos do Sistema

Antes de começar, certifique-se de que seu sistema atende aos seguintes requisitos:

### Para o Backend
- Python 3.9+
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)
- PostgreSQL 12+ (para produção)

### Para o Frontend
- Node.js 16+
- npm 8+ ou yarn 1.22+

## Instalação para Desenvolvimento

### Configurando o Backend

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/Planify.git
cd Planify
```

2. **Configure o ambiente virtual Python**

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências do backend**

```bash
cd backend
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na pasta `backend` com o seguinte conteúdo:

```
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@example.com
EMAIL_HOST_PASSWORD=sua-senha
EMAIL_USE_TLS=True
```

5. **Execute as migrações do banco de dados**

```bash
python manage.py migrate
```

6. **Crie um superusuário**

```bash
python manage.py createsuperuser
```

7. **Inicie o servidor de desenvolvimento**

```bash
python manage.py runserver
```

O backend estará disponível em `http://localhost:8000/`.

### Configurando o Frontend

1. **Instale as dependências do frontend**

```bash
cd ../frontend
npm install  # ou yarn install
```

2. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na pasta `frontend` com o seguinte conteúdo:

```
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

3. **Inicie o servidor de desenvolvimento**

```bash
npm run dev  # ou yarn dev
```

O frontend estará disponível em `http://localhost:3000/`.

## Instalação para Produção

### Configurando o Backend para Produção

1. **Configure o PostgreSQL**

Instale o PostgreSQL e crie um banco de dados para o Planify:

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql
```

No prompt do PostgreSQL:

```sql
CREATE DATABASE planify;
CREATE USER planify_user WITH PASSWORD 'senha-segura';
GRANT ALL PRIVILEGES ON DATABASE planify TO planify_user;
\q
```

2. **Configure o ambiente virtual e instale dependências**

Siga os mesmos passos da instalação para desenvolvimento, mas use um arquivo `.env` de produção:

```
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=postgres://planify_user:senha-segura@localhost:5432/planify
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
EMAIL_HOST=smtp.seu-provedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@seu-provedor.com
EMAIL_HOST_PASSWORD=sua-senha-segura
EMAIL_USE_TLS=True
```

3. **Configure o Gunicorn e Nginx**

Instale o Gunicorn:

```bash
pip install gunicorn
```

Crie um arquivo de serviço systemd para o Gunicorn:

```bash
sudo nano /etc/systemd/system/planify.service
```

Adicione o seguinte conteúdo:

```
[Unit]
Description=Planify Gunicorn Daemon
After=network.target

[Service]
User=seu-usuario
Group=seu-grupo
WorkingDirectory=/caminho/para/Planify/backend
ExecStart=/caminho/para/Planify/venv/bin/gunicorn --workers 3 --bind unix:/caminho/para/Planify/planify.sock planify.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Instale e configure o Nginx:

```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/planify
```

Adicione a seguinte configuração:

```
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location /static/ {
        alias /caminho/para/Planify/backend/static/;
    }

    location /media/ {
        alias /caminho/para/Planify/backend/media/;
    }

    location / {
        proxy_pass http://unix:/caminho/para/Planify/planify.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Ative o site e reinicie o Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/planify /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### Configurando o Frontend para Produção

1. **Construa o frontend**

```bash
cd ../frontend
npm run build  # ou yarn build
```

2. **Configure o Nginx para servir o frontend**

Modifique a configuração do Nginx:

```bash
sudo nano /etc/nginx/sites-available/planify
```

Atualize para:

```
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location /api/ {
        proxy_pass http://unix:/caminho/para/Planify/planify.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/ {
        proxy_pass http://unix:/caminho/para/Planify/planify.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/admin/ {
        alias /caminho/para/Planify/backend/static/admin/;
    }

    location /media/ {
        alias /caminho/para/Planify/backend/media/;
    }

    location / {
        root /caminho/para/Planify/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

Reinicie o Nginx:

```bash
sudo systemctl restart nginx
```

## Configuração HTTPS com Let's Encrypt

Para produção, é altamente recomendável configurar HTTPS:

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

Siga as instruções na tela para completar a configuração HTTPS.

## Próximos Passos

Agora que você instalou o Planify, continue para o [Guia de Configuração](./configuration) para personalizar sua instalação.
