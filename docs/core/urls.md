
# Configuração de URLs (core/urls.py)

Este documento descreve a configuração de roteamento de URLs do projeto.

## Rotas Globais

- **admin/**: Acesso ao painel de administração do Django.

```python
path('admin/', admin.site.urls)
```

* **pages/** : Define as páginas padrão do projeto como Home, Sobre e Contato.

```python
path('', include('pages.urls'))
```

* **portfolio/** : Gerencia as rotas relacionadas aos portfólios dos usuários.

```python
path('portfolio/', include('portfolios.urls'))
```

* **users/** : Define as rotas relacionadas ao sistema de autenticação e perfis de usuários.

```python
path('users/', include('custom_auth.urls'))
```

## Servindo Arquivos de Mídia

Durante o desenvolvimento, os arquivos de mídia (imagens, uploads) são servidos pela configuração:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Isso garante que os arquivos na pasta `media/` sejam acessíveis em desenvolvimento.
