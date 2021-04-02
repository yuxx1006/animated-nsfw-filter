FROM python:3.8

ENV MONGO 127.0.0.1:27017/troph

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# CMD ["gunicorn", "main:app", "-c", "./gunicorn.conf.py" ]
CMD [ "sh", "-c", "python ./main.py" ]


