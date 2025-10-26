#!/bin/bash

set -x

export WANDB_API_KEY=a92faa423301cc9e4934bd7b8f36b4a6a73a7067
export WANDB_PROJECT=EasyR1
export WANDB_NAME="qwen2_5_vl_7b_medreason_grpo"
export WANDB_RUN_GROUP="medreason_grpo"
export WANDB_DIR=./wandb_logs
MODEL_PATH=Qwen/Qwen2.5-VL-7B-Instruct  # replace it with your local file path

python3 -m verl.trainer.main \
    config=mine/config.yaml \
    data.train_files=QuintenWu/mixed_mcq_filtered_pmc@train \
    data.val_files=QuintenWu/mixed_mcq_filtered_pmck@validation \
    data.rollout_batch_size=128 \
    worker.actor.model.model_path=${MODEL_PATH} \
    worker.rollout.limit_images=3 \
    trainer.experiment_name=qwen2_5_vl_7b_medreason_grpo \
    trainer.n_gpus_per_node=8
