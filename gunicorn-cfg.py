import multiprocessing

# Bind address and port
bind = "0.0.0.0:8000"

# Número de workers (geralmente 2-4 workers por CPU)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class (default é sync, mas pode usar gevent, eventlet etc.)
worker_class = "sync"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Keep-alive
keepalive = 120

# Tempo limite para os workers
timeout = 30
