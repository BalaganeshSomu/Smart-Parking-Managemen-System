import firebase_admin
from firebase_admin import credentials , firestore
import math
import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler

cred = credentials.Certificate("C:\\Users\\Balaganesh\\Desktop\\bookyourlot-9b5c5-firebase-adminsdk-l9emf-dff5de6925.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection = db.collection("Peelamedu - Book your Lot")

def CronJob():
    print('CronJob taking place...')
    _ = collection.document('Availability').get().to_dict()['TimeStamp']
    details = collection.document('Availability').get().to_dict()['Booked']
    if len(details) != 0:
        for i in details:
            LotDetails = collection.document(i).get().to_dict()
            LotTime = LotDetails['time']
            LotPaid = LotDetails['paid']
            LotStatus = LotDetails['EntryStatus']
            if LotStatus == False:
                timeDelta = _ - LotTime
                minutes = timeDelta.seconds / 60
                if math.ceil(minutes) > LotPaid:
                    for j in range(0,3):
                        _ = collection.document(i).update({"VehicleNumber" : ""})
                    Availability = collection.document("Availability").get().to_dict()
                    BookedNumbers = Availability['BookedNumbers']
                    AvailableNumbers = Availability['AvailableNumbers']
                    Booked = Availability['Booked']
                    Available = Availability['Available']
                    AvailableNumbers = AvailableNumbers + 1
                    BookedNumbers = BookedNumbers - 1
                    Booked.remove(i)
                    Available.append(i)
                    AvailabilityUpdate = {'BookedNumbers': BookedNumbers, 'AvailableNumbers': AvailableNumbers, 'Booked': Booked, 'Available': Available}
                    for i in range(0,5):
                        _ = collection.document("Availability").update(AvailabilityUpdate)

scheduler = BlockingScheduler()
scheduler.add_job(CronJob, 'interval',minutes = 1)
scheduler.start()
