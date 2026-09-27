def top_n(freq, n):
    word_count = []

    for i, count in freq.items():
        word_count.append((i, count))

    word_count.sort(key=lambda x: x[1], reverse=True)

    return word_count[:n]