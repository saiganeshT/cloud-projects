import boto3
import argparse
import json
import time

def create_table(table_name, dynamodb):

  existing_tables = list(dynamodb.tables.all())
  
  # create a table if does not exist
  if table_name not in [table.name for table in existing_tables]:
    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'date',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'station',
                'AttributeType': 'S',
            }],
        KeySchema=[
            {
                'AttributeName' : 'station',
                'KeyType'       : 'HASH'
            },
            
            {
                'AttributeName' : 'date',
                'KeyType'       : 'RANGE'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits'  : 5,
            'WriteCapacityUnits' : 5,
        },
        
        TableName=table_name   
    )

    print("Table Created!")

  else:
    print("The already exits!")

# parse all the required arguments
parser = argparse.ArgumentParser()
parser.add_argument('key_id', type=str, help="Enter your AWS ACESS KEY ID")
parser.add_argument('key', type=str, help='Enter your AWS SECRET ACCESS KEY')
parser.add_argument('region', type=str, help = 'Enter the AWS region')
args = parser.parse_args()

dynamodb = boto3.resource('dynamodb')

table1_name = 'Temperature'
table2_name = 'Precipitation'

create_table(table1_name, dynamodb)
create_table(table2_name, dynamodb)


# sleep for 30 to wait for the creation of tables in AWS
time.sleep(30)

temperature_table = dynamodb.Table('Temperature')
precipitation_table = dynamodb.Table('Precipitation')


# Create a kinesis client
my_stream_name = "weather-pipeline"
kinesis_client = boto3.client('kinesis', region_name = args.region, 
                                aws_access_key_id = args.key_id, 
                                aws_secret_access_key = args.key)
                                
                                
response = kinesis_client.describe_stream(StreamName=my_stream_name)


my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']
shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                   ShardId=my_shard_id,
                                                   ShardIteratorType='TRIM_HORIZON')

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=1)

while 'NextShardIterator' in record_response:
  record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=1)
  
  record = record_response['Records']
  if record:
    item = record[0]['Data'].decode()
    item = json.loads(item)
    
    if item['datatype'] == 'PRCP' or item['datatype'] == 'SNOW':
      item.pop('datatype')
      item.pop('attributes')
      precipitation_table.put_item(Item=item)
      print("Item is inserted in precipitation table!")

    elif item['datatype'] == 'TOBS':
        item.pop('datatype')
        item.pop('attributes')
        temperature_table.put_item(Item=item)
        print("Item is inserted in temperature table!")
  else:
    break

print("Items are inserted!")