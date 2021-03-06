import json

import requests
from bs4 import BeautifulSoup


QUEST_URL = "https://pathofexile.gamepedia.com/Quest"


def parse_quests(items):
    section = "?"  # acts
    for i in items:
        if i.name == "span":
            section = i.text
        else:
            yield {"quest": i.text.strip(), "act": section}


def get_quests():
    res = requests.get(QUEST_URL)
    res.raise_for_status()
    parsed = BeautifulSoup(res.content, "html.parser")
    items = parsed.select("h3 > .mw-headline, .mw-parser-output > ul > li")
    yield from parse_quests(items)


def main():
    print(json.dumps({"quests": list(get_quests())}))


if __name__ == "__main__":
    main()
