n = 9875
sum = 0

def digital_root(n):
    # n=abs(n)
    while n > 9:
        sum = 0
        while n != 0:
            digit = n % 10
            sum = sum + digit
            n = n // 10
        n = sum  
    return n

print(digital_root(n))  
