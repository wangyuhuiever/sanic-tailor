FROM python:3.8-alpine

ENV PROJECTS_DIR=/opt/sanic
ENV USER=sanic

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add gcc make g++

COPY . $PROJECTS_DIR

COPY ./entrypoint.sh /

# 安装项目依赖包
RUN pip3 install -r $PROJECTS_DIR/requirements.txt -i https://pypi.douban.com/simple

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