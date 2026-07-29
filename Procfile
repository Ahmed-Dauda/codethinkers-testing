#web: uvicorn school.asgi:application --host=0.0.0.0 --port=$PORT

web: bin/start-pgbouncer uvicorn school.asgi:application --host=0.0.0.0 --port=$PORT
# In your deploy/start script:
nohup python /var/www/codethinkers-staging/project_router.py > /var/log/project_router.log 2>&1 &