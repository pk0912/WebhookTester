## Webhook Tester
#### Django and Vue based project to test out web hooks by creating unique HTTP endpoints for the web hooks to hit and test their content.


### Setup locally

#### For Django Project
Create virtual environment (using virtualenvwrapper)
```bash
$ cd webhook_tester
$ workon created_virtualenv
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

For populating database with unique endpoint names beforehand
```bash
$ python manage.py insert_url_names
```

#### For Vue part
```bash
$ cd webhook_tester/ui
$ npm install
$ npm run serve
```

#### For Celery Tasks
Install Redis using following link:
https://redis.io/topics/quickstart

For celery worker (run within same virtual environment)
```bash
$ celery -A webhook_tester worker -l INFO
```

For celery beat (run within same virtual environment)
```bash
$ celery -A webhook_tester beat -l INFO
```

### Production deployment

Using nginx, gunicorn on AWS EC2 machine.

Associating elastic IP with EC2 instance for static ip to access the project.
Also adding a security group with inbound rules to allow access to ports 22 and 80.

Building out the dist folder or the vue content and serving them as static content in nginx conf.

