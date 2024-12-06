FROM python:3.9-slim-buster

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

# Copy or mount node app here
WORKDIR /data/

EXPOSE 3000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000"]