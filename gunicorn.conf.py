# Gunicorn configuration for low memory
workers = 1
threads = 2
timeout = 120
max_requests = 100
max_requests_jitter = 10
graceful_timeout = 30

# Memory limits
worker_class = 'sync'
limit_request_line = 4094
limit_request_fields = 100