import sys
import os
import requests

from qiniu import Auth, put_file, etag

import qiniu.config

access_key = sys.argv[1]
secret_key = sys.argv[2]

#构建鉴权对象
q = Auth(access_key, secret_key)

key = 'Birthday-Calendar/config.yaml'
localfile = 'config.yaml'


def upload(bucket_name, local_config_file_path):
    #上传后保存的文件名

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径

    ret, info = put_file(token, key, local_config_file_path)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(local_config_file_path)


def download(bucket_domain, key):
    # 有两种方式构造base_url的形式
    base_url = 'http://%s/%s' % (bucket_domain, key)

    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    print(f"private_url: {private_url}")
    r = requests.get(private_url)
    print(f"r.text:\n{r.text}")
    with open(localfile, 'wb') as f:
        f.write(r.content)
    assert r.status_code == 200


if __name__ == '__main__':
    # upload: python utils/qiniu_api.py AK SK bucket_name local_config_file_path
    if len(sys.argv) > 4:
        bucket_name = sys.argv[3]
        local_config_file_path = sys.argv[4]
        upload(bucket_name, local_config_file_path)
    # download: python utils/qiniu_api.py AK SK bucket_domain
    else:
        bucket_domain = sys.argv[3]
        download(bucket_domain, key)
