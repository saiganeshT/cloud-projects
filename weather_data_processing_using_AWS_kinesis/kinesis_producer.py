import boto3
import argparse
import requests
import json
import time


# function to get the weather records
def get_noaa_data(url, token, **kwargs):
  request_type = 'data'
  header = {'token': token}

  r = requests.get(url + request_type, headers=header, params=kwargs)

  # print if the request doesn't go through
  if r.status_code != 200:  
      print("Error: " + str(r.status_code))
  else:
      r = r.json()
      try:
          # get the actual data 
          return r['results'] 
      except KeyError:
          # if the data is not nested return the whole JSON string
          return r  

# function to get station data
def get_noaa_station_data(url, token, **kwargs):
  request_type = 'stations'
  header = {'token': token}

  r = requests.get(url + request_type, headers=header, params=kwargs)

  # print if the request doesn't go through
  if r.status_code != 200:  
      print("Error: " + str(r.status_code))
  else:
      r = r.json()
      try:
          # get the actual data 
          return r['results'] 
      except KeyError:
          # if the data is not nested return the whole JSON string
          return r  


if __name__ == "__main__":

  # parse all the required arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('api_token', type=str, help="Enter your NOAA database API token")
  parser.add_argument('key_id', type=str, help="Enter your AWS ACESS KEY ID")
  parser.add_argument('key', type=str, help='Enter your AWS SECRET ACCESS KEY')
  parser.add_argument('region', type=str, help = 'Enter the AWS region')
  args = parser.parse_args()

  # set the URL to the API 
  url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/'


  # Create a kinesis client
  my_stream_name = "weather-pipeline"
  kinesis_client = boto3.client('kinesis', region_name = args.region, 
                                  aws_access_key_id = args.key_id, 
                                  aws_secret_access_key = args.key)


  # get all the location information for the station in Maryland
  locations = get_noaa_station_data(url, args.api_token,
                                  datasetid='GHCND', 
                                  locationid='FIPS:24',
                                  limit=1000
                                  )


  days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
          '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
          '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'
          ]

  for day in days: 

    start_date = '2021-10-' + day + 'T00:00:00'
    end_date = '2021-10-'+ day + 'T23:59:59'

    # get the weather report
    report = get_noaa_data(url, args.api_token,
                            datasetid='GHCND', 
                            locationid='FIPS:24',
                            startdate=start_date,
                            enddate=end_date,
                            limit=1000)



    # add location information to the records
    updated_report = []
    for record in report:
      for loc in locations:
        if record['station'] == loc['id']:
          record['location'] = loc['name']
          updated_report.append(record)


    counter = 0

    for record in updated_report:

      # Send message to Kinesis DataStream
      response = kinesis_client.put_record(StreamName = my_stream_name,
                                    Data = json.dumps(record),
                                    #Data = json.dumps(ride),
                                    PartitionKey = str(hash(record['station'])))

      counter = counter + 1
      
      # If the message was not sucssfully sent print an error message
      if response['ResponseMetadata']['HTTPStatusCode'] != 200:
          print('Error!')
          print(response)

      
    print(f'Sent {counter} records for the period between {start_date} and {end_date}')

    # sleep for 5 seconds before sending the records for the next day
    time.sleep(5)
