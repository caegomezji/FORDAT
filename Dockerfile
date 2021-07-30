FROM python

RUN python3 -m pip install -U pip

RUN pip install dash python-dotenv numpy pandas Flask-SQLAlchemy gunicorn

WORKDIR /var/www