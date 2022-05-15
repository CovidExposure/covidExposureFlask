FROM python:3.10-alpine
COPY ./requirements.txt /covidExposure/requirements.txt
WORKDIR /covidExposure
RUN pip install -r requirements.txt
COPY . /covidExposure
WORKDIR /
ENTRYPOINT [ "flask" ]
CMD ["run", "--with-threads"]
