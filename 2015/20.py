# pylint: disable-all

def find_divisors(n): 
    divisors = set[int]()
    for i in range(1, int(n**0.5) + 1): 
        if n % i == 0:
            divisors.add(i * 10)
            divisors.add(n // i * 10)
    return sum(divisors) 
    
def find_divisors2(n): 
    divisors = set[int]()
    for i in range(1, int(n**0.5) + 1): 
        if n % i == 0:
            if n <= i * 50:
                divisors.add(i * 11)
            if n <= n // i * 50:
                divisors.add(n // i * 11)
    return sum(divisors) 
    


def silver_solution(lines: list[str]) -> int:
    input = int(lines[0])

    i = 1
    while True:
        presents = find_divisors(i)
        if presents >= input:
            break

        i += 1

        if i % 100000 == 0:
            print(i)

    # for i in range(10):
    #     print(find_divisors(i))

    return i

def gold_solution(lines: list[str]) -> int:
    input = int(lines[0])

    i = 1
    while True:
        presents = find_divisors2(i)
        if presents >= input:
            break

        i += 1

        if i % 100000 == 0:
            print(i)

    # for i in range(10):
    #     print(find_divisors(i))

    return i
