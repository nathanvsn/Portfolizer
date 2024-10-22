# Portfolizer: SaaS de Portfólios/Currículos para Programadores

Portfolizer é um serviço de SaaS projetado para desenvolvedores criarem portfólios e currículos interativos. O projeto permite que usuários Free, Pro, e Ultra construam e gerenciem páginas com projetos e conteúdo personalizado, utilizando Markdown ou uploads diretos de arquivos HTML/CSS/JS.

## Funcionalidades

- **Portfólios Dinâmicos**: Usuários podem criar portfólios pessoais com Markdown.
- **Suporte a Imagens**: Upload de imagens para incluir em projetos e páginas.
- **Níveis de Conta**:
  - **Free**: Limite de 5 projetos com até 3 imagens por projeto.
  - **Pro**: Número ilimitado de projetos com até 10 imagens por projeto.
  - **Ultra**: Projetos ilimitados com upload de arquivos HTML/CSS/JS e até 1GB de armazenamento total.
- **Autenticação Personalizada**: Sistema de login e registro com suporte a perfis personalizados.
- **Gerenciamento de Tags**: Cada projeto pode ser marcado com até 3 tags para categorização.

---

## Sumário

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)

---

## Instalação

### Pré-requisitos

Certifique-se de ter os seguintes itens instalados no seu ambiente:

- Python 3.10+
- Django 5.1+
- SQLite (ou outro banco de dados configurado)
- Virtualenv (recomendado)

### Passos para instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/portfolizer.git
cd portfolizer
```

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Aplique as migrações do banco de dados:

```bash
python manage.py migrate
```

5. Crie um superusuário para acessar o painel de administração:

```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Agora, o projeto está disponível em `http://127.0.0.1:8000/`.

---

## Configuração

### Configuração de Arquivos Estáticos e Mídia

No arquivo `settings.py`, verifique as seguintes configurações para servir arquivos de mídia corretamente durante o desenvolvimento:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Em `urls.py`, certifique-se de incluir:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Suas rotas aqui
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Uso

### Criando um Portfólio

Após criar uma conta, os usuários podem personalizar sua página de portfólio da seguinte forma:

1. **Usuários Free** :

* Página em `localhost:8000/[username]/`.
* Suporte a Markdown para personalizar a página inicial.
* Até 5 projetos com até 3 imagens por projeto.

1. **Usuários Pro** :

* Criar páginas com upload de HTML/CSS/JS via uploads diretos.
* Projetos ilimitados com até 10 imagens por projeto.

1. **Usuários Ultra** :

* Página personalizada `[username].localhost:8000/`.
* Upload de arquivos HTML/CSS/JS diretamente.
* Armazenamento de até 1GB de imagens e vídeos.

### Exemplo de Markdown

Aqui está um exemplo de como adicionar uma imagem e descrição a um projeto usando Markdown:

```markdown
# Meu Projeto de Exemplo

Aqui está uma prévia do meu projeto:

![Imagem do Projeto](/media/project_resources/exemplo.png)

Este projeto usa Django para criar uma aplicação web completa.
```

### Gerenciamento de Imagens

* Para adicionar uma nova imagem ao projeto, basta clicar no botão **+** ao lado de "Imagens do Projeto".
* Para cada imagem, você pode copiar o link ou excluir a imagem diretamente.
