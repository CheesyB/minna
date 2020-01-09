FROM python:3.8
COPY . /app
WORKDIR /app
RUN ip add
RUN pip install -r requirements.txt


CMD ["python", "minna/minna.py"]
