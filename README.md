# Open Weather Integration

This project design and build a service that collects data from an Open Weather API and store it as
a JSON data.

## Specifications

- All the logic is built using Python 3;
- The application must do async calls to Open Weather API to get weather information from the cities indexed by the file 'cities.csv';
- The application must respect Open Weather free account limit, exactly 60 requests per minute (or 1 per sec);
- An account at Open Weather API it's necessary, each account has a code that must be send to the API;
- Code needs to have more than 90% of test coverage;
- Open git repository (preferable in github);
- Docker must be used to set up the environment, so a Dockerfile must exists in the project.

## Endpoints

### POST

Receives a user defined ID, collect weather data from Open Weather API and store:

- The user defined ID (needs to be unique for each request)
- Datetime of request
- JSON data with:
- City ID
- Temperature in Celsius
- Humidity

### GET

Receives the user defined ID, returns with the percentage of the POST progress ID (collected cities completed) until the current moment.

## Usage

The system works this way:

1. The user enter in the system and receives a unique ID;
2. The user request data, this could be a button or any other way to trigger an action;
3. The system records the user ID and the request datetime;
4. Then the system starts to request the following data for each city in 'cities.csv': city id, temperature and humidity;
5. The Open Weather API free account only accepts one request by second, so get data from 60 cities the time is going to be 1 minute, during this time the API must retrieve the user can be updated about the progress of the requests, something like a loading bar;
6. After finishing the requests to Open Weather it is possible to show the data to the user.

## My idea

My idea is to develop a frontend de-attached from the backend. The backend is going to implement the API and the communication with Open Weather. The frontend is going to send the requests and show the data to the user in a friendly way.

### Backend

All the backend implementation were done using Django Rest Framework. This is a complete framework that provides features to create endpoints, communicate with persistency in a simple way and testing the entire application.

The persistency are going to be done using MySQL, because it's a simple to use and robust enough to handle this use case. See more benefits in this [link](https://www.oracle.com/mysql/what-is-mysql/#mysql-benefits).

The following components are going to be part of the solution:

#### OpenWeatherAdapter

A class to communicate with Open Weather API, separating the project API logic from Open Weather API logic, the class should implement the following methods:

##### get_city(city_id)

A method to request data from a specific city.

#### RequestQueue

This class control how many requests are being done to Open Weather API, respecting the limit of time of each request. The requests can be inserted in a queue and then executed async in batches of 60 requests, using the class OpenWeatherAdapter to perform them, respecting the limit of 60 seconds between each batch. Only one instance of the object must be created, to grant full control of the requests being done. This class implements the following methods:

##### add_cities(list)

Add in the queue all the cities that have to be requested to Open Weather

##### request()

Once the queue is filled with the cities, this method can be called to execute the request loop. For each city in the queue the data is going to be requested, in batches of 60, async, between each batch the limit time is going to be waited. The requests are going do be done using the OpenWeatherAdapter, and the returned data is going to be stored in a result attribute of the class. Once a request to a city ID is done this ID can be removed from the queue, once the queue is empty the request loop finishes and the function can return. This function needs to be called async.

#### len()

Return the total number of city ID's in the list.

##### status()

Returns the total number of already requested city ID's.

#### clear()

Remove all t


#### UserQueue

Several users can access the system at the same time, but unfortunately Open Weather Free account have a limit of requests per minute (60 requests per minute) so the system have to put the users in a queue named UserQueue. This class is responsible to put the users in the Queue, trigger the method that perform the requests to the first user in the queue and once all requests is done, remove the user from the queue. This class have to implement the following methods:

##### add_user(user)

Add an user in the end of the queue and returns the position of the user in the list, 1-indexed (same than the length of the queue).

##### execute_first()

Add all the cities provided in the 'cites.csv' in the RequestQueue

##### get_user_status(user)

Receive an user

### Frontend

An web interface built using React, because react can easily update data in the screen using virtual DOM and this is exactly the behavior we are searching for. This is user journey on the frontend:

1. Once the user access the page the frontend loads and show him/her a button;
2. Once the user click in this button the frontend is going to generate an UID and send the POST request to the backend, if the UID already exists the backend is going to reply 400 BAD REQUEST, this way the frontend can generate another UID;
3. Once the UID was generated were generated and a 200 SUCCESS was replied by the backend the frontend knows that the the UID is now registered and the requests to Open Weather are going to be queued;
4. The frontend shows a loading bar and starts sending GET requests to the backend to update the loading bar status;
5. Once all the requests are finished the frontend can show the data from each city requested to Open Weather.
6. Observation: if the page was re-loaded on closed the UID will be lost by the frontend, the button is going to be displayed to start the requests again.


Why celery?

Why Redis?
https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#redis