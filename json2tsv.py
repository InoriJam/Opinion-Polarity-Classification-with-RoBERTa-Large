import json
import mafan


filenames = ["train","dev","test2"]
for filename in filenames:
    count_dict = {"Yes":0,"No":0,"Depends":0}
    length_arr = []
    with open(filename + '.json', "r") as fp, open('./dataset/' + filename + '.tsv', "w") as w:
        out_arr = []
        line = fp.readline()
        while line:
            content = json.loads(line)

            text_a = content.get("question")
            text_b = content.get("answer")
            label = content.get("yesno_answer")
            text_a = text_a.replace(' ', '')
            text_b = text_b.replace(' ', '')
            text_a = text_a.replace('\t', '')
            text_b = text_b.replace('\t', '')
            text_a = mafan.simplify(text_a)
            text_b = mafan.simplify(text_b)

            if label == "" and filename != "test2":
                print("miss label")
                label = "Yes"
            if filename != "test2":
                count_dict[label] += 1
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
        print(filename + " over 64 length is:%d", len([x for x in length_arr if x > 64]))
        print(filename + " contains %d lines" % len(out_arr))
        print(count_dict)
        print("######################################")
        for ele in out_arr:
            if ele != out_arr[-1]:
                w.write(ele + '\n')
            else:
                w.write(ele)