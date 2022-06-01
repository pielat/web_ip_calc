FROM python

MAINTAINER Adam Pielatowski "pielatowski@gmail.com"

COPY . /app

WORKDIR /app

RUN python setup.py develop

ENV FLASK_APP web_ip_calc

COPY . /app

CMD [ "flask", "run", "--host=0.0.0.0" ]

