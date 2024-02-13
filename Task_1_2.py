from typing import Callable
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
    numbers = map(float, filter(lambda x: re.match(r"\d+\.{0,1}\d+",x),text.split(" ")))
    for number in numbers:
        yield number

def sum_profit(text: str, func: Callable):
    return reduce(lambda x,y:x+y ,func(text))

if __name__=="__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")





