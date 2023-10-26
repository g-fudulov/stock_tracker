FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY python-requiremets.txt /app/
RUN pip install -r python-requirements.txt
COPY . /app/