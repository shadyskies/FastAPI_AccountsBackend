FROM python:3.9 as build-stage
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./core /code/core

CMD ["uvicorn", "core.main:app"]
