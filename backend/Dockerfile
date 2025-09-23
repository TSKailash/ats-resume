FROM python:3.13.7

WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r /backend/requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]