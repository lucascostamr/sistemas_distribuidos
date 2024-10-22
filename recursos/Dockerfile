FROM python:3.12-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update\
    && apt-get -y upgrade

WORKDIR /home/user/app

COPY . .

RUN pip install --no-cache -r requirements.txt

ENV PYTHONPATH="/home/user/app/src"

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python --version" ]

CMD ["sh"]
