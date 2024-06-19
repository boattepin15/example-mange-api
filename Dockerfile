FROM python:3.9-alpine3.13
LABEL maintainer="boatbot.seven"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# ติดตั้ง dependencies ที่จำเป็นสำหรับ Pillow และ PostgreSQL
RUN apk add --update --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers \
    zlib-dev \
    jpeg-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    libimagequant-dev \
    libwebp-dev \
    libxcb \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt

RUN adduser \
        --disabled-password \
        --home /home/django-user \
        django-user && \
        mkdir -p /vol/web/media && \
        mkdir -p /vol/web/media && \
        chown -R django-user:django-user /vol && \
        chmod -R 755 /vol


ENV PATH="/py/bin:$PATH"

USER django-user

# กำหนดโฟลเดอร์สำหรับไฟล์สื่อ
VOLUME /app/media
