FROM python:3.7

RUN apt update && apt install sshpass

RUN pip install fastapi uvicorn python-dotenv

EXPOSE 80

WORKDIR /home
# COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]