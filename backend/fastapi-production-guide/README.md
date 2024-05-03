# FastAPI Production Guide

## Setup

```bash
# setup to create .venv in project directory
poetry config --list
poetry config virtualenvs.in-project true

poetry add fastapi 'uvicorn[standard]'
poetry add -G dev ruff black mypy
poetry add python-dotenv pydantic-settings

# Async MongoDB driver
poetry add motor
poetry add -G dev motor-types

# Async HTTP client
poetry add httpx

# Testing
poetry add -G dev pytest coverage mongomock-motor pytest_httpx pytest-asyncio setuptools

export TESTING=true && poetry run coverage run --source ./app -m pytest --disable-warnings
poetry run coverage html

# Production
poetry add gunicorn
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app.main:app

# Benchmark with Apache Benchmark (ab)
curl -X 'GET' \
  'http://localhost:8000/v1/todos' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer githubaccesstoken'

# 50000 requests with 1000 concurrent requests (QPS)
ab -n 50000 -c 1000  -H 'Authorization: Bearer githubaccesstoken' http://localhost:8000/v1/todos

# Containerize
docker build . -t fastapi-todos:1.0.0
docker run -p 8000:8000 --env-file .env fastapi-todos:1.0.0

# Adding Nginx as reverse proxy
# Generate self-signed certificate (in production, use Let's Encrypt)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./certs/nginx-selfsigned.key -out ./certs/nginx-selfsigned.crt

# Kubernetes Deployment
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl create secret generic my-todos-api-secret --from-env-file=.env --dry-run=client -o yaml

# Kubernetes Deployment with Kustomize
cd k8s
kustomize build . | kubectl apply -f -

```

Extra config for dev tools:

```toml
[tool.black]
line-length = 88

[tool.ruff]
linter.select = ["E", "F", "I"]
linter.fixable = ["ALL"]
exclude = [".git", ".mypy_cache", ".ruff_cache"]
line-length = 88

[tool.mypy]
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
strict_equality = true
disallow_untyped_decorators = false
ignore_missing_imports = true
implicit_reexport = true
plugins = "pydantic.mypy"

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
warn_untyped_fields = true
```

## Benchmark Result

### Benchmark command

```bash
ab -n 50000 -c 1000  -H 'Authorization: Bearer githubaccesstoken' http://localhost:8000/v1/todos
```

### Result with 1 uvicorn worker

```bash
uvicorn app.main:app --host 0.0.0.0 --workers 1

# Requests per second:    915.73 [#/sec] (mean)
# Time per request:       1092.027 [ms] (mean)
# Time per request:       1.092 [ms] (mean, across all concurrent requests)
# Transfer rate:          4810.16 [Kbytes/sec] received
```

### Result with 10 uvicorn worker

```bash
uvicorn app.main:app --host 0.0.0.0 --workers 10

# Requests per second:    5232.86 [#/sec] (mean)
# Time per request:       191.100 [ms] (mean)
# Time per request:       0.191 [ms] (mean, across all concurrent requests)
# Transfer rate:          27487.68 [Kbytes/sec] received
```

### Result with gunicorn sync worker and 10 `uvicorn.workers.UvicornWorker`

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 10 app.main:app

# Requests per second:    6351.38 [#/sec] (mean)
# Time per request:       157.446 [ms] (mean)
# Time per request:       0.157 [ms] (mean, across all concurrent requests)
# Transfer rate:          33363.16 [Kbytes/sec] received
```

### Result with gunicorn sync worker and 10 `uvicorn.workers.UvicornWorker` in Docker

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 10 app.main:app

# Requests per second:    6095.56 [#/sec] (mean)
# Time per request:       164.054 [ms] (mean)
# Time per request:       0.164 [ms] (mean, across all concurrent requests)
# Transfer rate:          32019.33 [Kbytes/sec] received
```

## Reference

[FastAPI Production Setup Guide 🏁⚡️🚀](https://dev.to/dpills/fastapi-production-setup-guide-1hhh)
[GitHub - dpills/fastapi-prod-guide: FastAPI Production Setup Guide ⚡️🚀🏁](https://github.com/dpills/fastapi-prod-guide)
[gunicorn 高性能wsgi服务器 - 金色旭光 - 博客园](https://www.cnblogs.com/goldsunshine/p/16979098.html)
[Settings — Gunicorn 22.0.0 documentation](https://docs.gunicorn.org/en/stable/settings.html)
