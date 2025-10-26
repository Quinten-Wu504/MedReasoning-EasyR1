#!/bin/bash

set -x

export WANDB_API_KEY=a92faa423301cc9e4934bd7b8f36b4a6a73a7067
export WANDB_PROJECT=EasyR1
export WANDB_RUN_GROUP="RL_only_plus_MCQ_only"
export WANDB_NAME="qwen2_5_vl_7b_rl_only_plus_mcq_only_grpo"
export WANDB_DIR=./wandb_logs

export HF_DATASETS_DISABLE_MULTIPROCESSING=1
export TOKENIZERS_PARALLELISM=false

MODEL_PATH=Qwen/Qwen2.5-VL-7B-Instruct

python3 -m verl.trainer.main \
    config=mine/RL_only/settings/mcq_only/scripts/qwen2_5_vl_7b/config.yaml \
    data.train_files=QuintenWu/PMC_VQA_orig@train \
    data.val_files=QuintenWu/PMC_VQA_orig@validation \
    data.rollout_batch_size=256 \
    worker.actor.model.model_path=${MODEL_PATH} \
    worker.rollout.limit_images=0 \
    trainer.experiment_name=qwen2_5_vl_7b_rl_only_plus_mcq_only_grpo \
    trainer.n_gpus_per_node=8
