import random
from app import query
def create_request_number():
    try:
        starter_number= '#'
        request_number_list = set()
        for i in range(10):
            number = random.randrange(1,10)
            starter_number+=str(number)
        request_number_list.add(starter_number)          
        return request_number_list
    except:
        if request_number_list == query(f"SELECT request_number FROM requests WHERE request_number='{request_number_list}'"):
            random.shuffle(request_number_list)
        return request_number_list


print(create_request_number())