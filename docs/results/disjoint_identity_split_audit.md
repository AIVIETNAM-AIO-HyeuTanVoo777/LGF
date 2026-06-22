# Disjoint-Identity Split Audit

- manifest: `data\metadata\palm_segmented_manifest.csv`
- dataset column: `dataset`
- identity column: `subject_id` (subject_id)
- session column: `session`
- path column: `path`
- write mode: `False`

Terminology rule: use `subject-disjoint` only if identity column is true subject_id. Otherwise use `disjoint-identity` or `palm-disjoint`.

# Tongji

## tongji_subject_disjoint_s1_to_s2_seed42.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

## tongji_subject_disjoint_s2_to_s1_seed42.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

## tongji_subject_disjoint_s1_to_s2_seed2026.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

## tongji_subject_disjoint_s2_to_s1_seed2026.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

## tongji_subject_disjoint_s1_to_s2_seed2705.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

## tongji_subject_disjoint_s2_to_s1_seed2705.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 480
- test identities: 120
- train images: 3840
- val images: 960
- gallery images: 1200
- probe images: 1200
- train/test identity overlap: 0

# IITD secondary within-dataset candidate splits

## iitd_subject_disjoint_within_seed42.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 184
- test identities: 46
- train images: 1670
- val images: 417
- gallery images: 257
- probe images: 257
- train/test identity overlap: 0
- note: IITD is secondary within-dataset validation, not cross-session evidence.

## iitd_subject_disjoint_within_seed2026.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 184
- test identities: 46
- train images: 1659
- val images: 415
- gallery images: 263
- probe images: 264
- train/test identity overlap: 0
- note: IITD is secondary within-dataset validation, not cross-session evidence.

## iitd_subject_disjoint_within_seed2705.json
- identity column: subject_id (subject_id)
- split record mode: records
- train identities: 184
- test identities: 46
- train images: 1666
- val images: 417
- gallery images: 259
- probe images: 259
- train/test identity overlap: 0
- note: IITD is secondary within-dataset validation, not cross-session evidence.
