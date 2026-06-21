# Verified Literature Review

This file separates citations that are safe for the current paper draft from papers that still need metadata verification. The current paper draft uses only VERIFIED_CORE citations.

## 1. Palmprint Recognition

| Key | Paper | Venue/Year | Status | Why it is relevant | How used in paper |
|---|---|---|---|---|---|
| `gao2025deeplearning` | Chengrui Gao, Ziyuan Yang, Wei Jia, Lu Leng, Bob Zhang, Andrew Beng Jin Teoh. "Deep Learning in Palmprint Recognition: A Comprehensive Survey." | IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2026; also arXiv:2501.01166 | VERIFIED_CORE | Provides broad context for deep palmprint recognition, ROI processing, feature learning, and open challenges. | Cited to position the paper in deep palmprint recognition and motivate learned embeddings. |
| `tongji_dataset_unverified` | Tongji contactless palmprint dataset paper mentioned in the report as Zhang et al., 2017 PR. | Metadata incomplete in local report | RISKY | Would contextualize the Tongji benchmark used by this project. | Excluded from current draft until full author/title/venue/year are verified. |
| `glganet_unverified` | GLGAnet mentioned in the report as Zhang et al., 2023. | Metadata incomplete in local report | RISKY | Potential context for CNN+Transformer palmprint recognition. | Excluded from current draft until full metadata are verified. |
| `palmid_unverified` | Palm-ID mentioned in the report as Grosz et al., 2024. | Metadata incomplete in local report | RISKY | Potential context for mobile/end-to-end palmprint recognition. | Excluded from current draft until full metadata are verified. |
| `gabornet_unverified` | GaborNet mentioned in the report as Yang et al., 2026. | Metadata incomplete in local report | RISKY | Potential context for Gabor+CNN methods. | Excluded from current draft; also not used to revive a Gabor-superiority claim. |

## 2. Metric Learning for Biometrics

| Key | Paper | Venue/Year | Status | Why it is relevant | How used in paper |
|---|---|---|---|---|---|
| `deng2019arcface` | Jiankang Deng, Jia Guo, Niannan Xue, Stefanos Zafeiriou. "ArcFace: Additive Angular Margin Loss for Deep Face Recognition." | CVPR 2019 | VERIFIED_CORE | Defines the additive angular margin loss used by B6. | Cited in Introduction, Related Work, and Method for ArcFace supervision. |
| `luo2019strong` | Hao Luo, Wei Jiang, Youzhi Gu, Fuxu Liu, Xingyu Liao, Shenqi Lai, Jianyang Gu. "A Strong Baseline and Batch Normalization Neck for Deep Person Re-identification." | IEEE Transactions on Multimedia, 2020 | VERIFIED_CORE | Defines BNNeck, the normalization-neck design used by B6. | Cited in Introduction, Related Work, and Method for BNNeck. |
| `khosla2020supervised` | Prannay Khosla, Piotr Teterwak, Chen Wang, Aaron Sarna, Yonglong Tian, Phillip Isola, Aaron Maschinot, Ce Liu, Dilip Krishnan. "Supervised Contrastive Learning." | NeurIPS 2020 | VERIFIED_CORE | Defines SupCon, the metric-learning component in the B1 baseline and B7 ablation. | Cited in Introduction, Related Work, and Method for B1/B7 context. |

## 3. Cross-Session/Cross-Domain Robustness

| Key | Paper | Venue/Year | Status | Why it is relevant | How used in paper |
|---|---|---|---|---|---|
| `palmgan_unverified` | PalmGAN mentioned in the report as Shao et al., 2019 ICME. | Full title and author list not verified from local report | RISKY | Potential context for cross-domain palmprint adaptation. | Excluded from current draft. |
| `transfer_autoencoder_unverified` | Transfer convolutional autoencoder mentioned in the report as Shao et al., 2019 ICIP. | Full title and author list not verified from local report | RISKY | Potential context for adversarial cross-domain feature alignment. | Excluded from current draft. |
| `radah_unverified` | R-ADAH mentioned in the report as Du et al., 2021 TCSVT. | Full title and author list not verified from local report | RISKY | Potential context for adversarial domain-adaptive hashing. | Excluded from current draft. |
| `jpfa_unverified` | Joint Pixel and Feature Alignment mentioned in the report as Shao and Zhong, 2021 TIP. | Full title and author list not verified from local report | RISKY | Potential context for pixel/feature alignment under domain shift. | Excluded from current draft. |
| `genpalm_unverified` | GenPalm mentioned in the report as Grosz and Jain, 2024. | Venue metadata not verified from local report | RISKY | Potential context for synthetic palmprint generation. | Excluded from current draft. |
| `diffpalm_unverified` | Diff-Palm mentioned in the report as Jin et al., 2025. | Venue metadata not verified from local report | RISKY | Potential context for diffusion-based palmprint synthesis. | Excluded from current draft. |
| `xpalm_unverified` | X-Palm mentioned in the report as Seyedmohammadi et al., 2026. | Venue metadata not verified from local report | RISKY | Potential context for paired cross-device/cross-domain palmprint evaluation. | Excluded from current draft. |
