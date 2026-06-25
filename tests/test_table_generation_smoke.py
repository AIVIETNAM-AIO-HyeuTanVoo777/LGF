from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


METHODS = ["M0", "M1", "M2", "M3", "M4", "M6", "M7"]
DIRECTIONS = ["S1->S2", "S2->S1"]
SEEDS = [42, 2026, 2705]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_make_result_tables_smoke(tmp_path: Path):
    results = tmp_path / "results"
    out = tmp_path / "paper_sections"

    main_rows = []
    for method in METHODS:
        for direction in DIRECTIONS:
            for seed in SEEDS:
                main_rows.append({
                    "method": method,
                    "dataset": "Tongji",
                    "direction": direction,
                    "seed": seed,
                    "rank1": 0.9,
                    "rank5": 0.95,
                    "macro_f1": 0.89,
                    "eer": 0.05,
                    "tar_far_1e_2": 0.85,
                    "tar_far_1e_3": 0.70,
                })
    write_csv(results / "main_tongji_results.csv", main_rows)

    write_csv(results / "classical_reference_results.csv", [{
        "method": "Gabor",
        "dataset": "Tongji",
        "direction": "S1->S2",
        "seed": 42,
        "rank1": 0.8,
        "rank5": 0.9,
        "macro_f1": 0.8,
        "eer": 0.1,
        "tar_far_1e_2": 0.6,
        "tar_far_1e_3": 0.3,
    }])

    write_csv(results / "paired_deltas.csv", [{
        "comparison": "M4_minus_M1",
        "metric": "Rank-1",
        "n": 6,
        "mean_delta_pp": 1.0,
        "sd_delta_pp": 0.5,
        "bootstrap_ci95_low_pp": -0.1,
        "bootstrap_ci95_high_pp": 2.0,
        "exact_sign_flip_p_two_sided": 0.5,
        "interpretation": "diagnostic",
    }])

    write_csv(results / "iitd_secondary_results.csv", [{
        "method": "M1",
        "dataset": "IITD",
        "direction": "within",
        "seed": 42,
        "rank1": 0.95,
        "rank5": 0.99,
        "macro_f1": 0.94,
        "eer": 0.03,
        "tar_far_1e_2": 0.9,
        "tar_far_1e_3": 0.8,
    }])

    result = subprocess.run(
        [sys.executable, "scripts/make_result_tables.py", "--results-dir", str(results), "--out-dir", str(out)],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert (out / "strict_tongji_ablation_table.tex").exists()
    assert (out / "iitd_subject_disjoint_table.tex").exists()
