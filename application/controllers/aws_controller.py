import json
import os

from boto3 import client
from flask import Blueprint, request

from application.services.product_service import ProductService

sign_s3_blueprint = Blueprint('/sign_s3/', __name__)


@sign_s3_blueprint.route('/sign_s3/')
def sign_s3():
    s3_bucket = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = client('s3')

    new_id = 1

    product_service = ProductService()
    try:
        new_id = product_service.find_last_id() + 1
    except Exception as error:
        from run import app
        app.logger.error(error)

    file_name_to_save = 'image_'+str(new_id)

    pre_signed_post = s3.generate_presigned_post(
        Bucket=s3_bucket,
        Key=file_name_to_save,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': pre_signed_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (s3_bucket, file_name)
    })
