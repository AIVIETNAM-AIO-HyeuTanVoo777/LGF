# Gallery/Probe Construction Audit

Detailed audit of gallery and probe partitions, class support, and session-direction verification.

| split_file                                     |   gallery_images |   probe_images |   gallery_classes |   probe_classes | every_probe_class_has_gallery_support   | every_gallery_class_has_probe_support   | direction_mismatch   | status   |
|:-----------------------------------------------|-----------------:|---------------:|------------------:|----------------:|:----------------------------------------|:----------------------------------------|:---------------------|:---------|
| iitd_subject_disjoint_within_seed2026.json     |              251 |            276 |                92 |              92 | yes                                     | yes                                     | False                | PASS     |
| iitd_subject_disjoint_within_seed2705.json     |              242 |            276 |                92 |              92 | yes                                     | yes                                     | False                | PASS     |
| iitd_subject_disjoint_within_seed42.json       |              238 |            276 |                92 |              92 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s1_to_s2_seed2026.json |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s1_to_s2_seed2705.json |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s1_to_s2_seed42.json   |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s2_to_s1_seed2026.json |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s2_to_s1_seed2705.json |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
| tongji_subject_disjoint_s2_to_s1_seed42.json   |             1200 |           1200 |               120 |             120 | yes                                     | yes                                     | False                | PASS     |
