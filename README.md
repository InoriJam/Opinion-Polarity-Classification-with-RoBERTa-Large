# Opinion-Polarity-Classification-with-RoBERTa-Large
China Artificial Intelligence Competition · Language and Knowledge Technology Competition 9th
# 简介
阅读理解是自然语言处理和人工智能领域的重要前沿课题，对于提升机器智能水平、使机器具有持续知识获取能力具有重要价值。观点极性分类是机器阅读理解中的一个难点问题，观点极性分类一般为三分类，分为Yes、No、Depends，这就不仅要求模型能够对语义进行准确建模，而且还要具有良好的鲁棒性，这对传统的模型提出了挑战。为此，本文对数据集进行数据增强，使用RoBERTa Large模型进行迁移学习，在观点极性分类问题上取得了较好的效果。本文提出的方案在中国人工智能大赛·语言与知识技术竞赛（个人赛）中取得了第九名的成绩，B榜测试集准确率 84.81%，高于基线系统水平。
# 数据预处理
经过统计，训练集中标签为Yes的39092条, No 24787条, Depends 11512条，可以发现，训练集存在一定程度的样本不平衡现象，这导致模型可能会在训练的时候对某些类带有偏见，导致模型鲁棒性低，对训练集进行适当的数据增强，可以一定程度上改善类别不平衡的情况，也能够提升模型的鲁棒性，关于文本的常见数据增强方法有：同义句生成、回译、同义词替换、随机增删词语等，其中公认的文本数据增强方法以回译效果最佳，而且回译在实现难度上比其他方法更低。观察整个训练集的文本，发现很多问句末尾都不包含问号，为保证翻译的准确性，在预处理阶段为所有缺失问号的问题加上问号。由于训练集较大，本文不采用API进行回译，而是将训练集的文本在去除标签后转为docx格式并使用Google翻译提供的文档翻译功能进行批量回译，回译完成后再重新匹配标签，选出回译结果中所有标签为Depends的数据加入原有的训练集形成新的训练集用于训练。
# 具体操作
采用json2tsv.py实现比赛数据集到paddlehub数据集格式的转换 然后利用Google翻译的文档翻译功能对训练集进行了回译，并选出回译结果中所有标签为Depends的数据与原有的train.tsv放在一起生成train_aug.tsv

其中for_trans.py用于生成提交到google翻译的docx文档，翻译成英文后，从网页上把结果保存下来去除空行成为train.raw， 然后使用raw2docx.py转换成docx再把此文档翻译回中文（这里分了两个part）,翻译结果拼接成train_trans.raw， 使用pair_gen.py恢复标签，最后用select_dep.py过滤出回译结果中标签为Depends的训练数据。（过于复杂，有一部分需要手工操作，处理好的文件在dataset目录下train_aug.tsv）
# 环境
+ paddlepaddle 1.7.0
+ python 3
+ paddlehub 1.6.1
# 安装依赖
```shell
pip install mafan
pip install paddlehub==1.6.1 --upgrade
pip install docx
pip install tqdm
```
# 训练
```shell
python train.py --lr 0.02 --max_epoch 1
python train.py --lr 0.02 --max_epoch 2
python train.py --lr 0.002 --max_epoch 3
```
# 预测
```shell
python predict.py
```
