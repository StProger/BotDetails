FROM python:3.10
WORKDIR /app
RUN pip3 install --upgrade --no-cache-dir setuptools
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && chmod 755 .
COPY . .
CMD [ "python3", "main.py" ]

