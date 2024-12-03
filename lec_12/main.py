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
            numbers=[str(random.randint(1,100)) for _ in range(20)]
            line = " ".join(numbers)
            file.write(line+"\n")

@execution_time_decorator
def read_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        int_arrays = [list(map(int, line.split())) for line in lines]
    return int_arrays


@execution_time_decorator
def filter_num():
    array=[]
    with open("Numbers.txt","r") as file:
        for line in file:
            arr=list(map(int,line.split()))
            filtered=list(filter(lambda x:x>40,arr)) 
            array.append(filtered)
    with open("Filtered.txt", "w") as file:
        for line in array:
            file.write(" ".join(map(str, line)) + "\n")
    return array

@execution_time_decorator
def read_as_generator(file_name):
    with open(file_name,"r") as file:
        for line in file:
            yield list(map(int, line.split())) 

random_numbers()
lines = read_file("Numbers.txt")
for i in lines:
    print(i) 
    
filtered_array=filter_num()

for line in read_as_generator("Filtered.txt"):
    print(line)
