FROM python:alpine

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD ["manage.py", "runserver"]
