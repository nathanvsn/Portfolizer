from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'admin', 'core.urls_admin', name='admin'),  # Subdomínio admin
    host(r'www', 'core.urls', name='www'),  # Domínio principal
    host(r'', 'core.urls', name='default'),  # Domínio sem subdomínio (portfolizer.com.br)
)
