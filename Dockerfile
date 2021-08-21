FROM python:3.7

RUN python3 -m pip install -U pip

RUN pip install dash python-dotenv numpy pandas Flask-SQLAlchemy gunicorn dash-bootstrap-components

RUN python3 -m pip install -v pystan==2.19.1.1

RUN pip install statsmodels

RUN pip install pmdarima

RUN pip install  fbprophet==0.7.1

WORKDIR /var/www 
