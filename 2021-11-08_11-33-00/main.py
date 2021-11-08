import json
import re
from itertools import takewhile
from math import floor

if __name__ == "__main__":
    file = "$file"
    # config = "$config"

    html = open(file).read()

    prefix = '"evaluationTitle": "'

    # content = json.load(open(config))
    # title = content["reports"]["evaluationTitle"]
    # title = f"CodeGolfMovesCountNormalised{title}"
    # title = re.sub('[_: ,=.]', "", title)
    title = ""

    new_data = re.search(f"{title}:'.*'", html)
    index = new_data.span()[0] + len(f"{title}:'")

    if html[index:][0] == "—":
        data = re.findall(f"{title}:'.*'", html)
        data = [entry[len(title) + 2:-1] for entry in data]

        moves = []
        for d in data:
            num = "".join(list(takewhile(lambda x: x is not "'", d)))
            try:
                moves.append(float(num))
            except ValueError:
                continue

        mean = sum(moves) / len(moves)
        mean = floor(mean * 10 ** 3) / 10 ** 3
        print(mean)

        new_data = re.search(f"{title}:'.*'", html)
        index = new_data.span()[0] + len(f"{title}:'")
        html = html[:index] + str(mean) + html[index + 1:]
        open(file, "w").write(html)
