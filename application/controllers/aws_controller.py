import json
import os

from boto3 import client
from flask import Blueprint, request

from application.middleware.is_user_logged import check_is_admin
from application.services.product_service import ProductService

sign_s3_blueprint = Blueprint('/sign_s3/', __name__)


@sign_s3_blueprint.route('/sign_s3/')
@check_is_admin
def sign_s3():
    from run import app
    s3_bucket = os.environ.get('S3_BUCKET')

    file_type = request.args.get('file_type')
    id_received = request.args.get('id')

    s3 = client('s3')
    new_id = 0
    if int(id_received) == 0:
        try:
            product_service = ProductService()
            row = product_service.find_last_id()
            if row is not None:
                if row[0] is not None:
                    new_id = row[0] + 1
        except Exception as error:
            app.logger.error(error)
    else:
        new_id = int(id_received)

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

    return json.dumps({
        'data': pre_signed_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (s3_bucket, file_name_to_save)
    })
