with open('./dataset/train_trans.tsv', 'r') as r, open('./dataset/train_dep.tsv', 'w') as w:
    lines = r.read().splitlines()
    for line in lines:
        if line.split('\t')[2] == "Depends":
            if line != lines[-1]:
                w.write(line.replace('？','') + '\n')
            else:
                w.write(line)