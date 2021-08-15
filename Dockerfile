FROM python:3.8.5-alpine3.12
MAINTAINER wangyuhuiyi@gmail.com

ENV PROJECTS_DIR=/opt/sanic
ENV USER=sanic

COPY . $PROJECTS_DIR

COPY ./entrypoint.sh /

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev make g++ tzdata && \
 cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
 pip3 install -r $PROJECTS_DIR/requirements.txt -i https://pypi.douban.com/simple && \
 apk --purge del .build-deps

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$PROJECTS_DIR" \
    --no-create-home \
    "$USER"

EXPOSE 5000 5555

WORKDIR $PROJECTS_DIR
USER $USER

ENTRYPOINT ["/entrypoint.sh"]