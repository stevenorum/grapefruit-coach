import os
from toco.object import CFObject

User = CFObject.lazysubclass(stack_name=os.environ.get("STACK_NAME"), logical_name="UserTable")
Image = CFObject.lazysubclass(stack_name=os.environ.get("STACK_NAME"), logical_name="ImageTable")
Object = CFObject.lazysubclass(stack_name=os.environ.get("STACK_NAME"), logical_name="ObjectTable")

