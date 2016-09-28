#!/usr/bin/env python
import json
import boto3
import time
import urllib
from PIL import Image


new_bucket = 'pylambda-thumb'
s3 = boto3.client('s3')
size = 128, 128

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])
    local_file = '/tmp/{}'.format(key)
    out_path = local_file.replace(".jpg","-thumb.jpg")

    s3.download_file(bucket, key, local_file)

    im = Image.open(local_file)
    im.thumbnail(size)
    im.save(out_path)

    s3.upload_file(out_path, new_bucket, key)