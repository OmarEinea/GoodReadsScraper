import operator


def output(key, value):
    value_type = "" if value == int(value) else ".2f"
    print(f"{key:<25}{value:{value_type}}")


input_lines = open("reviews.csv", "r").readlines()
output("Number of reviews:", len(input_lines))

users = {}
books = {}
tokens = []
token_count = 0
sentence_count = 0

for line in input_lines:
    cells = line.split('\t')
    user = cells[1]
    users[user] = users[user] + 1 if user in users else 1
    book = cells[2]
    books[book] = books[book] + 1 if book in books else 1
    line_tokens = cells[6].split()
    tokens.append(len(line_tokens))
    token_count += len(line_tokens)
    for token in line_tokens:
        if '.' in token:
            sentence_count += 1

users = sorted(users.items(), key=operator.itemgetter(1))
output("Number of users:", len(users))
output("Avg. reviews per user:", len(input_lines) / len(users))
output("Max reviews per user:", users[-1][1])
output("Median reviews per user:", users[len(users) // 2][1])
output("Min reviews per user:", users[1][1])

books = sorted(books.items(), key=operator.itemgetter(1))
output("Number of books:", len(books))
output("Avg. reviews per book:", len(input_lines) / len(books))
output("Max reviews per book:", books[-1][1])
output("Median reviews per book:", books[len(books) // 2][1])
output("Min reviews per book:", books[1][1])
print(books[:5])
tokens = sorted(tokens)
output("Number of tokens:", token_count)
output("Avg. tokens per review:", token_count / len(tokens))
output("Max tokens per review:", tokens[-1])
output("Median tokens per review:", tokens[len(tokens) // 2])
output("Min tokens per review:", tokens[1])

output("Number of sentences:", sentence_count)
