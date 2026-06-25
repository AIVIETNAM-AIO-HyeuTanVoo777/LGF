# Configs

Canonical configs for the paper are in `configs/rankb_final/`.

The naming convention is:

```text
m<variant>_<model_and_loss>_<dataset>_<direction>_seed<seed>.yaml
```

Tongji configs cover S1->S2 and S2->S1 for M0, M1, M2, M3, M4, M6, and M7 over seeds 42, 2026, and 2705. IITD configs cover within-session validation for M1 and M6.

Older B-series, debug, LGF, and Gabor-working configs are archived under `configs/legacy/old_working_configs/` and are not part of the submitted paper artifact.
