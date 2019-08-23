import os

# Amazon Product API related
AWS_PRODUCT_API_VERSION = "2013-08-01"
AWS_ACCESS_KEY_ID = 'your value'
AWS_SECRET_ACCESS_KEY = 'your value'
AWS_ASSOCIATE_TAG = 'your value'
AWS_PRODUCT_API_SERVICE = 'AWSECommerceService'
AWS_PRODUCT_API_REGION = 'UK'

# eBay
EBAY_APP_ID = 'your value'
EBAY_DEV_ID = 'your value'
EBAY_CERT_ID = 'your value'
EBAY_GLOBAL_ID = 'EBAY-US'
EBAY_SITE_ID = '0'


# Flask related
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'data.db')
DATABASE_TEST_URI = 'sqlite:///' + os.path.join(_basedir, 'test.db')
DATABASE_CONNECT_OPTIONS = {}

#files path
FILES_PATH = os.path.join(_basedir, 'files')
