FROM python:3.7-slim

WORKDIR /gps-tracker

RUN apt-get update

RUN apt-get install -y git binutils libproj-dev gdal-bin python-virtualenv

RUN apt-get clean

COPY requirements.txt /gps-tracker/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY geo /gps-tracker

WORKDIR /gps-tracker
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
