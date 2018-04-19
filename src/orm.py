import boto3
import os
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
