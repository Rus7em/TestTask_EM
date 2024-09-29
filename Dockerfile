FROM python:3.12.4-slim

WORKDIR /code

copy ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

copy ./src /code/src

cmd ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", --port", "80"]

