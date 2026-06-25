from __future__ import annotations

import json
from pathlib import Path


def load_split(name: str) -> dict:
    return json.loads(Path("data/splits", name).read_text(encoding="utf-8"))


def values(rows: list[dict], key: str) -> set[str]:
    return {str(row[key]) for row in rows if key in row and row[key] not in (None, "")}


def test_tongji_split_has_no_development_test_overlap():
    split = load_split("tongji_subject_disjoint_s1_to_s2_seed42.json")
    dev = split["train"] + split["val"]
    test = split["gallery"] + split["probe"]

    assert values(dev, "path").isdisjoint(values(test, "path"))
    assert values(dev, "class_id").isdisjoint(values(test, "class_id"))
    assert values(dev, "palm_id").isdisjoint(values(test, "palm_id"))


def test_gallery_probe_closed_set_and_direction():
    split = load_split("tongji_subject_disjoint_s1_to_s2_seed42.json")
    gallery = split["gallery"]
    probe = split["probe"]

    assert values(gallery, "path").isdisjoint(values(probe, "path"))
    assert values(gallery, "class_id") == values(probe, "class_id")
    assert values(gallery, "session") == {"session1"}
    assert values(probe, "session") == {"session2"}
