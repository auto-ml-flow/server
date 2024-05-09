# server
Server for tracking user ML actions and help to improve models

# Starting for development
```bash
cp .env.local .env
```

```bash
docker compose up -d
```

```python
python manage.py migrate
```

```python
python manage.py runserver
```

It is more convenient to work via makefile
### Just start everything in one command
```bash
make local
```

### Copy local env to .env
```bash
make env
```

### Run postgres/redis/rabbit (third party apps)
```bash
make start_third_party
```

### Run development app
```bash
make run
```

### Clean environment
```bash
make clean
```

### Requirements
```bash
make requirements
```

Export poetry environment to requirements.txt  
Very good for docker image size  

### Build docker image
```bash
make docker
```