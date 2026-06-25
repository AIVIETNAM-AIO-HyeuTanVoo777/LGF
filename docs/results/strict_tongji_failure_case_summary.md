# Strict Tongji Failure Case Analysis

This file summarizes reconstructed failure cases from saved `scores.csv` files.

The reconstruction uses the split JSON gallery/probe order and the score export order from `eval_embedding.py`: genuine scores first, followed by impostor scores.

## Summary

| Method | Direction | Seed | Threshold | FAR | TAR | FA@thr | FR@thr | Rank-1 errors | Rank-1 acc. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B1 | S1->S2 | 42 | 0.551223 | 0.001000 | 0.598833 | 1428 | 4814 | 154 | 0.871667 |
| B1 | S1->S2 | 2026 | 0.465813 | 0.001000 | 0.681000 | 1428 | 3828 | 85 | 0.929167 |
| B1 | S1->S2 | 2705 | 0.443614 | 0.001000 | 0.756250 | 1428 | 2925 | 60 | 0.950000 |
| B1 | S2->S1 | 42 | 0.431853 | 0.000999 | 0.762000 | 1427 | 2856 | 54 | 0.955000 |
| B1 | S2->S1 | 2026 | 0.457060 | 0.000996 | 0.702833 | 1423 | 3566 | 76 | 0.936667 |
| B1 | S2->S1 | 2705 | 0.405619 | 0.000998 | 0.805333 | 1425 | 2336 | 47 | 0.960833 |
| B5 | S1->S2 | 42 | 0.406622 | 0.000999 | 0.715750 | 1427 | 3411 | 75 | 0.937500 |
| B5 | S1->S2 | 2026 | 0.398102 | 0.000998 | 0.741833 | 1425 | 3098 | 72 | 0.940000 |
| B5 | S1->S2 | 2705 | 0.374180 | 0.001000 | 0.793167 | 1428 | 2482 | 63 | 0.947500 |
| B5 | S2->S1 | 42 | 0.384169 | 0.001000 | 0.753667 | 1428 | 2956 | 50 | 0.958333 |
| B5 | S2->S1 | 2026 | 0.433411 | 0.001000 | 0.671500 | 1428 | 3942 | 98 | 0.918333 |
| B5 | S2->S1 | 2705 | 0.417207 | 0.001000 | 0.683167 | 1428 | 3802 | 87 | 0.927500 |
| B6 | S1->S2 | 42 | 0.421851 | 0.001000 | 0.658833 | 1428 | 4094 | 114 | 0.905000 |
| B6 | S1->S2 | 2026 | 0.366591 | 0.001000 | 0.743167 | 1428 | 3082 | 79 | 0.934167 |
| B6 | S1->S2 | 2705 | 0.425930 | 0.000998 | 0.670000 | 1425 | 3960 | 111 | 0.907500 |
| B6 | S2->S1 | 42 | 0.394965 | 0.001000 | 0.679667 | 1428 | 3844 | 103 | 0.914167 |
| B6 | S2->S1 | 2026 | 0.370295 | 0.000996 | 0.758000 | 1423 | 2904 | 62 | 0.948333 |
| B6 | S2->S1 | 2705 | 0.401516 | 0.000999 | 0.672750 | 1426 | 3927 | 92 | 0.923333 |
| B8 | S1->S2 | 42 | 0.406486 | 0.001000 | 0.703500 | 1428 | 3558 | 96 | 0.920000 |
| B8 | S1->S2 | 2026 | 0.382879 | 0.001000 | 0.723000 | 1428 | 3324 | 64 | 0.946667 |
| B8 | S1->S2 | 2705 | 0.396989 | 0.000999 | 0.724583 | 1426 | 3305 | 115 | 0.904167 |
| B8 | S2->S1 | 42 | 0.362643 | 0.001000 | 0.764833 | 1428 | 2822 | 67 | 0.944167 |
| B8 | S2->S1 | 2026 | 0.375628 | 0.000998 | 0.746250 | 1425 | 3045 | 89 | 0.925833 |
| B8 | S2->S1 | 2705 | 0.383031 | 0.001000 | 0.727500 | 1428 | 3270 | 100 | 0.916667 |

