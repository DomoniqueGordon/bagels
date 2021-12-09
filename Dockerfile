FROM python:latest

WORKDIR /bagels

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]