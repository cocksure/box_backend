FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root


COPY requirements.txt /app/
WORKDIR /app
RUN python -m pip install --no-cache-dir -U pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
#CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8030"]
#CMD ["daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8001"]