# Matrix Toolkit


# 1. Transpose
def transpose(m):
    result = []

    for j in range(len(m[0])):
        row = []

        for i in range(len(m)):
            row.append(m[i][j])

        result.append(row)

    return result


# 2. Multiply
def multiply(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Matrix dimensions do not match")

    result = []

    for i in range(len(a)):
        row = []

        for j in range(len(b[0])):
            total = 0

            for k in range(len(a[0])):
                total += a[i][k] * b[k][j]

            row.append(total)

        result.append(row)

    return result


# 3. Spiral Order
def spiral_order(m):
    result = []

    top = 0
    bottom = len(m) - 1
    left = 0
    right = len(m[0]) - 1

    while top <= bottom and left <= right:

        for j in range(left, right + 1):
            result.append(m[top][j])

        top += 1

        for i in range(top, bottom + 1):
            result.append(m[i][right])

        right -= 1

        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(m[bottom][j])

            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(m[i][left])

            left += 1

    return result


# 4. Rotate 90 Degrees
def rotate_90(m):
    result = transpose(m)

    for row in result:
        row.reverse()

    return result


# 5. Pretty Print
def pretty_print(m):
    for row in m:
        for value in row:
            print(f"{value:5}", end=" ")
        print()


# Testing
m = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Original Matrix:")
pretty_print(m)

print("\nTranspose:")
pretty_print(transpose(m))

print("\nRotate 90:")
pretty_print(rotate_90(m))

print("\nSpiral Order:")
print(spiral_order(m))

a = [
    [1, 2],
    [3, 4]
]

b = [
    [5, 6],
    [7, 8]
]

print("\nMultiplication:")
pretty_print(multiply(a, b))