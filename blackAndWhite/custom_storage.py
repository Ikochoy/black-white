from storages.backends.s3boto3 import S3Boto3Storage

class ProductStorage(S3Boto3Storage):
    bucket_name = 'molekiu-black-white'
    location = 'media/products'

class BlogCritiqueCoverStorage(S3Boto3Storage):
    bucket_name = 'molekiu-black-white'
    location = 'media/blogs_critiques_covers'

class ProfileStorage(S3Boto3Storage):
    bucket_name = 'molekiu-black-white'
    location = 'media/profiles'

