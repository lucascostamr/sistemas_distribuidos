FROM python:3.12-slim

RUN apt-get update\
    && apt-get -y upgrade

WORKDIR /home/user/app

COPY . .

RUN pip install --no-cache-dir rpyc==6.0.1

ENV PYTHONPATH="/home/user/app"

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python --version" ]

CMD ["sh"]
