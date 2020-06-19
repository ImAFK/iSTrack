from models.record import Record
from models.user import User
from models.RecordManager import RecordManager
from models.UserManager import UserManager


record_1 = Record (
    id_number = '12345673',
    location = 'National Taiwan University of Science and Technology',
    body_temperature = 36.7
)

# recordManager = RecordManager()
#recordManager.save(record_1)

# record = recordManager.readAll()
# print(record.to_json())



user_1 = User(
    id_number = '222222',
    first_name = "Jeremy",
    last_name = "Toulanlan",
    phone_number = "12341234",
    email = "JeremyToulanlan@gmail.com"
)

userManager = UserManager()
user = User(id_number='f6e314a3',
            first_name='Test',
            last_name='RFID',
            phone_number='0912745623',
            email='test.me@rfid.com')
userManager.save(user)
userManager.disconnect()

#user = userManager.readAll()
#print(user.to_json())