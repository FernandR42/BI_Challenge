import json
import boto3
import datetime

DEFAULT_S3_IMAGE_PAYLOAD_NAME = 'image-monitoring-payload'
DEFAULT_DYNAMO_TABLE_NAME = 'image-monitoring-table'

def archive_image(image):

	file_name = image["image_id"]
	today = datetime.date.today()
	s3_path = str(today) + '/' + file_name

	s3 = boto3.resource("s3")
	s3.Bucket(DEFAULT_S3_IMAGE_PAYLOAD_NAME).put_object(Key=s3_path, Body=json.dumps(image))

def store_image(image):

	dynamodb = boto3.client('dynamodb')
	
	dynamodb.put_item(TableName=DEFAULT_DYNAMO_TABLE_NAME, Item={
		'id':{'S':image['image_id']},
		'event_name':{'S': image['event_name']},
		'user_id':{'S': image['user_id']},
		'timestamp':{'S': image['timestamp']}
	})

def main(event, context):

	payload = event['Records'][0]['body']
	image = json.loads(payload)
	
	archive_image(image)
	store_image(image)