#Linux Version
FROM python:3

# set working diretory
WORKDIR /

# Copy Flask application code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
