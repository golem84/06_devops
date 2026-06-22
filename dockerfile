FROM python:3.12-slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY app.py .

STOPSIGNAL SIGTERM

CMD ["flask", "run", "--debug"]