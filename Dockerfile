FROM node:14.15.3-buster as ui
WORKDIR /app
COPY . /app
WORKDIR /app/ui/static
RUN npm install -g gulp
RUN npm install gulp
RUN npm install
RUN npm rebuild node-sass
RUN cp node_modules/bootstrap-maxlength/dist/bootstrap-maxlength.min.js node_modules/bootstrap-maxlength
RUN gulp build

FROM python:3.8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get install -y gettext rsync
RUN pip3 install -r requirements.txt
COPY . /app
COPY --from=ui /app/ui/static /app/ui/static

CMD ["./bin/run"]
