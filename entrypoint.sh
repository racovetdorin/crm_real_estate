rsync -arv ui/templates_default/ ui/templates &&
rsync -arv ui/templates_ipk/ ui/templates &&
gunicorn crm.asgi:application --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker --workers 2 --log-file=- --log-level debug
