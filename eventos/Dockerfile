FROM python:3.12-slim

RUN apt-get update\
    && apt-get -y upgrade\
    && apt-get install -y tk

WORKDIR /home/user/app

COPY . .

ENV PYTHONPATH="/home/user/app"
ENV DISPLAY=:0

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python --version" ]

CMD ["sh"]
