import paddlehub as hub
from paddlehub.dataset.base_nlp_dataset import BaseNLPDataset
import paddle.fluid as fluid
import numpy as np
import argparse

np.random.seed(1)
prog = fluid.default_main_program()
prog.random_seed = 1

parser = argparse.ArgumentParser(description='Opps...')
parser.add_argument('--lr', type=str, help='learning rate')
parser.add_argument('--max_epoch', type=int, help='max epoch')
args = parser.parse_args()

class Dataset(BaseNLPDataset):
    def __init__(self):
        self.dataset_dir = "./dataset"
        super(Dataset, self).__init__(
            base_path=self.dataset_dir,
            train_file="train_aug.tsv",
            dev_file="dev.tsv",
            test_file=None,
            predict_file="test2.tsv",
            train_file_with_header=False,
            dev_file_with_header=False,
            test_file_with_header=False,
            predict_file_with_header=False,
            # 数据集类别集合
            label_list=["Yes", "Depends", "No"])
dataset = Dataset()

from paddlehub import TransformerModule
from TransformerModule_patch import TransformerModule as TransformerModule_pat
TransformerModule.context = TransformerModule_pat.context

module = hub.Module(name="chinese-roberta-wwm-ext-large")
inputs, outputs, program = module.context(trainable=True, max_seq_len=128)
program.random_seed = 1


reader = hub.reader.ClassifyReader(
    dataset=dataset,
    vocab_path=module.get_vocab_path(),
    max_seq_len=128,
    random_seed=1)

print("learning rate: ", eval(args.lr))
print("max epoch: ", args.max_epoch)
strategy = hub.DefaultFinetuneStrategy(learning_rate=eval(args.lr), optimizer_name="sgd")

config = hub.RunConfig(use_cuda=True, num_epoch=args.max_epoch, batch_size=32, strategy=strategy, log_interval=100,
                 eval_interval=1400,save_ckpt_interval=1400, checkpoint_dir='./checkpoint_aug')
                 

pooled_output = outputs["pooled_output"]

feed_list = [
    inputs["input_ids"].name,
    inputs["position_ids"].name,
    inputs["segment_ids"].name,
    inputs["input_mask"].name
]

cls_task = hub.TextClassifierTask(
    data_reader=reader,
    feature=pooled_output,
    feed_list=feed_list,
    num_classes=dataset.num_labels,
    config=config)

cls_task.finetune_and_eval()