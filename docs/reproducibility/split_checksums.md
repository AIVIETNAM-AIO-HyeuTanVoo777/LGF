# Split Checksums

Fill after final split files are generated.

Suggested Windows command:

```bat
certutil -hashfile data\splits\<split_file>.json SHA256
```

Required entries:

```text
Tongji disjoint-identity S1→S2 seed42
Tongji disjoint-identity S2→S1 seed42
Tongji disjoint-identity S1→S2 seed2026
Tongji disjoint-identity S2→S1 seed2026
Tongji disjoint-identity S1→S2 seed2705
Tongji disjoint-identity S2→S1 seed2705
Optional IITD secondary splits
```
