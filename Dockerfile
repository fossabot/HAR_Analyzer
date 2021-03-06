FROM python:3.8.6-slim-buster

ARG BUILD_DATE
ARG VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/Cyb3r-Jak3/HAR_Analyzer.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.schema-version="1.0.0-rc1"

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

COPY app /usr/src/app/app

WORKDIR /usr/src/app

ENTRYPOINT ["gunicorn", "-k", "gevent", "--bind", "0.0.0.0", "--workers", "8", "app:app"]