import json
import glob

files = glob.glob("data/splits/*.json")
print("JSON files:", files)

for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        d = json.load(fp)

    print("\nFILE:", f)
    print("KEYS:", list(d.keys()))

    for k, v in d.items():
        if isinstance(v, list):
            print(f"  {k}: {len(v)}")
        elif isinstance(v, dict):
            print(f"  {k}: dict keys={list(v.keys())[:10]}")
        else:
            print(f"  {k}: {type(v)}")