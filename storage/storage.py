import boto3

from django.conf import settings


def storage_client():
    session = boto3.session.Session()
    client = session.client(
        's3',
        region_name=settings.STORAGE_REGION,
        endpoint_url=settings.STORAGE_S3_CUSTOM_DOMAIN,
        aws_access_key_id=settings.STORAGE_ACCESS_KEY_ID,
        aws_secret_access_key=settings.STORAGE_SECRET_ACCESS_KEY
    )
    return client


def get():
    pass


def save(fileobj, location, key, public=False):
    client = storage_client()
    extra_args = {}
    if public:
        extra_args['ACL'] = 'public-read'

    key = '/'.join([location, key])
    if settings.ENVIRONMENT != 'production':
        key = '/'.join([settings.ENVIRONMENT, key])

    client.upload_fileobj(fileobj, settings.STORAGE_BUCKET_NAME, key, ExtraArgs=extra_args)
