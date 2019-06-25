Parking Reservation Rest API Services
--------------------------------------

1. Required DB , python packages and installation required for the package
-----------------------------------------------------------------------------

1. DataBase : MySQL DB 

2. Python Package : 

   i.bottle package for to develop Rest API Methods in Python 
   
   ii.faker package for to get the random and dummy data for DB

   iii. json package to convert the Python Objects into Json format

   iv. MySQLdb package to connect to mysql DB and to perform CURD operation with Reservation_ Parking system DB

   v. datetime package to calulcate date and time for adding
  
   vi unittest package to write the Unit Test case for every Rest API Service Method



3. Installing Bottle Framework
--------------------------------
pip install bottle

It will install the bottle package



4. Installing faker module
------------------------------

pip install faker 

It will install the faker package



5. Create Database in MySQL for Parking Reservation
-----------------------------------------------------

CREATE DATABSE PARKING_RESERVATION ;



6. CREATE BELOW TABLES 
--------------------------



I Parking_Spot_Master_Table
--------------------------

CREATE TABLE PARKING_SPOT_MASTER_TABLE
(ParkingSpotId int NOT NULL AUTO_INCREMENT , 
Address_OF_Parking_Spot VARCHAR(250) NOT NULL,
Parking_Spot_Price_Par_Hour FLOAT(10) NOT NULL,
Parking_Spot_Dist_In_Radious_meter FLOAT(10) NOT NULL,
Latitude FLOAT NOT NULL,
Longitude FLOAT NOT NULL,
PRIMARY KEY(ParkingSpotId)
);



II Parking_Reservation_table 
--------------------------------

CREATE TABLE PARKING_RESERVATION_TABLE(
ParkingSpotId int , 
User_Id INT NOT NULL AUTO_INCREMENT ,
Cost_Of_Reservation float NOT NULL,
AddressOfParkingSpot varchar(250) NOT NULL,
Resevation_Duration_In_Hours float NOT NULL,
Reservation_Start_Time varchar(100) NOT NULL,
Reservation_End_Time varchar(100) NOT NULL,
Reservation_Status varchar(50) NOT NULL,
FOREIGN KEY (ParkingSpotId) REFERENCES Parking_Spot_Master_Table(ParkingSpotId),
PRIMARY KEY(User_Id)
);




7. Populate the  fake and dummy data to master table with PopulateFakeReservationDataToDB.py
--------------------------------------------------------------------------------------------

I. Inside into this script we have populate method with n as argument , Provide how many dummy
records you want to insert into Master table

If you provide 30 or 300 , it will genearate 300 unique records into the table and hence we can setup 
our master table in few seconds




Demonstration With Rest API Services with the ParkingServiceRestApi.py. :-
-------------------------------------------------------------------------

Run the script

python ParkingServiceRestApi.py 

You will get the below output

Bottle v0.12.16 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.








1. See available parking spots on a map 
-----------------------------------------
http://127.0.0.1:8080/viewParkingSpotAvilable

You will get all the available Parking Spots which are avilable in Parking Master Table and it will return JSON with all the data

The above API will hit to the below method

def getParkingSpotAvilable()




2.Search for an address and find nearby parking spot. (input: lat, lng, radius in meters.    
   Output - list of parking spots within the radius). 
-----------------------------------------------------------


http://127.0.0.1:8080/findNearByParkingSpot/<lattitude>/<longitude>/<meter>

Here you will get all the nearest parking spot based on the input provided in the url as distance in meter

and the above API will hit to the below method

def findNearByParkingSpotWithinRadius(lattitude,longitude,meter)





3.Reserve a parking spot 
----------------------------

http://127.0.0.1:8080/reserveParkingSpot/<spotId>/<ParkingHours>



The above REST API will make entry into PARKING_RESERVATION_TABLE and and it will update the PARKING_SPOT_MASTER_TABLE
based on the Spot Id and Parking Hours provided in the URL


If SpotId Is not Available then it will return HTML response by saying 
Spot id is not available


4.View existing Reservations 
-------------------------------
http://127.0.0.1:8080/viewReservation/<userId>

It will return the JSON Response with Parking Reservation Details based on the userId Provided in the URL

If UserId Is not Available then it will return HTML response by saying 
 UserId is not available


5.Cancel an existing reservation 
----------------------------------

http://127.0.0.1:8080/cancelReservation/<userId>

It will cancel the reservation and the based on the UserId , It will make the Parking_Status to CANCELED
in PARKING_RESERVATION_TABLE and it will update the AVAILABILITY column for to Yes based on the Spot Id in PARKING_SPOT_MASTER_TABLE


6.Show the user the cost of the reservation 
--------------------------------------------
http://127.0.0.1:8080/costOfReservation/<userId>

It will return the JSON response with Price Of The Reservation from PARKING_RESERVATION_TABLE 



7. Unit Testing with unittest package in Python
--------------------------------------------------


In this unit testing will do the API Service method level assertion based on the return code of REST API

here one commone test case will do the assertion with 200 and return status code from Rest API , if both
the values are same then Test case will going to execute

Example :-

def test_getCostOfReservation(self):
        url="http://127.0.0.1:8080/costOfReservation/6"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)    
        here status and 200 are both equlas then Test case will going to execute and it will return OK for test cases executed
