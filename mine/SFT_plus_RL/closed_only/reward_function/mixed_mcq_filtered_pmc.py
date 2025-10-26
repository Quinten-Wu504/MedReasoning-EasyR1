#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Any, List, Dict

def extract_answer_content(response: str) -> str:
    """
    Extract the content within <answer> tags, removing leading/trailing whitespace and newlines.
    """
    pattern = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)
    match = pattern.search(response)
    if match:
        return match.group(1).strip()
    return ""

def format_reward(response: str) -> float:
    """
    Check if the response follows the expected <think>...</think><answer>...</answer> format.
    """
    pattern = re.compile(r"<think>.*?</think>\s*<answer>.*?</answer>", re.DOTALL)
    format_match = re.fullmatch(pattern, response.strip())
    return 1.0 if format_match else 0.0

def accuracy_reward(response: str, ground_truth: str) -> float:
    """
    Compute accuracy reward based on response and ground truth.
    - For multiple-choice questions (starting with 'A:', 'B:', etc.), match both the option letter and content.
    - For closed-end questions, match the full answer, ignoring leading/trailing spaces, newlines, and punctuation.
    """
    answer = extract_answer_content(response)
    if not answer:
        return 0.0

    # Normalize ground truth and answer by removing leading/trailing spaces, newlines, and trailing punctuation
    ground_truth_clean = re.sub(r"^[ \n]+|[ \n]+$", "", ground_truth)
    ground_truth_clean = re.sub(r"[.,:;?!]$", "", ground_truth_clean)
    answer_clean = re.sub(r"^[ \n]+|[ \n]+$", "", answer)
    answer_clean = re.sub(r"[.,:;?!]$", "", answer_clean)

    # Check if it's a multiple-choice question (starts with 'A:', 'B:', etc.)
    mcq_pattern = re.compile(r"^[A-D]:\s*")
    if mcq_pattern.match(ground_truth_clean):
        # Extract option letter and content
        gt_parts = re.match(r"^([A-D]):\s*(.*)", ground_truth_clean)
        ans_parts = re.match(r"^([A-D]):\s*(.*)", answer_clean)
        
        if not gt_parts or not ans_parts:
            return 0.0
        
        gt_letter, gt_content = gt_parts.groups()
        ans_letter, ans_content = ans_parts.groups()
        
        # Compare both letter and content (case-sensitive, ignoring trailing punctuation)
        gt_content_clean = re.sub(r"[.,:;?!]$", "", gt_content.strip())
        ans_content_clean = re.sub(r"[.,:;?!]$", "", ans_content.strip())
        
        return 1.0 if gt_letter == ans_letter and gt_content_clean == ans_content_clean else 0.0
    else:
        # Closed-end question: exact match ignoring spaces, newlines, and punctuation
        return 1.0 if ground_truth_clean == answer_clean else 0.0

def compute_score(reward_inputs: List[Dict[str, Any]], format_weight: float = 0.1) -> List[Dict[str, float]]:
    """
    Compute the reward score for a list of responses.
    - format_weight: Weight for format score (default 0.1, so accuracy dominates).
    - Returns a list of dicts with 'overall', 'format', and 'accuracy' scores.
    """
    if not isinstance(reward_inputs, list):
        raise ValueError("Please use `reward_type=batch` for reward function.")

    scores = []
    for reward_input in reward_inputs:
        response = re.sub(r"\s*(<|>|/)\s*", r"\1", reward_input["response"])  # Normalize tag spacing
        ground_truth = reward_input["ground_truth"]
        
        format_score = format_reward(response)
        accuracy_score = accuracy_reward(response, ground_truth)
        
        scores.append({
            "overall": (1 - format_weight) * accuracy_score + format_weight * format_score,
            "format": format_score,
            "accuracy": accuracy_score,
        })

    return scores


if __name__ == "__main__":
    # Example usage for testing
    test_inputs = [
        {
            "response": "<think>Reasoning here</think><answer>C: The appressorium</answer>",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "<think>Reasoning here</think><answer>\n\nC:The appressorium,\n\n</answer>",
            "ground_truth": "C: The appressorium."
        },
        {
            "response": "<think>Reasoning here</think><answer>Normal</answer>",
            "ground_truth": "Normal."
        },
        {
            "response": "<think>Reasoning here</think><answer>B: Incorrect</answer>",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "<answer>C: The appressorium</answer>",  # Invalid format
            "ground_truth": "C: The appressorium"
        }
    ]
    
    scores = compute_score(test_inputs)
    for i, score in enumerate(scores):
        print(f"Test case {i + 1}: {score}")