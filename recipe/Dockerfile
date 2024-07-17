FROM diliplakshya/python-3.11.1-poetry-slim-bullseye 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

ADD . /api/
# https://stackoverflow.com/questions/10919569/install-a-module-using-pip-for-specific-python-version
RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install -r requirements.txt

EXPOSE 8000

CMD ["python3.11", "manage.py", "runserver", "0.0.0.0:8000"]