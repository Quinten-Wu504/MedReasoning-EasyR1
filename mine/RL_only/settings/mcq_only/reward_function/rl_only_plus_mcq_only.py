#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Any, List, Dict

def format_reward(response: str) -> float:
    """
    Check if the response follows the expected multiple-choice format (e.g., 'A: content').
    """
    pattern = re.compile(r"^[A-F]:\s*\S.*$", re.DOTALL)
    format_match = re.fullmatch(pattern, response.strip())
    return 1.0 if format_match else 0.0

def accuracy_reward(response: str, ground_truth: str) -> float:
    """
    Compute accuracy reward based on response and ground truth for multiple-choice questions.
    - Match both the option letter and content (case-sensitive, ignoring spaces and punctuation).
    """
    # Normalize response and ground truth by removing leading/trailing spaces and newlines
    response_clean = re.sub(r"^[ \n]+|[ \n]+$", "", response)
    ground_truth_clean = re.sub(r"^[ \n]+|[ \n]+$", "", ground_truth)

    # Extract option letter and content for multiple-choice question
    mcq_pattern = re.compile(r"^([A-F]):\s*(.*)")
    gt_parts = re.match(mcq_pattern, ground_truth_clean)
    ans_parts = re.match(mcq_pattern, response_clean)
    
    if not gt_parts or not ans_parts:
        return 0.0
    
    gt_letter, gt_content = gt_parts.groups()
    ans_letter, ans_content = ans_parts.groups()
    
    # Compare both letter and content (case-sensitive, ignoring trailing punctuation)
    gt_content_clean = re.sub(r"[.,:;?!]$", "", gt_content.strip())
    ans_content_clean = re.sub(r"[.,:;?!]$", "", ans_content.strip())
    
    return 1.0 if gt_letter == ans_letter and gt_content_clean == ans_content_clean else 0.0

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
        response = reward_input["response"]
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
            "response": "C: The appressorium",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "C:The appressorium",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "C: The appressorium,",
            "ground_truth": "C: The appressorium."
        },
        {
            "response": "Normal",  # Invalid format
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "B: Incorrect",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "B: The appressorium",
            "ground_truth": "C: The appressorium"
        },
        {
            "response": "C: Wrong content",  # Correct letter, wrong content
            "ground_truth": "C: The appressorium"
        }
    ]
    
    scores = compute_score(test_inputs)
    for i, score in enumerate(scores):
        print(f"Test case {i + 1}: {score}")