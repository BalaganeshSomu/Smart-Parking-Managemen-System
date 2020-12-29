import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials , firestore
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
servo_pin = 21 
45
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT) # Declaring GPIO 21 as output pin
p = GPIO.PWM(servo_pin, 50) # Created PWM channel at 50Hz frequency
while True:
 if GPIO.input(23)==GPIO.HIGH:
 def Vnumber():
 cam.resolution=(640,480)
 cam.framerate=30
 img = PiRGBArray(cam, size=(640, 480))
 img=np.array(img)
 img = cv2.resize(img, (800,500) )
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 gray = cv2.bilateralFilter(gray, 13, 15, 15)
 edged = cv2.Canny(gray, 30, 200)
 contours = cv2.findContours(edged.copy(), cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)
 contours = imutils.grab_contours(contours)
 contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
 screenCnt = None
 for c in contours:
 peri = cv2.arcLength(c, True)
 approx = cv2.approxPolyDP(c, 0.018 * peri, True)
 if len(approx) == 4:
 screenCnt = approx
 break
 if screenCnt is None:
 detected = 0
 print ("No contour detected")
 else:
 detected = 1
46
 if detected == 1:
 cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
 mask = np.zeros(gray.shape,np.uint8)
 new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
 new_image = cv2.bitwise_and(img,img,mask=mask)
 (x, y) = np.where(mask == 255)
 (topx, topy) = (np.min(x), np.min(y))
 (bottomx, bottomy) = (np.max(x), np.max(y))
 Cropped = gray[topx:bottomx+1, topy:bottomy+1]
 text= pytesseract.image_to_string(Cropped, config='--psm 11')
 return text
 obtained_number=Vnumber()
 def RemoveUnwanted(vehicle_number):
 alphanumeric_filter = filter(str.isalnum,vehicle_number)
 alphanumeric_string = "".join(alphanumeric_filter)
 return alphanumeric_string
 obtained_number=RemoveUnwanted(obtained_number)
 cred = credentials.Certificate("/home/pi/Desktop/bookyourlot-9b5c5-firebaseadminsdk-l9emf-dff5de6925.json")
 firebase_admin.initialize_app(cred)
 db = firestore.client()
 collection = db.collection("Peelamedu - Book your Lot")
 def GetDetails():
 details = dict()
 for i in collection.document('Availability').get().to_dict()['Booked']:
 details[i] = collection.document(i).get().to_dict()
 return details
 def CheckIfBooked(vehicle_number , details):
 location = []
 for i in details:
 if details[i]['VehicleNumber'] == vehicle_number:
47
 location.append(i)
 if len(location) == 0:
 if (collection.document('Availability').get().to_dict()['AvailableNumbers'] ==
0):
 String = 'Sorry! No Room'
 return(String) #TODO : DISPLAY IN LCD
 else:
 paid = 0
 Availability = collection.document('Availability').get().to_dict()
 BookedNumbers = Availability['BookedNumbers']
 AvailableNumbers = Availability['AvailableNumbers']
 Booked = Availability['Booked']
 Available = Availability['Available']
 Alloted = Available.pop()
 AvailableNumbers = AvailableNumbers - 1
 BookedNumbers = BookedNumbers + 1
 Booked.append(Alloted)
 AvailabilityUpdate = {'BookedNumbers': BookedNumbers,
'AvailableNumbers': AvailableNumbers, 'Booked': Booked, 'Available': Available}
 for i in range(0,5):
 _ = collection.document('Availability').update(AvailabilityUpdate)
 LotUpdate = {'EntryStatus' : True , 'VehicleNumber' : vehicle_number ,
'paid' : paid , 'time' : firestore.SERVER_TIMESTAMP}
 for i in range(0,5):
 _ = collection.document(Alloted).update(LotUpdate)
 String = "Your lot is "+str(Alloted)
 return(String) #TODO : DISPLAY IN LCD
 else:
 LotNumber = location[0] #ONLINE
 collection.document(LotNumber).update({'EntryStatus' : True })
 String = "Your lot is "+str(LotNumber)
