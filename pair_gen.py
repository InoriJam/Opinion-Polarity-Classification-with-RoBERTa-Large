import json
import re

filename = "train_trans"
length_arr = []
with open('./dataset/' + filename + '.raw', "r") as f, open('train.json', "r") as fp, open('./dataset/' + filename + '.tsv', "w") as w:
    out_arr = []
    line = fp.readline()
    while line:
        content = json.loads(line)

        text_a = f.readline().rstrip('\n')
        text_b = f.readline().rstrip('\n')
        label = content.get("yesno_answer")

        if label == "" and filename != "test":
            print("miss label")
            label = "Yes"
        if filename != "test":
            out_line = text_a + '\t' + text_b + '\t' + label
        else:
            out_line = text_a + '\t' + text_b
        out_arr.append(out_line)
        length_arr.append(len(out_line))
        line = fp.readline()

    print(filename + " aver length is:%d", sum(length_arr) / len(length_arr))
    print(filename + " max length is:%d", max(length_arr))
    print(filename + " over 512 length is:%d", len([x for x in length_arr if x > 512]))
    print(filename + " over 256 length is:%d", len([x for x in length_arr if x > 256]))
    print(filename + " over 128 length is:%d", len([x for x in length_arr if x > 128]))
    print(filename + " contains %d lines" % len(out_arr))
    print("######################################")
    for ele in out_arr:
        if ele != out_arr[-1]:
            w.write(ele + '\n')
        else:
            w.write(ele)