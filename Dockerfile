FROM python:3.8.18
WORKDIR /app
COPY . /app
RUN apt update -y && apt install awscli -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]