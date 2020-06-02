#!/usr/local/bin/python3

import json
import re
import sys


with open(str(sys.argv[1])) as f:
    data = json.load(f)[0]


question_list = []
clozes = []


def create_tag_string(tag_l):
    return " ".join(x.replace(" ", "_") for x in tag_l)


def create_cloze_if_pattern_match(s, tags):
    matches = re.findall(r'(?<=\[).+?(?=\])', s)
    tmp = s
    i = 1
    if (not "[TODO" in matches):
        for ma in matches:
            tmp = re.sub(re.escape("[" + ma +"]"), "{{c" + str(i) + "::" + ma + "}}", tmp)
            i = i + 1
            if matches[-1] == ma: clozes.append({"c": tmp, "tags": create_tag_string(tags)})


def create_questions(d, tags):
    create_cloze_if_pattern_match(d.get("string", ""), tags[:])
    if d.get("string", "") == "Q::":
        q = d["children"][0]["string"]
        a = [x['string'] for x in d["children"][1:]]
        question_list.append({"q": q, "a": a, "tags": create_tag_string(tags)})
    elif d.get("children", False):
        tags.append(d.get("string", d.get("title")))
        for d_c in d["children"]:
            create_questions(d_c, tags.copy())


create_questions(data, [])


with open("questions.txt", "w") as f2:
    for q in question_list:
        ans = "<br>".join(q["a"])
        f2.write(q["q"] + " ;" + '"' + ans + '"' + " ;" + q["tags"] + "\n")


with open("cloze.txt", "w") as f3:
    for c in clozes:
        f3.write( c["c"] + " ;" + c["tags"] + "\n")

