import json

import requests
import re
from bs4 import BeautifulSoup


GEM_REWARDS_PAGE = "https://pathofexile.gamepedia.com/List_of_skill_gems_rewarded_from_quests"

REWARD_TEXT_RE = re.compile(r"Act (?P<act>\d) after (?P<quest>.+?) with (?P<classes>any character|[\w,\s]+)")
VENDOR_REWARD_TEXT_RE = re.compile(
    r"Act (?P<act>\d) after (?P<quest>.+?) from (?P<vendor>.+?) with (?P<classes>any character|[\w,\s]+)"
)


def parse_reward_info(match_obj, vendor=True):
    if not match_obj:
        return

    classes = [_.strip() for _ in match_obj.group("classes").lower().split(",")]
    if classes == ["any character"]:
        classes = None

    return {
        "act": match_obj.group("act"),
        "quest": match_obj.group("quest"),
        "vendor": match_obj.group("vendor") if vendor else None,
        "classes": classes
    }


def parse_gem_info(row):
    gem, quest_reward, vendor_reward = row.find_all("td")
    return {
        "name": gem.find("a").text,
        "quest_reward": parse_reward_info(
            REWARD_TEXT_RE.match(quest_reward.text), vendor=False
        ),
        "vendor_reward": [
            parse_reward_info(_) for _ in VENDOR_REWARD_TEXT_RE.finditer(vendor_reward.text)
        ],
    }


def get_quest_reward_gems():
    res = requests.get(GEM_REWARDS_PAGE)
    res.raise_for_status()
    parsed = BeautifulSoup(res.content, "html.parser")

    # skipping first since its the header in raw html
    for row in parsed.find("table").find_all("tr")[1:]:
        yield parse_gem_info(row)


def main():
    print(json.dumps({"gems": list(get_quest_reward_gems())}))


if __name__ == "__main__":
    main()
