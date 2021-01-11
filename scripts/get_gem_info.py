import requests
import re
from bs4 import BeautifulSoup


GEM_REWARDS_PAGE = "https://pathofexile.gamepedia.com/List_of_skill_gems_rewarded_from_quests"

REWARD_TEXT_RE = re.compile("Act (\d{1}) after ([\w,\s]+) with (any character|[\w\,\s]+)")
VENDOR_REWARD_TEXT_RE = re.compile(
    "Act (\d{1}) after ([\w,\s]+) from ([\w\s]+) with (any character|[\w\,\s]+)"
)


def parse_gem_info(row):
    gem, quest_reward, vendor_reward = row.find_all("td")
    name = gem.find("a").text
    return (
        name,
        REWARD_TEXT_RE.findall(quest_reward.text),
        VENDOR_REWARD_TEXT_RE.findall(vendor_reward.text),
    )


def get_quest_reward_gems():
    res = requests.get(GEM_REWARDS_PAGE)
    res.raise_for_status()
    parsed = BeautifulSoup(res.content, "html.parser")

    # skipping first since its the header in raw html
    for row in parsed.find("table").find_all("tr")[1:]:
        yield parse_gem_info(row)


def main():
    print(list(get_quest_reward_gems()))


if __name__ == "__main__":
    main()

