FROM python:3.10-buster
COPY . /covidExposure
RUN apt update && apt install -y build-essential libzbar-dev 
RUN pip install -r /covidExposure/requirements.txt
WORKDIR /
# FIXME: remove credentials in source code
ENV FLASK_APP=covidExposure GCP_MAPS_API_KEY=AIzaSyAQg_2Oe_8l_6hq3hgW4IOrIdwq2M--qI0
EXPOSE 5000
ENTRYPOINT [ "flask" ]
CMD ["run", "--with-threads", "--host=0.0.0.0"]
