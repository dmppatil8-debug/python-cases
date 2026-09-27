
original = int(input("Enter the Number"))
n = original

def isarmstrong(n):
    original = n
    digits = len(str(original))
    total = 0

    while n != 0:
        digit = n % 10
        power = digit ** digits
        total = total + power
        n = n // 10

    return original == total

print(isarmstrong(n)) 
 
n=100000
for i in range(1,n+1):
    if isarmstrong(i):
        print(i)
    



            
        
    