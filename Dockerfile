FROM python:3.10-buster
COPY ./requirements.txt /covidExposure/requirements.txt
RUN apt update && apt install -y build-essential libzbar-dev 
RUN pip install -r /covidExposure/requirements.txt
COPY . /covidExposure
WORKDIR /
ENV FLASK_APP=covidExposure
EXPOSE 5000
ENTRYPOINT [ "flask" ]
CMD ["run", "--with-threads", "--host=0.0.0.0"]
