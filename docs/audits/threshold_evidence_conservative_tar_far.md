# Threshold-Level Evidence for Conservative TAR@FAR

## Purpose

This audit exports threshold-level evidence for conservative TAR@FAR.

## Conservative invariant

`empirical_far <= target_far` for every checkable row.

## Output

`docs\results\threshold_evidence_conservative_tar_far.csv`

## Summary

- Rows exported: 84
- Rows with target and empirical FAR available: 84
- Conservative FAR violations: 0

## Columns

| Column | Meaning |
|---|---|
| dataset | Dataset name |
| method | Method or variant name |
| direction | Evaluation direction |
| seed | Random seed |
| num_genuine | Number of genuine pairs |
| num_impostor | Number of impostor pairs |
| target_far | Requested FAR target |
| selected_threshold | Conservative threshold selected for target FAR |
| empirical_far | Empirical FAR at selected threshold |
| tar | TAR at selected threshold |
| eer | Interpolated EER when available, otherwise nearest EER |
| eer_threshold | EER threshold associated with the run |
| source_file | Source evidence file |

## Status

PASS