48
 return(String)
 # Define GPIO to LCD mapping
 LCD_RS = 26
 LCD_E = 19
 LCD_D4 = 13
 LCD_D5 = 6
 LCD_D6 = 5
 LCD_D7 = 11
 LED_ON = 15
 # Define some device constants
 LCD_WIDTH = 16 # Maximum characters per line
 LCD_CHR = True
 LCD_CMD = False
 LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
 LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 # Timing constants
 E_PULSE = 0.00005
 E_DELAY = 0.00005
 def main():
 # Main program block
 # Initialise display
 lcd_init()
 # Toggle backlight on-off-on
 GPIO.output(LED_ON, True)
 time.sleep(1)
 GPIO.output(LED_ON, False)
 time.sleep(1)
 GPIO.output(LED_ON, True)
 time.sleep(1)
49
 # Send some centred test
 details = GetDetails()
 vehicle_number = obtained_number
 StringOutput = CheckIfBooked(vehicle_number , details)
 lcd_byte(LCD_LINE_1, LCD_CMD)
 lcd_string(StringOutput,1)
 time.sleep(3) # 3 second delay
 time.sleep(30)
 # Turn off backlight
 GPIO.output(LED_ON, False)
 def lcd_init():
 GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
 GPIO.setup(LCD_E, GPIO.OUT) # E
 GPIO.setup(LCD_RS, GPIO.OUT) # RS
 GPIO.setup(LCD_D4, GPIO.OUT) # DB4
 GPIO.setup(LCD_D5, GPIO.OUT) # DB5
 GPIO.setup(LCD_D6, GPIO.OUT) # DB6
 GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
 # Initialise display
 lcd_byte(0x33,LCD_CMD)
 lcd_byte(0x32,LCD_CMD)
 lcd_byte(0x28,LCD_CMD)
 lcd_byte(0x0C,LCD_CMD)
 lcd_byte(0x06,LCD_CMD)
 lcd_byte(0x01,LCD_CMD)
 def lcd_string(message,style):
 if style==1:
 message = message.ljust(LCD_WIDTH," ") 
50
 elif style==2:
 message = message.center(LCD_WIDTH," ")
 elif style==3:
 message = message.rjust(LCD_WIDTH," ")
 for i in range(LCD_WIDTH):
 lcd_byte(ord(message[i]),LCD_CHR)
 def lcd_byte(bits, mode):
 GPIO.output(LCD_RS, mode) # RS
 # High bits
 GPIO.output(LCD_D4, False)
 GPIO.output(LCD_D5, False)
 GPIO.output(LCD_D6, False)
 GPIO.output(LCD_D7, False)
 if bits&0x10==0x10:
 GPIO.output(LCD_D4, True)
 if bits&0x20==0x20:
 GPIO.output(LCD_D5, True)
 if bits&0x40==0x40:
 GPIO.output(LCD_D6, True)
 if bits&0x80==0x80:
 GPIO.output(LCD_D7, True)
 # Toggle 'Enable' pin
 time.sleep(E_DELAY)
 GPIO.output(LCD_E, True)
 time.sleep(E_PULSE)
 GPIO.output(LCD_E, False)
 time.sleep(E_DELAY)
 # Low bits
 GPIO.output(LCD_D4, False)
 GPIO.output(LCD_D5, False)
51
 GPIO.output(LCD_D6, False)
 GPIO.output(LCD_D7, False)
 if bits&0x01==0x01:
 GPIO.output(LCD_D4, True)
 if bits&0x02==0x02:
 GPIO.output(LCD_D5, True)
 if bits&0x04==0x04:
 GPIO.output(LCD_D6, True)
 if bits&0x08==0x08:
 GPIO.output(LCD_D7, True)
 # Toggle 'Enable' pin
 time.sleep(E_DELAY)
 GPIO.output(LCD_E, True)
 time.sleep(E_PULSE)
 GPIO.output(LCD_E, False)
 time.sleep(E_DELAY)
 if __name__ == '__main__':
 main()
 p.start(2.5)
 try:
 p.ChangeDutyCycle(2.5) # Move servo to 0 degrees
 sleep(5) # Delay of 1 sec
 p.ChangeDutyCycle(7.5)
 sleep(5)
 p.ChangeDutyCycle(2.5)
 except KeyboardInterrupt:
 pass
 GPIO.cleanup()
 if GPIO.input(14)==GPIO.HIGH:
 def Vnumber():
