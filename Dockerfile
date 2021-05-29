FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ ./
ENV PYTHONPATH="/app"
EXPOSE 80
CMD gunicorn -w 4 -b [::]:80 "wsgi:create_app()"