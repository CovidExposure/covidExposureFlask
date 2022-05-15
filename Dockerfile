FROM python:3.10-alpine
COPY . /covidExposure
RUN pip install -r /covidExposure/requirements.txt
WORKDIR /
ENV FLASK_APP=covidExposure
EXPOSE 5000
ENTRYPOINT [ "flask" ]
CMD ["run", "--with-threads", "--host=0.0.0.0"]
