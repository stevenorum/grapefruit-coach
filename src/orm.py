import boto3
import os
from stack_info import STACK_OUTPUTS
from toco.object import CFObject

class User(CFObject):
    _CF_STACK_NAME = os.environ.get("STACK_NAME")
    _CF_LOGICAL_NAME = "UserTable"

class Object(CFObject):
    _CF_STACK_NAME = os.environ.get("STACK_NAME")
    _CF_LOGICAL_NAME = "ObjectTable"

class Image(CFObject):
    _CF_STACK_NAME = os.environ.get("STACK_NAME")
    _CF_LOGICAL_NAME = "ImageTable"

    def _presigned_url(self, lifetime_minutes=60):
        return boto3.client("s3").generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket':self.s3bucket if self.s3bucket else STACK_OUTPUTS["PhotoBucket"],'Key':self.s3key if self.s3key else self.image_name},
            ExpiresIn=60*lifetime_minutes
        )

    @property
    def _temp_url(self):
        return self._presigned_url(lifetime_minutes = 60*24*14)
