FROM python:3.9.13
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /quora
COPY requirements.txt /quora/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /quora/