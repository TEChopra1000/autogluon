
import os
import pickle
import tempfile
import logging

import boto3

from tabular.utils import s3_utils

logger = logging.getLogger(__name__)

def save(path, object, format=None):
    pickle_fn = lambda o, buffer: pickle.dump(o, buffer, protocol=4)
    save_with_fn(path, object, pickle_fn, format)


def save_with_fn(path, object, pickle_fn, format=None):
    print('Saving', path)
    if s3_utils.is_s3_url(path):
        format = 's3'
    if format == 's3':
        save_s3(path, object, pickle_fn)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fout:
            pickle_fn(object, fout)


def save_s3(path: str, obj, pickle_fn):
    logger.info(f'save object to {path}')
    with tempfile.TemporaryFile() as f:
        pickle_fn(obj, f)
        f.flush()
        f.seek(0)

        bucket, key = s3_utils.s3_path_to_bucket_prefix(path)
        s3_client = boto3.client('s3')
        try:
            config = boto3.s3.transfer.TransferConfig()   # enable multipart uploading for files larger than 8MB
            response = s3_client.upload_fileobj(f, bucket, key, Config=config)
        except:
            logger.exception('failed to save object')
            raise
