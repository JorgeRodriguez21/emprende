import json
import os

from boto3 import client
from flask import Blueprint, request

from application.services.product_service import ProductService

sign_s3_blueprint = Blueprint('/sign_s3/', __name__)


@sign_s3_blueprint.route('/sign_s3/')
def sign_s3():
    from run import app
    s3_bucket = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = client('s3')

    new_id = 1

    product_service = ProductService()
    try:
        row = product_service.find_last_id()
        if row is not None:
            if row[0] is not None:
                new_id = row[0] + 1
    except Exception as error:
        app.logger.error(error)

    file_name_to_save = 'image_' + str(new_id)

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

    from run import app
    app.logger.error('variables')
    app.logger.error(s3_bucket)
    app.logger.error(file_name)
    app.logger.error(file_name_to_save)
    app.logger.error('https://%s.s3.amazonaws.com/%s' % (s3_bucket, file_name_to_save))

    return json.dumps({
        'data': pre_signed_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (s3_bucket, file_name_to_save)
    })
