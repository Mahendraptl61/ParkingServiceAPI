from bottle import run , route,get,post,Bottle
import MySQLdb
import json
from datetime import datetime  
from datetime import timedelta  
#View Available Parking Spots On Map (To get the Parking Spots and display in terms of Json format).
USERNAME='root'
PASSWORD='xxxxx'
HOST='localhost'
DB='parking_reservation'
app=Bottle()


@get('/viewParkingSpotAvilable')
def getParkingSpotAvilable():
    SelectParkingSpot="SELECT ParkingSpotId, Address_OF_Parking_Spot,Parking_Spot_Price_Par_Hour ,Parking_Spot_Dist_In_Radious_meter,Latitude,Longitude,AVAILABILITY FROM PARKING_SPOT_MASTER_TABLE WHERE AVAILABILITY='Yes';"
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    print cur
    cur.execute(SelectParkingSpot)
    res=cur.fetchall()
    resultedList=[]
    for data in res:
          resultedList.append({"ParkingSpotId":data[0],"Address_OF_Parking_Spot":data[1],"Parking_Spot_Price_Par_Hour":data[2],"Parking_Spot_Dist_In_Radious_meter":data[3],"Latitude":data[4],"Longitude":data[5],"AVAILABILITY":data[6]})
    
    
    return json.dumps(resultedList)           
       
       
@get('/findNearByParkingSpot/<lattitude>/<longitude>/<meter>')
def findNearByParkingSpotWithinRadius(lattitude,longitude,meter):
    findParkingSpot="SELECT ParkingSpotId,Address_OF_Parking_Spot,Parking_Spot_Price_Par_Hour ,Parking_Spot_Dist_In_Radious_meter,Latitude,Longitude,AVAILABILITY FROM PARKING_SPOT_MASTER_TABLE WHERE Parking_Spot_Dist_In_Radious_meter <={0} and  AVAILABILITY='Yes' ;".format(meter)
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    cur.execute(findParkingSpot)
    res=cur.fetchall()
    resultedList=[]
    for data in res:
          resultedList.append({"ParkingSpotId":data[0],"Address_OF_Parking_Spot":data[1],"Parking_Spot_Price_Par_Hour":data[2],"Parking_Spot_Dist_In_Radious_meter":data[3],"Latitude":data[4],"Longitude":data[5],"AVAILABILITY":data[6]})
    return json.dumps(resultedList)          

@route('/reserveParkingSpot/<spotId>/<ParkingHours>',method=['GET','POST'])
def reserveParkingSpotBasedOnSpotId(spotId,ParkingHours):
    findParkingSpotBasedOnId="SELECT Address_OF_Parking_Spot,Parking_Spot_Price_Par_Hour FROM PARKING_SPOT_MASTER_TABLE WHERE ParkingSpotId={0} and  AVAILABILITY='Yes' ;".format(spotId)
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    cur.execute(findParkingSpotBasedOnId)
    res=cur.fetchone()
    if res==None:
        return "<h2 style='color:red;'>Parking Spot Is Not Available For This Parking Id "+spotId+" </h1>"
    AddressOfParking=res[0]
    ParkingSpotPriceParHour=res[1]
    ParkingHours=int(ParkingHours)
    ParkingCost=ParkingSpotPriceParHour*ParkingHours
    Reservation_Start_Time=datetime.now()  
    Reservation_End_Time=Reservation_Start_Time+timedelta(hours=ParkingHours)  
    reserveParking="UPDATE PARKING_SPOT_MASTER_TABLE SET AVAILABILITY='{0}' WHERE ParkingSpotId={1} ;".format('No',spotId)     
    ParkingStatus=''
    cur.execute(reserveParking)
    dbConnectObj.commit()
    if cur.rowcount >=1:
       ParkingStatus='SUCCESS'
    else:
       ParkingStatus="CANCELED" 
    insertParkingReservation="INSERT INTO Parking_Reservation_table(ParkingSpotId,Cost_Of_Reservation,AddressOfParkingSpot,Resevation_Duration_In_Hours,Reservation_Start_Time,Reservation_End_Time,Reservation_Status) VALUES({0},{1},'{2}',{3},'{4}','{5}','{6}');".format(spotId,ParkingCost,AddressOfParking,ParkingHours,Reservation_Start_Time,Reservation_End_Time,ParkingStatus)
    cur.execute(insertParkingReservation)
    dbConnectObj.commit()
    if cur.rowcount >=1:
             return {spotId:"Parking Reservation successful"} 
         
    else:
        return {spotId:"Parking Reservation Is Not Successful"} 
    


