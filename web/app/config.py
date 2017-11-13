import os

CONFIG = {
    'postgres': {
        'database': os.environ.get('POSTGRES_DATABASE', 'docker_aiohttp'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'user': os.environ.get('POSTGRES_USER', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': int(os.environ.get('POSTGRES_PORT', 5432)),
        'statement_cache_size': int(os.environ.get('STATEMENT_CACHE_SIZE', 0))
    },
    'redis': {
        'host': os.environ.get('REDIS_HOST', 'localhost'),
        'port': int(os.environ.get('REDIS_PORT', 6379)),
    },
    'host': os.environ.get('HOST', 'localhost'),
    'port': int(os.environ.get('PORT', 8080)),
    'secret_key': os.environ.get('SECRET_KEY', '91L1JPWq3M0fp19o2OG3Z107fKzMoYXI'),
    'template_dir': os.path.join(
        os.path.basename(os.path.dirname(os.path.realpath(__file__))),
        'templates'
    )
}
