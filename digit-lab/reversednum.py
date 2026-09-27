n = -123

is_negative = n < 0
positive_n = abs(n)

rev = 0

while positive_n != 0:
    digit = positive_n % 10
    rev = rev * 10 + digit
    positive_n = positive_n // 10

if is_negative:
    rev = rev * -1

print(rev)