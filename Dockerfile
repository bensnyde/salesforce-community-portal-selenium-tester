FROM python:slim-buster
COPY requirements.txt .
COPY ./src .
RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]
