import json
import logging
import sys
from collections import OrderedDict, defaultdict
from operator import itemgetter

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from livesplit_builder import build_splits


LOGGER = logging.getLogger(__name__)


def get_gem_prompt(completer):
    return prompt("> ", completer=completer)


def build_gems_list(gems):
    gem_names = [_["name"] for _ in gems]
    auto_complete = WordCompleter(
        gem_names,
        ignore_case=True,
        match_middle=True,
        sentence=True,
    )

    print("Select gems. ^D to finish")
    selected = []
    while True:
        try:
            g = get_gem_prompt(auto_complete)
            if g not in gem_names:
                continue
            else:
                selected.append(g)
        except EOFError:
            return selected


def valid_for_class(classes, klass):
    if not classes:
        return True
    else:
        return klass in classes


def get_gem_progression(selected_gems, gems, quests, klass=None):
    if klass is not None:
        klass = klass.lower()
    else:
        LOGGER.warning("Character class not supplied, results will be suboptimal")

    gem_info = [_ for _ in gems if _["name"] in selected_gems]
    quests_map = OrderedDict()
    for q in quests:
        # "reward" will have gem, "vendors": will have vendor_name: gems
        quests_map[q["quest"]] = {"reward": None, "vendors": defaultdict(list), "act": q["act"]}

    for g in gem_info:
        if g["quest_reward"] and valid_for_class(g["quest_reward"]["classes"], klass):
            quest_name = g["quest_reward"]["quest"]
            if not quests_map[quest_name]["reward"]:
                quests_map[quest_name]["reward"] = g["name"]
                continue

        for vendor_reward in sorted(g["vendor_reward"], key=itemgetter("act")):
            if valid_for_class(vendor_reward["classes"], klass):
                vendor_name = vendor_reward["vendor"]
                quests_map[vendor_reward["quest"]]["vendors"][vendor_name].append(g["name"])
                break

    return quests_map


def get_splits(gem_progression):
    for quest_name, details in gem_progression.items():
        if not details["reward"] and not details["vendors"]:
            continue

        act = details["act"]
        gem = details["reward"]
        if gem:
            yield f"{gem.replace('Support', '(S)')} - Quest Reward (\"{quest_name}\", {act})"
            # yield {"gem": gem, "quest": quest_name, "act": act}

        vendors = details["vendors"]
        if not vendors:
            continue

        for v, gems in vendors.items():
            for gem in gems:
                yield f"{gem.replace('Support','(S)')} - from \"{v}\" (\"{quest_name}\", {act})"
                # yield {"gem": gem, "quest": quest_name, "act": act, "vendor": v}


def print_splits(splits):
    print(build_splits(splits))


def main(gems_file, quests_file, klass=None):
    with open(gems_file) as f:
        gems = json.loads(f.read())["gems"]

    selected = build_gems_list(gems)

    with open(quests_file) as f:
        quests = json.loads(f.read())["quests"]

    gem_progression = get_gem_progression(selected, gems, quests, klass=klass)
    splits = get_splits(gem_progression)

    print("="*30)
    print_splits(splits)


if __name__ == "__main__":
    main("gems.json", "quests.json", klass=sys.argv[1])
