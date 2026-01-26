FROM python:3.12-slim AS builder

WORKDIR /install
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY --from=builder /wheels /wheels

COPY requirements.txt requirements.txt

RUN pip install --no-index --find-links=/wheels -r requirements.txt

COPY ./ ./

CMD ["python", "-m", "app.main"]
