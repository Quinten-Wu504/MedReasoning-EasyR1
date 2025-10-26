#!/bin/bash

set -x

export WANDB_API_KEY=a92faa423301cc9e4934bd7b8f36b4a6a73a7067
export WANDB_PROJECT=EasyR1
export WANDB_NAME="qwen2_5_vl_7b_grpo_test_1"
export WANDB_RUN_GROUP="grpo_debug"
export WANDB_DIR=/opt/dlami/nvme/wujinxuan/wandb_logs
MODEL_PATH=Qwen/Qwen2.5-VL-7B-Instruct  # replace it with your local file path

python3 -m verl.trainer.main \
    config=examples/config.yaml \
    data.train_files=hiyouga/geometry3k@train \
    data.val_files=hiyouga/geometry3k@test \
    worker.actor.model.model_path=${MODEL_PATH} \
    trainer.experiment_name=qwen2_5_vl_7b_geo_grpo \
    trainer.n_gpus_per_node=8