52
 cam.resolution=(640,480)
 cam.framerate=30
 img1 = PiRGBArray(cam, size=(640, 480))
 img1=np.array(img)
 img1 = cv2.resize(img, (800,500) )
 gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 gray1 = cv2.bilateralFilter(gray, 13, 15, 15)
 edged1 = cv2.Canny(gray1, 30, 200)
 contours1 = cv2.findContours(edged1.copy(), cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)
 contours1 = imutils.grab_contours1(contours1)
 contours1 = sorted(contours1, key = cv2.contourArea, reverse = True)[:10]
 screenCnt1 = None
 for c in contours1:
 peri1 = cv2.arcLength(c, True)
 approx1 = cv2.approxPolyDP(c, 0.018 * peri1, True)
 if len(approx) == 4:
 screenCnt = approx
 break
 if screenCnt1 is None:
 detected1 = 0
 print ("No contour detected")
 else:
 detected1 = 1
 if detected1 == 1:
 cv2.drawContours(img1, [screenCnt], -1, (0, 0, 255), 3)
 mask1 = np.zeros(gray.shape,np.uint8)
 new_image1 = cv2.drawContours1(mask1,[screenCnt],0,255,-1,)
 new_image1 = cv2.bitwise_and(img1,img1,mask1=mask1)
 (x, y) = np.where(mask == 255)
 (topx, topy) = (np.min(x), np.min(y))
53
 (bottomx, bottomy) = (np.max(x), np.max(y))
 Cropped1 = gray[topx:bottomx+1, topy:bottomy+1]
 text1= pytesseract.image_to_string(Cropped1, config='--psm 11',nice=1)
 return text1
 obtained_number1=Vnumber()
 def RemoveUnwanted(vehicle_number):
 alphanumeric_filter = filter(str.isalnum,vehicle_number)
 alphanumeric_string = "".join(alphanumeric_filter)
 return alphanumeric_string
 obtained_number=RemoveUnwanted(obtained_number)
 cred = credentials.Certificate("/home/pi/Desktop/bookyourlot-9b5c5-firebaseadminsdk-l9emf-dff5de6925.json")
 firebase_admin.initialize_app(cred)
 db = firestore.client()
 collection = db.collection("Peelamedu - Book your Lot")
 def GetDetails():
 details = dict()
 for i in collection.document('Availability').get().to_dict()['Booked']:
 details[i] = collection.document(i).get().to_dict()
 return details
 def GetLotNumber(vehicle_number , details):
 location = []
 for i in details:
 if details[i]['VehicleNumber'] == vehicle_number:
 location.append(i)
 if len(location) == 0:
 return('Sorry!')
 else:
 LotNumber = location[0]
 for i in range(0,5):
54
 _ = collection.document(LotNumber).update({'endtime' :
firestore.SERVER_TIMESTAMP })
 _ = collection.document(LotNumber).get().to_dict()
 amnt_paid = _['paid']
 start_time = _['time']
 end_time = _['endtime']
 timedelta = end_time - start_time
 minutes = timedelta.seconds / 60
 minutes = math.ceil(minutes) #ASSUMING 50p / MIN
 amount = minutes * 0.5
 for i in range(0,5):
 _ = collection.document(LotNumber).update({"VehicleNumber" : ""})
 Availability = collection.document("Availability").get().to_dict()
 BookedNumbers = Availability['BookedNumbers']
 AvailableNumbers = Availability['AvailableNumbers']
 Booked = Availability['Booked']
 Available = Availability['Available']
 AvailableNumbers = AvailableNumbers + 1
 BookedNumbers = BookedNumbers - 1
 Booked.remove(LotNumber)
 Available.append(LotNumber)
 AvailabilityUpdate = {'BookedNumbers': BookedNumbers,
'AvailableNumbers': AvailableNumbers, 'Booked': Booked, 'Available': Available}
 for i in range(0,5):
 _ = collection.document("Availability").update(AvailabilityUpdate)
 if amount - amnt_paid <= 0:
 return("Thank You!") #OPEN AUTOMATICALLY
 else:
 return("Please Pay:"+ str(amount-amnt_paid)) #GATE OPEN ON
