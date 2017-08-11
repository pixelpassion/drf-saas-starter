# 1 Use the Python Slim
FROM python:3.6.2-slim

# 2 Force stdin, stdout and stderr to be totally unbuffered and don´t write .pyc or .pyo files
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# 3 Install required system packages
RUN apt-get update \
    && apt-get install -y postgresql-client libpq-dev gettext gcc git build-essential libssl-dev libffi-dev python-dev \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# 4 Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements/local.txt /requirements/local.txt

# 5 Update PIP and install the local requirements
RUN pip install -r /requirements/local.txt \
    && groupadd -r django \
    && useradd -r -g django django

# 6 Copy the project folder
COPY . /app/

# 7 Copy the starting script

COPY ./docker/django/start_daphne.sh /start_daphne.sh

# 8 Set the rights to access the files
RUN sed -i 's/\r//' /start_daphne.sh \
    && chmod +x /start_daphne.sh \
    && chown django /start_daphne.sh \
    && chown -R django /app

# 9 Set the working dir
WORKDIR /app
