# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7.4
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV FLASK_ENV=development
ENV FLASK_APP=run.py
ENTRYPOINT ["python"]
CMD ["run.py"]