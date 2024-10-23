from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'(?P<username>[\w-]+)', 'portfolios.ultra.urls', name='user-subdomain'),  # Subdomínios dinâmicos
    host(r'www', 'core.urls', name='www'),  # Domínio principal
    host(r'', 'core.urls', name='default'),  # Domínio sem subdomínio (portfolizer.com.br)
)
