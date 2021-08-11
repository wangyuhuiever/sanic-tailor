FROM python:3.8-alpine

ENV PROJECTS_DIR=/opt/sanic

COPY . $PROJECTS_DIR

COPY ./entrypoint.sh /
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add gcc make g++

# 安装项目依赖包
RUN pip3 install -r $PROJECTS_DIR/requirements.txt -i https://pypi.douban.com/simple

EXPOSE 5000

WORKDIR $PROJECTS_DIR

ENTRYPOINT ["/entrypoint.sh"]