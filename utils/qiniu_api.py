import sys
import os
import requests

from qiniu import Auth, put_file, etag

import qiniu.config

access_key = sys.argv[1]
secret_key = sys.argv[2]
# bucket_name = sys.argv[3]    # upload
bucket_domain = sys.argv[3]    # download
#构建鉴权对象
q = Auth(access_key, secret_key)

key = 'Birthday-Calendar/config.yaml'
localfile = '../config.yaml.yaml'

def upload(bucket_name, key):
    #上传后保存的文件名


    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径

    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


def download(bucket_domain, key):
    # 有两种方式构造base_url的形式
    base_url = 'http://%s/%s' % (bucket_domain, key)

    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    print(private_url)
    r = requests.get(private_url)
    with open('../config.yaml', 'wb') as f:
        f.write(r.content)
    print(os.getcwd())
    os.walk(os.getcwd())
    os.walk('..')
    assert r.status_code == 200


if __name__ == '__main__':
    # upload(bucket_name, key)
    download(bucket_domain, key)
