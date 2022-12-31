# Weather Data Collection and Consumption Using Amazon Kinesis

### Abstract
The project aims to collect and analyze weather data using Amazon's Kinesis data streaming service. The collected data can be used to provide insights into weather patterns and trends, with the goal of helping users make informed decisions based on real-time weather information. It will also store the necessary information such as precipitation, snowfall and temperature in our case in a DynamoDB database for future reference.

### Introduction
The project involves using an Amazon Elastic Compute Cloud (EC2) instance to collect weather data from the National Oceanic and Atmospheric Administration (NOAA) using its API. The EC2 instance acts as a Kinesis Producer, feeding the collected data into a Kinesis Data Stream. The specific data being requested from the NOAA API is daily weather information for the state of Maryland from all available stations for the month October of the year 2021. The EC2 instance will make the necessary API calls to obtain this data, which will then be streamed into the Kinesis Data Stream for further analysis and consumption.

Another EC2 instance, acting as a Kinesis Consumer, will read through the records in the data stream and filter out only the relevant information, such as temperature, precipitation, and snowfall. This filtered data will then be stored in separate DynamoDB databases for temperature and precipitation data. In this way, the project aims to provide a scalable and efficient solution for collecting, analyzing, and storing weather data from the NOAA.

### Design

##### Components

###### NOAA API
The National Oceanic and Atmospheric Administration (NOAA) is a scientific agency within the United States Department of Commerce that focuses on the conditions of the oceans and the atmosphere. The NOAA provides a variety of public data and information through its website and API (Application Programming Interface). The NOAA API allows developers to access and integrate the data and functionality of the NOAA with other applications and services. With the API, users can access a range of data, including weather forecasts, current conditions, and climate data. This data can be used for a variety of purposes, such as weather forecasting, climate research, and emergency management. The NOAA API is a valuable resource for individuals and organizations looking to access and use high-quality weather and climate data.

###### Kinesis
Amazon Kinesis is a fully managed, cloud-based service that makes it easy to collect, process, and analyze real-time, streaming data at massive scale. It provides the ability to build custom applications that can process and analyze streaming data, allowing organizations to gain real-time insights and respond to new information as it becomes available. Kinesis is designed to handle large amounts of data and can automatically scale to match the volume and throughput of the data being processed. It also provides the ability to replay data streams, making it easy to backtrack and process data that may have been missed or processed incorrectly.

###### Kinesis Producer
A Kinesis Producer is a client application that puts data records into an Amazon Kinesis stream. The producer is responsible for packaging the data into records and sending them to the Kinesis stream, where they can be processed and analyzed by other applications. The producer can be any type of application, such as a mobile app, a web server, or an EC2 instance (as in our case). The Kinesis stream acts as a buffer, temporarily storing the data records until they can be consumed by one or more Kinesis Consumers. This allows for decoupling of data production and consumption, enabling real-time processing and analysis of the data.

###### Kinesis Consumer
A Kinesis Consumer is a client application that reads data records from an Amazon Kinesis stream. The consumer is responsible for consuming the data records in the stream and processing them in some way, such as storing the data in a database – matches our case –, analyzing the data, or triggering other actions based on the data. The consumer can be any type of application, such as a data analysis tool, a real-time monitoring system, an EC2 instance or a machine learning model.

###### DynamoDB
Amazon DynamoDB is a fully managed, NoSQL database service offered by Amazon Web Services (AWS). It provides fast and predictable performance with the ability to scale up or down as needed, making it suitable for a wide range of applications. DynamoDB is a key-value store, which means that it stores data in the form of attribute-value pairs, similar to a dictionary. It also supports data structures such as lists and maps, allowing for more complex data models. DynamoDB is designed to be highly available and durable, with automatic data replication across multiple availability zones to protect against data loss. It also provides flexible querying capabilities, allowing users to easily retrieve data using simple queries or more complex, nested queries. 

### Flow Chart
![flow_chart_of_the_architecture](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_flow_chart.png)

### Method

##### steps
1. Create EC2 instances for Kinesis producer and consumer
![img1](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img1.png)

2. Copy the required scripts from the local machine to the EC2 instances
![img2](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img2.png)

3. Install all the required python modules
![img3](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img3.png)

4. Create Kinesis Data Stream Pipeline 
![img4](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img6.png)
![img5](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img7.png)

5. Create two dynamoDB databases
![img6](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img8.png)

6. Run the producer python script to send data to the pipeline
![img7](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img9.png)

7. Run the consumer python script to consume and to store the data in database
![img8](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img10.png)
![img9](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img11.png)
![img10](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img12.png)

### Results

Records in Kinesis Data Stream
![img11](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img13.png)

An example record in Kinesis Data Stream
![img12](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img14.png)

Write Usage In dynamoDB given by CloudWatch
![img13](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img15.png)

Sample Records in _Precipitation_ Database 
![img14](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img16.png)

Sample Records in _Temperature_ Database
![img15](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img17.png)

Sample Record in Database
![img16](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img18.png)

Total number of Records in Precipitation Database
![img17](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img19.png)

Total Records in Temperature Database
![img18](https://github.com/saiganeshT/cloud-projects/blob/main/weather_data_processing_using_AWS_kinesis/images/cloud1_img20.png)

