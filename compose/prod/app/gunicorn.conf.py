from __future__ import annotations

import multiprocessing

module = "ruian"
name = module
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "-"
errorlog = "-"
loglevel = "debug"
worker_tmp_dir = "/dev/shm"  # nosec
user = "root"
timeout = 120
