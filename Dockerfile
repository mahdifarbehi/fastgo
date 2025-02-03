FROM python:3.12
WORKDIR /main
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY src .
CMD ["python3", "main.py"]