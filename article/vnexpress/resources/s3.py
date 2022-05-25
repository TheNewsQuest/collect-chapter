from article._base.resources.s3 import build_s3_resource
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key

vnexpress_s3_resource = build_s3_resource(Providers.VNEXPRESS)
vnexpress_s3_resource_key = build_resource_key(Providers.VNEXPRESS,
                                               ResourceKeys.S3_RESOURCE_PREFIX)
