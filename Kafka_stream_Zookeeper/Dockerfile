FROM python:3.9-slim

WORKDIR /app

COPY stock_data_stream.py /app

RUN pip install requests kafka-python

CMD ["python", "stock_data_stream.py"]
