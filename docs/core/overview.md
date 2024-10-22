# Core do Projeto

O aplicativo `core` é o núcleo da aplicação Django. Ele é responsável por configurar as rotas, o carregamento de templates, middlewares, e a inicialização do servidor WSGI. Além disso, define o arquivo `settings.py` que gerencia toda a configuração global do projeto.

## Principais Componentes

- **settings.py**: Contém as configurações principais do projeto, como instalação de aplicativos, middlewares, rotas de URLs, e templates.
- **urls.py**: Gerencia o roteamento principal do projeto, incluindo as rotas globais e a inclusão das URLs dos apps.
- **wsgi.py**: Ponto de entrada para servidores compatíveis com WSGI, responsável por servir o projeto em produção.

Esta documentação detalha os principais componentes do app `core`.
