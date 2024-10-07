FROM python:3.12-slim

# RUN curl -sSL https://install.python-poetry.org | python3 -

# RUN pip install poetry

RUN ls

RUN pip install --no-cache-dir poetry==1.8.3

# RUN mkdir /horse_club_app

WORKDIR  /horse_club_app

COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false

RUN poetry install

# RUN poetry build

COPY . .

# ECHO ls
# ECHO pip freeze

# CMD ls

# CMD python main.py

CMD  gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
