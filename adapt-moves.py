#!/usr/bin/env python3

import json
import re

moveCategoryList = None

with open("moves-ironsworn.json","r") as f:
    moveCategoryList = json.load(f)

tiddlerList = []

# tags = """Move"""
tags = "Move"

# for each type
for category in moveCategoryList:
    # move-type = "Name"
    moveType = category["Name"]

    print(moveType)

    # for each move
    for move in category["Moves"]:
        moveDict = {}
        moveDict["move-type"] = moveType
        moveDict["tags"] = tags
        moveDict["module"] = move["$id"].split('/')[0]

        # title = "first part of id"/"Name"
        moveDict["title"] = move["$id"].split('/')[0] + "/" + move["Name"]

        print(moveDict["title"])

        # start building text
        textList = []

        # move text
        # replace bolds
        p = re.compile("\*\*")
        moveTextAdapted = p.sub(r"''", move["Text"])

        # replace links
        p = re.compile("\[([\w ]*)\]\((\w*)/[\w/]*\)")
        moveTextAdapted = p.sub(r"[[\1|\2/\1]]", moveTextAdapted)

        textList.append(moveTextAdapted)

        # move oracles TODO

        assetDict["text"] = "\n\n".join(textList)

        print(moveDict)

        tiddlerList.append(moveDict)

with open("adapted-moves.json","w") as f:
    json.dump(tiddlerList, f)
