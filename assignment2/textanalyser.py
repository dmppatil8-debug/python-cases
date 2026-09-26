
import string


# Topic 1: Clean Words

text = "Python is a powerful programming language. It is widely used for data science, machine learning, artificial intelligence, and automation! Python's simple syntax makes it easy to learn, but its large ecosystem makes it powerful for real-world projects."


def clean_words(text):
    text = text.lower()

    for i in string.punctuation:
        text = text.replace(i, "")

    new_text = text.split()

    return new_text


result = clean_words(text)
print(result)


# Topic 2: Word Frequency

def word_frequency(words):
    frequency = {}

    for i in words:
        if i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1

    return frequency


frequency = word_frequency(result)
print(frequency)


# Topic 3: Counting Repeated Words

text = "apple banana apple mango banana apple orange mango"

new = text.split()

frequency = {}

for i in new:
    count = new.count(i)
    frequency[i] = count

print(frequency)


# Topic 4: Top N Words

def top_n(freq, n):
    word_count = []

    for i, count in freq.items():
        word_count.append((i, count))

    word_count.sort(key=lambda x: x[1], reverse=True)

    return word_count[:n]


words = clean_words(text)

freq = word_frequency(words)

print(top_n(freq, 3))


# Topic 5: Palindrome

words = ["hello", "level", "world", "radar", "python", "civic"]


def find_palindromes(words):
    palindromes = []

    for i in words:
        if i == i[::-1]:
            palindromes.append(i)

    return palindromes


print(find_palindromes(words))


# Topic 6: Group Anagrams

def group_anagrams(words):
    groups = {}

    for word in words:
        key = "".join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return groups


words = ["listen", "silent", "evil", "vile", "hello"]

print(group_anagrams(words))


# Topic 7: Pangram

import string


def is_pangram(text):
    text = text.lower()

    for letter in string.ascii_lowercase:
        if letter not in text:
            return False

    return True


text = "The quick brown fox jumps over the lazy dog"

print(is_pangram(text))

