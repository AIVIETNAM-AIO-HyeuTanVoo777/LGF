# ArcFace Sensitivity Plan

## Purpose

This plan defines how ArcFace sensitivity should be handled after the metric/protocol correction.

## Current revision decision

The current revision does not run a new ArcFace margin or scale sweep. Instead, it reports fixed-recipe component sensitivity using existing strict Tongji ablation evidence:

- B4: ArcFace without BNNeck.
- B6: BNNeck + ArcFace.
- B7: BNNeck + ArcFace + light SupCon.
- B5: BNNeck + CE as the non-ArcFace BNNeck contrast.
- B1: CE + SupCon baseline.

This is sufficient to support the scoped claim that the tested ArcFace-based variants do not show a reliable gain under the strict Tongji palm-class-disjoint protocol.

## Locked protocol for any future margin sweep

A future ArcFace margin/scale sweep must be pre-registered before training. It must use:

- The same palm-class-disjoint Tongji split files.
- The same seeds: 42, 2026, 2705.
- The same directions: S1->S2 and S2->S1.
- The same model family and optimizer/training schedule as the strict ablation.
- Development-only train/validation data for checkpoint and hyperparameter selection.
- No gallery/probe/test information for margin, scale, checkpoint, early stopping, threshold, or model selection.

## Candidate sweep grid

A minimal future grid would vary one factor at a time:

- margin m: 0.30, 0.40, 0.50
- scale s: 30.0 fixed for the margin sweep
- optional follow-up scale sweep only after margin is fixed by development validation

## Reporting rule

If run later, the sweep must report all attempted configurations, not only the best one. Results should include Rank-1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3, selected thresholds, empirical FAR, and paired uncertainty over seed-direction units.

## Current evidence file

The current fixed-recipe evidence is documented in:

- `docs/results/arcface_sensitivity_evidence.md`
