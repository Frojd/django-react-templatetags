FROM python:3.6

RUN apt-get update && apt-get install -y \
    netcat \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
    binutils libproj-dev

ENV PYTHONUNBUFFERED 1
ENV APP_LOG_DIR /var/log/app

ADD . /app/
WORKDIR /app

RUN pip install -r requirements.txt

# Install and setup vim
RUN apt-get update && apt-get install -y vim curl
RUN curl -L https://raw.githubusercontent.com/marteinn/Notebook/master/vim/vim-server-conf.vimrc > ~/.vimrc

EXPOSE 8080

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["runserver"]
