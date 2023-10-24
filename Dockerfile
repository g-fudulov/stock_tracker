FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY python-requiremets.txt /app/
#COPY package.json /app/
RUN pip install -r python-requiremets.txt
#RUN npm install
#Make npm install work
COPY . /app/