## Top failure cases by type

### false_accept_top_score

| Method | Direction | Seed | Rank | Score | Probe class | Gallery class | Probe path | Gallery path |
|---|---|---:|---:|---:|---:|---:|---|---|
| B1 | S1->S2 | 42 | 1 | 0.726911 | 481 | 479 | `data/segmented/Tongji/session2/00211.bmp` | `data/segmented/Tongji/session1/00191.bmp` |
| B1 | S1->S2 | 42 | 2 | 0.713326 | 476 | 768 | `data/segmented/Tongji/session2/00168.bmp` | `data/segmented/Tongji/session1/03083.bmp` |
| B1 | S1->S2 | 42 | 3 | 0.707913 | 742 | 756 | `data/segmented/Tongji/session2/02829.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 4 | 0.700023 | 742 | 756 | `data/segmented/Tongji/session2/02823.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 5 | 0.697937 | 768 | 476 | `data/segmented/Tongji/session2/03083.bmp` | `data/segmented/Tongji/session1/00169.bmp` |
| B1 | S1->S2 | 42 | 6 | 0.694855 | 742 | 756 | `data/segmented/Tongji/session2/02828.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 7 | 0.694314 | 481 | 479 | `data/segmented/Tongji/session2/00212.bmp` | `data/segmented/Tongji/session1/00192.bmp` |
| B1 | S1->S2 | 42 | 8 | 0.693982 | 742 | 756 | `data/segmented/Tongji/session2/02822.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 9 | 0.693864 | 549 | 551 | `data/segmented/Tongji/session2/00894.bmp` | `data/segmented/Tongji/session1/00920.bmp` |
| B1 | S1->S2 | 42 | 10 | 0.693145 | 549 | 551 | `data/segmented/Tongji/session2/00894.bmp` | `data/segmented/Tongji/session1/00911.bmp` |
| B1 | S1->S2 | 42 | 11 | 0.693121 | 585 | 753 | `data/segmented/Tongji/session2/01256.bmp` | `data/segmented/Tongji/session1/02931.bmp` |
| B1 | S1->S2 | 42 | 12 | 0.692785 | 549 | 551 | `data/segmented/Tongji/session2/00894.bmp` | `data/segmented/Tongji/session1/00916.bmp` |
| B1 | S1->S2 | 42 | 13 | 0.691564 | 902 | 868 | `data/segmented/Tongji/session2/04425.bmp` | `data/segmented/Tongji/session1/04089.bmp` |
| B1 | S1->S2 | 42 | 14 | 0.687992 | 585 | 753 | `data/segmented/Tongji/session2/01256.bmp` | `data/segmented/Tongji/session1/02934.bmp` |
| B1 | S1->S2 | 42 | 15 | 0.686418 | 756 | 708 | `data/segmented/Tongji/session2/02969.bmp` | `data/segmented/Tongji/session1/02488.bmp` |
| B1 | S1->S2 | 42 | 16 | 0.684891 | 768 | 476 | `data/segmented/Tongji/session2/03090.bmp` | `data/segmented/Tongji/session1/00166.bmp` |
| B1 | S1->S2 | 42 | 17 | 0.684613 | 742 | 756 | `data/segmented/Tongji/session2/02827.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 18 | 0.684585 | 756 | 708 | `data/segmented/Tongji/session2/02962.bmp` | `data/segmented/Tongji/session1/02488.bmp` |
| B1 | S1->S2 | 42 | 19 | 0.682881 | 768 | 476 | `data/segmented/Tongji/session2/03081.bmp` | `data/segmented/Tongji/session1/00166.bmp` |
| B1 | S1->S2 | 42 | 20 | 0.681870 | 768 | 476 | `data/segmented/Tongji/session2/03090.bmp` | `data/segmented/Tongji/session1/00169.bmp` |

### false_reject_low_score

| Method | Direction | Seed | Rank | Score | Probe class | Gallery class | Probe path | Gallery path |
|---|---|---:|---:|---:|---:|---:|---|---|
| B1 | S1->S2 | 42 | 1 | -0.087389 | 811 | 811 | `data/segmented/Tongji/session2/03517.bmp` | `data/segmented/Tongji/session1/03515.bmp` |
| B1 | S1->S2 | 42 | 2 | -0.052233 | 948 | 948 | `data/segmented/Tongji/session2/04890.bmp` | `data/segmented/Tongji/session1/04884.bmp` |
| B1 | S1->S2 | 42 | 3 | -0.044407 | 811 | 811 | `data/segmented/Tongji/session2/03519.bmp` | `data/segmented/Tongji/session1/03514.bmp` |
| B1 | S1->S2 | 42 | 4 | -0.029076 | 811 | 811 | `data/segmented/Tongji/session2/03520.bmp` | `data/segmented/Tongji/session1/03514.bmp` |
| B1 | S1->S2 | 42 | 5 | -0.017942 | 811 | 811 | `data/segmented/Tongji/session2/03512.bmp` | `data/segmented/Tongji/session1/03514.bmp` |
| B1 | S1->S2 | 42 | 6 | -0.010980 | 948 | 948 | `data/segmented/Tongji/session2/04890.bmp` | `data/segmented/Tongji/session1/04881.bmp` |
| B1 | S1->S2 | 42 | 7 | -0.009021 | 811 | 811 | `data/segmented/Tongji/session2/03518.bmp` | `data/segmented/Tongji/session1/03515.bmp` |
| B1 | S1->S2 | 42 | 8 | -0.007460 | 948 | 948 | `data/segmented/Tongji/session2/04889.bmp` | `data/segmented/Tongji/session1/04884.bmp` |
| B1 | S1->S2 | 42 | 9 | -0.006942 | 515 | 515 | `data/segmented/Tongji/session2/00553.bmp` | `data/segmented/Tongji/session1/00552.bmp` |
| B1 | S1->S2 | 42 | 10 | -0.001670 | 948 | 948 | `data/segmented/Tongji/session2/04883.bmp` | `data/segmented/Tongji/session1/04884.bmp` |
| B1 | S1->S2 | 42 | 11 | 0.004698 | 948 | 948 | `data/segmented/Tongji/session2/04889.bmp` | `data/segmented/Tongji/session1/04881.bmp` |
| B1 | S1->S2 | 42 | 12 | 0.014785 | 811 | 811 | `data/segmented/Tongji/session2/03517.bmp` | `data/segmented/Tongji/session1/03516.bmp` |
| B1 | S1->S2 | 42 | 13 | 0.015714 | 811 | 811 | `data/segmented/Tongji/session2/03517.bmp` | `data/segmented/Tongji/session1/03514.bmp` |
| B1 | S1->S2 | 42 | 14 | 0.024853 | 894 | 894 | `data/segmented/Tongji/session2/04341.bmp` | `data/segmented/Tongji/session1/04345.bmp` |
| B1 | S1->S2 | 42 | 15 | 0.027520 | 894 | 894 | `data/segmented/Tongji/session2/04343.bmp` | `data/segmented/Tongji/session1/04345.bmp` |
| B1 | S1->S2 | 42 | 16 | 0.028495 | 894 | 894 | `data/segmented/Tongji/session2/04342.bmp` | `data/segmented/Tongji/session1/04345.bmp` |
| B1 | S1->S2 | 42 | 17 | 0.030007 | 894 | 894 | `data/segmented/Tongji/session2/04350.bmp` | `data/segmented/Tongji/session1/04345.bmp` |
| B1 | S1->S2 | 42 | 18 | 0.042764 | 948 | 948 | `data/segmented/Tongji/session2/04883.bmp` | `data/segmented/Tongji/session1/04881.bmp` |
| B1 | S1->S2 | 42 | 19 | 0.042846 | 811 | 811 | `data/segmented/Tongji/session2/03516.bmp` | `data/segmented/Tongji/session1/03512.bmp` |
| B1 | S1->S2 | 42 | 20 | 0.048352 | 811 | 811 | `data/segmented/Tongji/session2/03518.bmp` | `data/segmented/Tongji/session1/03514.bmp` |

### rank1_misidentification

| Method | Direction | Seed | Rank | Score | Probe class | Gallery class | Probe path | Gallery path |
|---|---|---:|---:|---:|---:|---:|---|---|
| B1 | S1->S2 | 42 | 1 | 0.726911 | 481 | 479 | `data/segmented/Tongji/session2/00211.bmp` | `data/segmented/Tongji/session1/00191.bmp` |
| B1 | S1->S2 | 42 | 2 | 0.700023 | 742 | 756 | `data/segmented/Tongji/session2/02823.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 3 | 0.694855 | 742 | 756 | `data/segmented/Tongji/session2/02828.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 4 | 0.693982 | 742 | 756 | `data/segmented/Tongji/session2/02822.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 5 | 0.693864 | 549 | 551 | `data/segmented/Tongji/session2/00894.bmp` | `data/segmented/Tongji/session1/00920.bmp` |
| B1 | S1->S2 | 42 | 6 | 0.693121 | 585 | 753 | `data/segmented/Tongji/session2/01256.bmp` | `data/segmented/Tongji/session1/02931.bmp` |
| B1 | S1->S2 | 42 | 7 | 0.691564 | 902 | 868 | `data/segmented/Tongji/session2/04425.bmp` | `data/segmented/Tongji/session1/04089.bmp` |
| B1 | S1->S2 | 42 | 8 | 0.684613 | 742 | 756 | `data/segmented/Tongji/session2/02827.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 9 | 0.681124 | 751 | 551 | `data/segmented/Tongji/session2/02912.bmp` | `data/segmented/Tongji/session1/00911.bmp` |
| B1 | S1->S2 | 42 | 10 | 0.678136 | 742 | 756 | `data/segmented/Tongji/session2/02821.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 11 | 0.671725 | 598 | 716 | `data/segmented/Tongji/session2/01387.bmp` | `data/segmented/Tongji/session1/02563.bmp` |
| B1 | S1->S2 | 42 | 12 | 0.671274 | 585 | 753 | `data/segmented/Tongji/session2/01259.bmp` | `data/segmented/Tongji/session1/02934.bmp` |
| B1 | S1->S2 | 42 | 13 | 0.667640 | 598 | 716 | `data/segmented/Tongji/session2/01382.bmp` | `data/segmented/Tongji/session1/02563.bmp` |
| B1 | S1->S2 | 42 | 14 | 0.667459 | 484 | 532 | `data/segmented/Tongji/session2/00250.bmp` | `data/segmented/Tongji/session1/00721.bmp` |
| B1 | S1->S2 | 42 | 15 | 0.666648 | 585 | 753 | `data/segmented/Tongji/session2/01258.bmp` | `data/segmented/Tongji/session1/02931.bmp` |
| B1 | S1->S2 | 42 | 16 | 0.665864 | 742 | 756 | `data/segmented/Tongji/session2/02830.bmp` | `data/segmented/Tongji/session1/02961.bmp` |
| B1 | S1->S2 | 42 | 17 | 0.663151 | 481 | 479 | `data/segmented/Tongji/session2/00215.bmp` | `data/segmented/Tongji/session1/00191.bmp` |
| B1 | S1->S2 | 42 | 18 | 0.662815 | 701 | 585 | `data/segmented/Tongji/session2/02413.bmp` | `data/segmented/Tongji/session1/01252.bmp` |
| B1 | S1->S2 | 42 | 19 | 0.659380 | 701 | 585 | `data/segmented/Tongji/session2/02419.bmp` | `data/segmented/Tongji/session1/01252.bmp` |
| B1 | S1->S2 | 42 | 20 | 0.657677 | 742 | 756 | `data/segmented/Tongji/session2/02826.bmp` | `data/segmented/Tongji/session1/02961.bmp` |

## Claim boundary

- Safe: this analysis identifies score-tail and rank-1 failure cases reconstructed from saved score files and split metadata.
- Safe: paths/classes are reconstructed using the same gallery/probe ordering used by evaluation.
- Unsafe: this analysis does not by itself diagnose visual image quality, unless image-quality features are separately computed.
- Unsafe: do not include image figures unless dataset policy permits image display.
