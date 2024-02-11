from typing import Callable
import sys
from collections import defaultdict
import re
from functools import reduce
 

#Задача перша
def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]
        
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
        
    return fibonacci

fib = caching_fibonacci()

print(fib(10))
print(fib(15))


#Задача друга
def generator_numbers(text: str):
    numbers = map(float, filter(lambda x: re.match(r"\d+[\.,]{0,1}\d+.",x),text.split(" ")))
    for number in numbers:
        yield number

def sum_profit(text: str, func: Callable):
    return reduce(lambda x,y:x+y ,func(text))

if __name__=="__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


#Задача третя
def parse_log_line(line: str) -> dict:
    if not re.match(r'(\d{4}(?:-\d{2}){2} \d{2}(?::\d{2}){2}) (\w+) (.*)',line):
        return None
    date,time,level,*message = line.split(' ')
    return {'date':date,'time':time,'level':level,"message":' '.join(message)}

def load_logs(file_path: str) -> list:
    with open(file_path,"r+") as logfile:
        lines=list(filter(lambda x: x is not None,(map(parse_log_line,logfile.readlines()))))
    return lines

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda x: x['level']==level,logs))

def count_logs_by_level(logs: list) -> dict:
    cntr=defaultdict()
    cntr.default_factory=int  
    for log in logs:
        cntr[log['level']]+=1
    return dict(cntr)

def display_log_counts(counts: dict):
    print(f"{'Рівень логування ':20}| Кількість ")
    print(f"{'-'*20}|{'-'*10}")
    print("\n".join(list(map(lambda x:f"{x:20}| {counts[x]}",counts))))
    

if __name__=="__main__":
    filename=sys.argv[1] 
    logs=load_logs(file_path=filename)
    display_log_counts(count_logs_by_level(logs))
    if len(sys.argv)==3:
        level=sys.argv[2]
        logs=filter_logs_by_level(logs,level)
        print()
        print(f"Деталі логів для рівня '{level}':")
        print(''.join(map(lambda x:f"{x['date']} {x['time']} - {x['message']}",logs)))


#Задача четверта
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added"

@input_error
def change_contact(args, contacts):
    if args[0] in contacts.keys():
        add_contact(args, contacts)
    else:
        raise(KeyError)
        
@input_error
def show_phone(args, contacts):
    return contacts[args[0]]

@input_error
def show_all(args,contacts):
    s=''
    for key in contacts:
        s+=(f"{key:10} : {contacts[key]}\n")
    return s
    
def main():
    contacts = {'John':"123", 'Jane':"234", 'Steve':"555"}
    print("Welcome to the assistant bot!")
    commands = ["hello", "add", "change", "phone", "all", "close", "exit"]
    while True:
        user_input = input(f"Enter a command ({commands}): \n>>> ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "show":
            print(show_phone(args,contacts))
        elif command == "all":
            print(show_all(args,contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()