from boto3 import resource
from helpers.getSecret import get_secret



# gets the secret data and changes it to a dict for use
awsData = get_secret("aws-cli-access-keys", "us-west-1")

data = resource(
  'dynamodb',
  aws_access_key_id     = awsData['aws_access_key_id'],
  aws_secret_access_key = awsData['aws_secret_access_key'],
  region_name           = awsData['aws_region']
)


