import json
from pathlib import Path
import pandas as pd


MANIFEST = Path("data/metadata/palm_segmented_manifest.csv")
SPLIT_FILES = [
    "data/splits/tongji_s1_to_s2.json",
    "data/splits/tongji_s2_to_s1.json",
    "data/splits/iitd_within.json",
    "data/splits/cross_dataset_fewshot.json",
]


def item_path(x):
    if isinstance(x, str):
        return x.replace("\\", "/")
    if isinstance(x, dict):
        for k in ["path", "image_path", "filepath", "file"]:
            if k in x:
                return str(x[k]).replace("\\", "/")
    return None


def normalize_path(p):
    return str(Path(p)).replace("\\", "/")


df = pd.read_csv(MANIFEST)
df["norm_path"] = df["path"].apply(normalize_path)

print("Manifest shape:", df.shape)
print("Manifest columns:", df.columns.tolist())
print(df.groupby("dataset").size())

path_to_row = {row["norm_path"]: row for _, row in df.iterrows()}

for sf in SPLIT_FILES:
    print("\n" + "=" * 80)
    print("SPLIT:", sf)

    with open(sf, "r", encoding="utf-8") as f:
        split = json.load(f)

    for key, items in split.items():
        if not isinstance(items, list):
            print(f"{key}: non-list {type(items)}")
            continue

        paths = [item_path(x) for x in items]
        paths = [p for p in paths if p is not None]

        rows = []
        missing = []
        for p in paths:
            np = normalize_path(p)
            if np in path_to_row:
                rows.append(path_to_row[np])
            else:
                missing.append(p)

        sub = pd.DataFrame(rows)

        print(f"\n[{key}] n={len(items)}, parsed_paths={len(paths)}, matched_manifest={len(sub)}, missing={len(missing)}")

        if len(sub) > 0:
            cols = [c for c in ["dataset", "session", "hand", "class_id", "palm_id", "sample_id"] if c in sub.columns]
            for c in ["dataset", "session", "hand"]:
                if c in sub.columns:
                    print(f"{c}:")
                    print(sub[c].value_counts(dropna=False).to_string())

            if "class_id" in sub.columns:
                print("unique classes:", sub["class_id"].nunique())

        if missing[:5]:
            print("missing examples:", missing[:5])