FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 72

WORKDIR /home
# COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "72", "--reload"]