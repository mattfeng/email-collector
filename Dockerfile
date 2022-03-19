FROM python:3.9

ADD main.py /
ADD requirements.txt /
RUN pip install -r requirements.txt

CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0", "main:create_app()"]