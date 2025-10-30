#!/bin/bash

set -x

export WANDB_API_KEY=a92faa423301cc9e4934bd7b8f36b4a6a73a7067
export WANDB_PROJECT=EasyR1
export WANDB_RUN_GROUP="SFT_plus_RL_plus_mixed_mcq"
export WANDB_NAME="qwen3_vl_4b_sft_plus_rl_plus_mixed_mcq_grpo"
export WANDB_DIR=./wandb_logs

export HF_DATASETS_DISABLE_MULTIPROCESSING=1
export TOKENIZERS_PARALLELISM=false

MODEL_PATH=Qwen/Qwen3-VL-4B-Instruct

python3 -m verl.trainer.main \
    config=mine/SFT_plus_RL/settings/mixed_mcq/scripts/qwen3_vl_4b/config.yaml \
    data.train_files=QuintenWu/RL_Mixed_MCQ_Filtered_Our_PMC@train \
    data.val_files=QuintenWu/RL_Mixed_MCQ_Filtered_Our_PMC@validation \
    data.rollout_batch_size=256 \
    worker.actor.model.model_path=${MODEL_PATH} \
    worker.rollout.limit_images=0 \
    trainer.experiment_name=qwen3_vl_4b_sft_plus_rl_plus_mixed_mcq_grpo \
    trainer.n_gpus_per_node=8
