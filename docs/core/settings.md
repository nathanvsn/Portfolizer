# Configurações do Projeto (core/settings.py)

Este documento descreve as configurações principais do projeto no arquivo `settings.py`.

## INSTALLED_APPS

- **Django Apps**: Aplicações essenciais do Django:

  - `django.contrib.admin`: Sistema de administração.
  - `django.contrib.auth`: Sistema de autenticação.
  - `django.contrib.contenttypes`: Gerencia tipos de conteúdo dinâmicos.
  - `django.contrib.sessions`: Gerencia sessões de usuários.
  - `django.contrib.messages`: Sistema de mensagens.
  - `django.contrib.staticfiles`: Gerencia arquivos estáticos.
- **Apps do Projeto**:

  - `portfolios`: Gerencia os portfólios de usuários.
  - `custom_auth`: Sistema de autenticação customizado, substituindo o modelo padrão do Django.
  - `pages`: Gerencia páginas padrão como Home, Sobre e Contato.
- **Terceiros**:

  - `taggit`: Biblioteca de tags, usada para permitir que os projetos sejam marcados com tags.

## MIDDLEWARE

Middleware processa requisições e respostas. Aqui estão alguns middlewares importantes:

- `SecurityMiddleware`: Aplicação de políticas de segurança.
- `SessionMiddleware`: Habilita o uso de sessões.
- `CsrfViewMiddleware`: Protege contra ataques CSRF (Cross-Site Request Forgery).
- `AuthenticationMiddleware`: Conecta o sistema de autenticação com as sessões.
- `MessageMiddleware`: Gerencia o sistema de mensagens.

## ROOT_URLCONF

O arquivo principal de roteamento é `core.urls`, que centraliza todas as URLs do projeto.

## TEMPLATES

Configuração do sistema de templates:

- **DIRS**: Diretório global de templates, apontando para `templates/` na raiz do projeto.
- **APP_DIRS**: Permite que o Django carregue templates de diretórios de cada app.

## LOGIN/LOGOUT

- `LOGIN_REDIRECT_URL`: Redireciona os usuários após login bem-sucedido.
- `LOGOUT_REDIRECT_URL`: Redireciona os usuários após logout.

## Arquivos Estáticos e de Mídia

- **STATIC_URL**: URL pública para acessar arquivos estáticos.
- **STATICFILES_DIRS**: Diretórios onde os arquivos estáticos são armazenados.
- **MEDIA_URL**: URL pública para acessar arquivos de mídia (imagens, uploads).
- **MEDIA_ROOT**: Diretório onde os arquivos de mídia são armazenados.

## Autenticação Customizada

- **AUTH_USER_MODEL**: Define o modelo de usuário customizado (`custom_auth.User`), que substitui o modelo padrão do Django.
