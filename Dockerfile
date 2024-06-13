FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /app

CMD ["sh", "-c", "python /app/db.py && uvicorn main:app --reload --host 0.0.0.0 --port 8000"]
