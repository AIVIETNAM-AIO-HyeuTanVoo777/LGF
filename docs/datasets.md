# Datasets

Supported datasets:

- Tongji: primary audited cross-session S1->S2 and S2->S1 evaluation.
- IITD: secondary within-session validation.

Raw datasets are not redistributed. Obtain them from official sources and follow their licenses and citation requirements.

Expected local segmented-image layout:

```text
data/segmented/Tongji/session1/*.bmp
data/segmented/Tongji/session2/*.bmp
data/segmented/IITD/Left/*.bmp
data/segmented/IITD/Right/*.bmp
```

The tracked files under `data/metadata/` and `data/splits/` are non-image metadata and split definitions with relative paths.
