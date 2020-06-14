from record import Record
from user import User
from RecordManager import RecordManager
from UserManager import UserManager


record_1 = Record (
    id_number = '12345673',
    location = 'National Taiwan University of Science and Technology',
    body_temperature = 36.7
)

recordManager = RecordManager()
#recordManager.save(record_1)

record = recordManager.readAll()
print(record.to_json())



user_1 = User(
    id_number = '222222',
    first_name = "Jeremy",
    last_name = "Toulanlan",
    phone_number = "12341234",
    email = "JeremyToulanlan@gmail.com"
)

#userManager = UserManager()
#userManager.save(user_1)

#user = userManager.readAll()
#print(user.to_json())