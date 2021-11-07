# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from settings import SMS


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
        # args: List[str],
            phone,
            code
    ) -> None:
        client = Sample.create_client(SMS.key, SMS.secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=SMS.sign_name,
            template_code=SMS.template_code,
            template_param='{"code": %s}' % code
        )
        # 复制代码运行请自行打印 API 的返回值
        res =  client.send_sms(send_sms_request)
        print(res)

    @staticmethod
    async def main_async(
        # args: List[str],
            phone,
            code
    ):
        client = Sample.create_client(SMS.key, SMS.secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=SMS.sign_name,
            template_code=SMS.template_code,
            template_param='{"code": %s}' % code
        )
        # 复制代码运行请自行打印 API 的返回值
        res = await client.send_sms_async(send_sms_request)
        return res


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
