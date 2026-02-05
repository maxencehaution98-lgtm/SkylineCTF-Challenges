FROM python:3.9-alpine
RUN apk add --no-cache iputils curl
RUN pip install flask
COPY src/app.py /app/
COPY src/flag.txt /flag.txt
RUN chmod 444 /flag.txt
WORKDIR /app
CMD ["python", "app.py"]

