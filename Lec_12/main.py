import random
import time

def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        ex_time = end_time - start_time  
        print(f"Execution time of {func.__name__}:{ex_time} seconds.")
        return result  
    return wrapper

@execution_time_decorator
def random_numbers():
    with open("Numbers.txt","w") as file:
        for _ in range(100):
            numbers=[str(random.randint(1,100)) for _ in range(21)]
            line = " ".join(numbers)
            file.write(line+"\n")


@execution_time_decorator
def filter_num():
    array=[]
    with open("Numbers.txt","r") as file:
        lines=file.readlines()
        for i in lines:
            arr=list(map(int,i.split()))
            filtered=list(filter(lambda x:x>40,arr)) 
            array.append(filtered)
    with open("Filtered.txt", "w") as file:
        for i in array:
            file.write(" ".join(map(str, i)) + "\n")
    return array

@execution_time_decorator
def read_as_generator(file_name):
    with open(file_name,"r") as file:
        for i in file:
            yield list(map(int, i.split())) 

random_numbers()
filtered_array=filter_num()

for line in read_as_generator("Filtered.txt"):
    print(line)
