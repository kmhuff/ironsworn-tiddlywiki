#!/usr/bin/env python3

import json
import re

assetCategoryList = None

with open("assets-ironsworn.json","r") as f:
    assetCategoryList = json.load(f)

tiddlerList = []

# tags = """Asset"""
tags = "Asset"

# for each type
for category in assetCategoryList:
    # asset-type = "Name"
    assetType = category["Name"]

    print(assetType)

    # for each asset
    for asset in category["Assets"]:
        assetDict = {}
        assetDict["asset-type"] = assetType
        assetDict["tags"] = tags
        assetDict["module"] = asset["$id"].split('/')[0]

        # title = "first part of id"/"Name"
        assetDict["title"] = asset["$id"].split('/')[0] + "/" + asset["Name"]

        print(assetDict["title"])

        # start building text
        textList = []

        # for each input
        if "Inputs" in asset.keys():
            for input in asset["Inputs"]:
                print(input["Name"])
                # textList += "Name": <$edit-text field=\""Name".toLower()\"/>
                textList.append(input["Name"] + ": <$edit-text field=\"" + input["Name"].lower() + "\"/>")

        # textList += "Requirement"
        if "Requirement" in asset.keys():
            textList.append(asset["Requirement"])

        # for each ability
        for ability in asset["Abilities"]:
            # abilityText = "Text"
            abilityText = ability["Text"]

            # regex search for json link [\1](\2/.*). Replace with [[\1|\2/\1]]
            p = re.compile("\[([\w ]*)\]\((\w*)/[\w/]*\)")
            abilityTextAdapted = p.sub(r"[[\1|\2/\1]]", abilityText)

            # textList += <$checkbox with name "Name".toLower()> ''"Name":'' abilityText <$chekbox/>
            if "Name" in ability.keys():
                print(ability["Name"])
                textList.append("<$checkbox field=\"" + ability["Name"].lower() + "\" checked=\"taken\" unchecked=\"untaken\" default=\"untaken\"/> ''" + ability["Name"] + "'': " + abilityTextAdapted)
                if ability["Enabled"]:
                    assetDict[ability["Name"].lower()] = "taken"
            else:
                index = asset["Abilities"].index(ability)
                print(index)
                textList.append("<$checkbox field=\"" + str(index) + "\" checked=\"taken\" unchecked=\"untaken\" default=\"untaken\"/> " + abilityTextAdapted)
                if ability["Enabled"]:
                    assetDict[str(index)] = "taken"

            if "Inputs" in ability.keys():
                for input in ability["Inputs"]:
                    textList.append(input["Name"] + ": <$edit-text field=\"" + input["Name"].lower() + "\"/>")

        # if "Condition Meter"
        if "Condition Meter" in asset.keys():
            conditionMeter = asset["Condition Meter"]
            print("Condition Meter")
            # textList += "Name": <$edit-text field=\""Name".toLower()\" type=\"number\" size=2/> / "Max"
            textList.append(conditionMeter["Name"] + ": <$edit-text field=\"" + conditionMeter["Name"].lower() + "\" type=\"number\" size=2/> / " + str(conditionMeter["Max"]))
            assetDict[conditionMeter["Name"].lower()] = str(conditionMeter["Max"])

            if "Conditions" in conditionMeter.keys():
                for condition in conditionMeter["Conditions"]:
                    textList.append("<$checkbox field=\"" + condition.lower() + "\" checked=\"active\" unchecked=\"inactive\" default=\"inactive\"/> " + condition)

        # text = textList.concat(\n\n)
        assetDict["text"] = "\n\n".join(textList)

        print(assetDict)

        tiddlerList.append(assetDict)

with open("adapted-assets.json","w") as f:
    json.dump(tiddlerList, f)
