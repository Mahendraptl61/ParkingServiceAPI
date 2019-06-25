import unittest 
import requests

class ResrvationParkingTest(unittest.TestCase): 
  
    # Returns True or False.  
    def test_getParkingSpotAvilable(self):         
        url="http://127.0.0.1:8080/viewParkingSpotAvilable"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)
        
    def test_findNearByParkingSpotWithinRadius(self):         
        url="http://127.0.0.1:8080/findNearByParkingSpot/-60/75/250"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)    
    
    def test_reserveParkingSpotBasedOnSpotId(self):
        url="http://127.0.0.1:8080/reserveParkingSpot/203/2"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)    
    
    def test_viewParkingReservation(self):
        url="http://127.0.0.1:8080/viewReservation/6"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)  
        
    def test_cancelExistinReservation(self):
        url="http://127.0.0.1:8080/cancelReservation/6"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)     
     
    def test_getCostOfReservation(self):
        url="http://127.0.0.1:8080/costOfReservation/6"
        res=requests.get(url)
        status=res.status_code
        print status
        self.assertEqual(200,status)      



if __name__ == '__main__': 
    unittest.main()  