@route('/viewReservation/<userId>')
def viewParkingReservation(userId):
    viewParkingRervation="SELECT ParkingSpotId,Cost_Of_Reservation,AddressOfParkingSpot,Resevation_Duration_In_Hours,Reservation_Status FROM PARKING_RESERVATION_TABLE WHERE User_Id={0} and  Reservation_Status='SUCCESS';".format(userId)
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    cur.execute(viewParkingRervation)
    res=cur.fetchone()
    if res==None:
        return "<h2 style='color:red;'>Oh Sorry. Parking Reservation Is Not Available For This User Id "+userId+" And Hence It's not reserved For This User Id</h1>"
    ParkingSpotId=res[0]
    Cost_Of_Reservation=res[1]
    AddressOfParkingSpot=res[2]
    Resevation_Duration_In_Hours=res[3]
    Reservation_Status=res[4]
    return{ "Reservation Available": {"ParkingSpotId":ParkingSpotId,"Cost_Of_Reservation":Cost_Of_Reservation,"AddressOfParkingSpot":AddressOfParkingSpot,"Resevation_Duration_In_Hours":Resevation_Duration_In_Hours,"Reservation_Status":Reservation_Status}}


@route('/cancelReservation/<userId>')
def cancelExistinReservation(userId):
    viewParkingRervation="SELECT ParkingSpotId,Cost_Of_Reservation,AddressOfParkingSpot,Resevation_Duration_In_Hours,Reservation_Status FROM PARKING_RESERVATION_TABLE WHERE User_Id={0} and  Reservation_Status='SUCCESS';".format(userId)
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    cur.execute(viewParkingRervation)
    res=cur.fetchone()
    if res==None:
        return "<h2 style='color:red;'>Oh Sorry. Parking Reservation Is Not Available For This User Id "+userId+" And Hence It's not reserved</h1>"
    ParkingSpotId=res[0]
    Cost_Of_Reservation=res[1]
    AddressOfParkingSpot=res[2]
    Resevation_Duration_In_Hours=res[3]
    Reservation_Status=res[4]
    updateMasterParkingTableForNo="UPDATE PARKING_SPOT_MASTER_TABLE SET AVAILABILITY='{0}' WHERE ParkingSpotId={1} ;".format('Yes',ParkingSpotId)
    cur.execute(updateMasterParkingTableForNo)
    dbConnectObj.commit()
    if cur.rowcount>=1:
       cancelParkingTable="UPDATE PARKING_RESERVATION_TABLE SET Reservation_Status='{0}' WHERE User_Id={1} ;".format('CANCELED',userId)           
       cur.execute(cancelParkingTable)
       dbConnectObj.commit()
       viewParkingRervation="SELECT ParkingSpotId,Cost_Of_Reservation,AddressOfParkingSpot,Resevation_Duration_In_Hours,Reservation_Status FROM PARKING_RESERVATION_TABLE WHERE User_Id={0};".format(userId)             
       cur.execute(viewParkingRervation)
       res=cur.fetchone()
       ParkingSpotId=res[0]
       Cost_Of_Reservation=res[1]
       AddressOfParkingSpot=res[2]
       Resevation_Duration_In_Hours=res[3]
       Reservation_Status=res[4]
       return{ "Reservation Canceled": {"ParkingSpotId":ParkingSpotId,"Cost_Of_Reservation":Cost_Of_Reservation,"AddressOfParkingSpot":AddressOfParkingSpot,"Resevation_Duration_In_Hours":Resevation_Duration_In_Hours,"Reservation_Status":Reservation_Status}}

@route('/costOfReservation/<userId>')
def getCostOfReservation(userId):
    costOfRervation="SELECT ParkingSpotId,Cost_Of_Reservation FROM PARKING_RESERVATION_TABLE WHERE User_Id={0} and  Reservation_Status='SUCCESS';".format(userId)
    print costOfRervation
    dbConnectObj=MySQLdb.connect(HOST,USERNAME,PASSWORD,DB)
    cur=dbConnectObj.cursor()
    cur.execute(costOfRervation)
    res=cur.fetchone()
    if res==None:
        return "<h2 style='color:red;'>Oh Sorry. Parking Reservation Is Not Available For This User Id "+userId+" And Hence It's not reserved and reservation is not available for given user Id</h1>"

    ParkingSpotId=res[0]
    Cost_Of_Reservation=res[1]    
    return {"Reservation Price":Cost_Of_Reservation,"Parking-Spot-Id":ParkingSpotId}




if __name__=="__main__":
    run(debug=True,reloader=True)
   



    
