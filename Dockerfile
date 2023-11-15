FROM python:3.9.16

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]