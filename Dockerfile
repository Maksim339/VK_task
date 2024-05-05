FROM python:3.8-slim as builder

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/code

RUN pytest

FROM python:3.8-slim as production

WORKDIR /code

COPY --from=builder /code /code

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/code

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]