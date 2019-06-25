from faker import Faker
import MySQLdb 

USERNAME='root'
PASSWORD='M1234@patil'
HOST='localhost'
DB='parking_reservation'

def populateData(n):
 dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)   
 for i in xrange(n):
  fakeData=Faker('en_US')
  AddressOfParkingSpot=fakeData.address().replace("\n","-").replace(",","-").replace(" ","-")
  print AddressOfParkingSpot
  Parking_Spot_Price_Par_Hour=fakeData.random_element(elements=(65,35,110,120,75,25,67,95,85,78,105,55,50,78))
  print Parking_Spot_Price_Par_Hour
  Parking_Spot_Dist_In_Radious_meter=fakeData.random_element(elements=((210,205,105,250,500,550,80,25,90,170,195,125,35,89,20,30)))
  print Parking_Spot_Dist_In_Radious_meter
  Latitude=int(Faker().latitude())
  print Latitude
  Longitude=int(Faker().longitude())
  print Longitude
  Availability=fakeData.random_element(elements=('Yes','No'))
  print Availability
  DummyInsert="INSERT INTO PARKING_SPOT_MASTER_TABLE (Address_OF_Parking_Spot,Parking_Spot_Price_Par_Hour,Parking_Spot_Dist_In_Radious_meter,Latitude,Longitude,AVAILABILITY) VALUES(%s,%s,%s,%s,%s,%s);"  
  input=(AddressOfParkingSpot,Parking_Spot_Price_Par_Hour,Parking_Spot_Dist_In_Radious_meter,Latitude,Longitude,Availability)
  print "Insert Query",(DummyInsert,input)
  cur=dbConnectObj.cursor()
  print cur.execute(DummyInsert,input) 
  dbConnectObj.commit()
  
populateData(100)