BUTTON
55
 # Define GPIO to LCD mapping
 LCD_RS = 26
 LCD_E = 19
 LCD_D4 = 20
 LCD_D5 = 16
 LCD_D6 = 12
 LCD_D7 = 1
 LED_ON = 15
 # Define some device constants
 LCD_WIDTH = 16 # Maximum characters per line
 LCD_CHR = True
 LCD_CMD = False
 LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
 LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 # Timing constants
 E_PULSE = 0.00005
 E_DELAY = 0.00005
 def ExitLCD():
 # Main program block
 # Initialise display
 lcd_init()
 # Toggle backlight on-off-on
 GPIO.output(LED_ON, True)
 time.sleep(1)
 GPIO.output(LED_ON, False)
 time.sleep(1)
 GPIO.output(LED_ON, True)
 time.sleep(1)
 # Send some centred test
 details = GetDetails()
56
 vehicle_number = obtained_number
 StringOutput = GetLotNumber(vehicle_number , details)
 lcd_byte(LCD_LINE_1, LCD_CMD)
 lcd_string(StringOutput,1)
 time.sleep(3) # 3 second delay
 GPIO.output(LED_ON, False)
 def lcd_init():
 GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
 GPIO.setup(LCD_E, GPIO.OUT) # E
 GPIO.setup(LCD_RS, GPIO.OUT) # RS
 GPIO.setup(LCD_D4, GPIO.OUT) # DB4
 GPIO.setup(LCD_D5, GPIO.OUT) # DB5
 GPIO.setup(LCD_D6, GPIO.OUT) # DB6
 GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
 # Initialise display
 lcd_byte(0x33,LCD_CMD)
 lcd_byte(0x32,LCD_CMD)
 lcd_byte(0x28,LCD_CMD)
 lcd_byte(0x0C,LCD_CMD)
 lcd_byte(0x06,LCD_CMD)
 lcd_byte(0x01,LCD_CMD)
 def lcd_string(message,style):
 if style==1:
 message = message.ljust(LCD_WIDTH," ")
 elif style==2:
 message = message.center(LCD_WIDTH," ")
 elif style==3:
 message = message.rjust(LCD_WIDTH," ")
 for i in range(LCD_WIDTH):
57
 lcd_byte(ord(message[i]),LCD_CHR)
 def lcd_byte(bits, mode):
 GPIO.output(LCD_RS, mode) # RS
 # High bits
 GPIO.output(LCD_D4, False)
 GPIO.output(LCD_D5, False)
 GPIO.output(LCD_D6, False)
 GPIO.output(LCD_D7, False)
 if bits&0x10==0x10:
 GPIO.output(LCD_D4, True)
 if bits&0x20==0x20:
 GPIO.output(LCD_D5, True)
 if bits&0x40==0x40:
 GPIO.output(LCD_D6, True)
 if bits&0x80==0x80:
 GPIO.output(LCD_D7, True)
 # Toggle 'Enable' pin
 time.sleep(E_DELAY)
 GPIO.output(LCD_E, True)
 time.sleep(E_PULSE)
 GPIO.output(LCD_E, False)
 time.sleep(E_DELAY)
 # Low bits
 GPIO.output(LCD_D4, False)
 GPIO.output(LCD_D5, False)
 GPIO.output(LCD_D6, False)
 GPIO.output(LCD_D7, False)
 if bits&0x01==0x01:
 GPIO.output(LCD_D4, True)
 if bits&0x02==0x02:
58
 GPIO.output(LCD_D5, True)
 if bits&0x04==0x04:
 GPIO.output(LCD_D6, True)
 if bits&0x08==0x08:
 GPIO.output(LCD_D7, True)
 # Toggle 'Enable' pin
 time.sleep(E_DELAY)
 GPIO.output(LCD_E, True)
 time.sleep(E_PULSE)
 GPIO.output(LCD_E, False)
 time.sleep(E_DELAY)
 ExitLCD()
