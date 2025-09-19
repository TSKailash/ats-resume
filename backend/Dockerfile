FROM python:3.13.7

WORKDIR /backend

COPY requirements.txt
RUN pip -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]