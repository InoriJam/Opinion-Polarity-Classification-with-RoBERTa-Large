import paddlehub as hub
from paddlehub.dataset.base_nlp_dataset import BaseNLPDataset
import paddle.fluid as fluid
import numpy as np
import json


np.random.seed(1)
prog = fluid.default_main_program()
prog.random_seed = 1

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
            label_list=["Yes", "Depends", "No"])
dataset = Dataset()

module = hub.Module(name="chinese-roberta-wwm-ext-large")
inputs, outputs, program = module.context(trainable=False, max_seq_len=128)
program.random_seed = 1
print(program.random_seed)


reader = hub.reader.ClassifyReader(
    dataset=dataset,
    vocab_path=module.get_vocab_path(),
    max_seq_len=128)


strategy = hub.DefaultFinetuneStrategy(learning_rate=0.002, optimizer_name="sgd")

config = hub.RunConfig(use_cuda=True, num_epoch=3, batch_size=32, strategy=strategy, log_interval=100,
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

data = [[d.text_a, d.text_b] for d in dataset.get_predict_examples()]
run_states = cls_task.predict(data, load_best_model=False)
results = [run_state.run_results for run_state in run_states]
labels=["Yes", "Depends", "No"]
id = 0
with open('predict_aug_sgd.json', "w") as fp:
    for batch_result in results:
        # get predict index
        batch_result = np.argmax(batch_result, axis=2)[0]
        for result in batch_result:
            content = {"id": id, "yesno_answer": labels[result]}
            content = json.dumps(content, ensure_ascii=False) + "\n"
            fp.write(content)
            id += 1