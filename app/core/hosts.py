from django_hosts import patterns, host

def debug_host(hostname):
    print(f"Capturando Host: {hostname}")

host_patterns = patterns(
    '',
    host(r'(?P<username>[\w-]+)', 'portfolios.ultra.urls', name='user-subdomain', callback=debug_host),
    host(r'www', 'core.urls', name='www'),  # Domínio principal
    host(r'', 'core.urls', name='default'),  # Domínio sem subdomínio (portfolizer.com.br)
)
