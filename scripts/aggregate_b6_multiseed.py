import json
import math
import re
import shutil
import sys
from pathlib import Path


RESULTS_DIR = Path("docs/results")
METRICS = [
    "rank1",
    "rank5",
    "macro_f1",
    "eer",
    "tar_far_1e_2",
    "tar_far_1e_3",
    "time_ms",
    "params_m",
    "flops_g",
]
PERFORMANCE_METRICS = {
    "rank1",
    "rank5",
    "macro_f1",
    "eer",
    "tar_far_1e_2",
    "tar_far_1e_3",
}
METHOD_RUNS = {
    "B1": {
        "S1->S2": {
            42: "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4",
            2026: "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2026",
            2705: "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2705",
        },
        "S2->S1": {
            42: "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4",
            2026: "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2026",
            2705: "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2705",
        },
    },
    "B2": {
        "S1->S2": {
            42: "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4",
            2026: "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2026",
            2705: "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2705",
        },
        "S2->S1": {
            42: "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4",
            2026: "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2026",
            2705: "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2705",
        },
    },
    "B6": {
        "S1->S2": {
            42: "b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed42",
            2026: "b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026",
            2705: "b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705",
        },
        "S2->S1": {
            42: "b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed42",
            2026: "b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026",
            2705: "b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705",
        },
    },
}


def normalize_key(key):
    return re.sub(r"[^a-z0-9]+", "", str(key).lower())


KEY_ALIASES = {
    "rank1": {
        "rank1",
        "rank01",
        "rank1accuracy",
        "top1",
        "top1accuracy",
    },
    "rank5": {
        "rank5",
        "rank05",
        "rank5accuracy",
        "top5",
        "top5accuracy",
    },
    "macro_f1": {
        "macrof1",
        "f1macro",
        "macroaveragef1",
    },
    "eer": {"eer", "equalerrorrate"},
    "tar_far_1e_2": {
        "tarfar1e2",
        "tarfar001",
        "taratfar1e2",
        "taratfar001",
    },
    "tar_far_1e_3": {
        "tarfar1e3",
        "tarfar0001",
        "taratfar1e3",
        "taratfar0001",
    },
    "params_m": {
        "paramsm",
        "parametersm",
        "totalparamsm",
        "totalparametersm",
        "params",
        "totalparams",
        "totalparameters",
    },
    "flops_g": {
        "flopsg",
        "gflops",
        "estimatedflopsg",
        "estimatedflops",
        "flops",
    },
    "time_ms": {
        "averageinferencetimems",
        "avginferencetimems",
        "inferencetimems",
        "latencyms",
        "timems",
    },
}


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def json_metric(data, metric):
    aliases = KEY_ALIASES[metric]
    for key, value in data.items():
        if normalize_key(key) in aliases:
            return float(value)
    return None


def as_percent(value):
    if value is None:
        return None
    return value * 100.0 if abs(value) <= 1.0000001 else value


def as_params_m(value):
    if value is None:
        return None
    return value / 1_000_000.0 if value > 100_000 else value


def as_flops_g(value):
    if value is None:
        return None
    return value / 1_000_000_000.0 if value > 100_000 else value


def parse_md_metrics(path):
    if path is None or not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    parsed = {}

    patterns = {
        "params_m": [
            r"Total Parameters\*\*:\s*([\d,]+)",
            r"Total Parameters\*\*:\s*[\d,]+\s*\(([\d.]+)\s*M\)",
            r"Params\*\*:\s*([\d.]+)\s*M",
        ],
        "flops_g": [
            r"Estimated FLOPs\*\*:\s*([\d.]+)\s*GFLOPs",
            r"FLOPs\*\*:\s*([\d.]+)\s*G",
        ],
        "time_ms": [
            r"Average Inference Time.*?:\s*([\d.]+)\s*ms",
            r"Latency.*?:\s*([\d.]+)\s*ms",
        ],
    }
    for metric, pats in patterns.items():
        for pat in pats:
            match = re.search(pat, text, flags=re.IGNORECASE)
            if match:
                value = float(match.group(1).replace(",", ""))
                if metric == "params_m" and value > 100_000:
                    value = value / 1_000_000.0
                parsed[metric] = value
                break

    table_patterns = {
        "rank1": r"\|\s*\*\*Rank-1\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
        "rank5": r"\|\s*\*\*Rank-5\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
        "macro_f1": r"\|\s*\*\*Macro-F1\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
        "eer": r"\|\s*\*\*EER\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
        "tar_far_1e_2": r"\|\s*\*\*TAR@FAR=1e-2\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
        "tar_far_1e_3": r"\|\s*\*\*TAR@FAR=1e-3\*\*\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)%",
    }
    for metric, pat in table_patterns.items():
        match = re.search(pat, text, flags=re.IGNORECASE)
        if match:
            parsed[metric] = float(match.group(2))

    return parsed


def docs_paths(exp_name):
    return {
        "json": RESULTS_DIR / f"{exp_name}_metrics.json",
        "md": RESULTS_DIR / f"{exp_name}_metrics.md",
        "yaml": RESULTS_DIR / f"{exp_name}.yaml",
    }


def experiment_paths(exp_name):
    return {
        "json": Path("experiments") / exp_name / "metrics.json",
        "md": Path("experiments") / exp_name / "metrics.md",
        "yaml": Path("configs") / f"{exp_name}.yaml",
    }


def resolve_run_files(method, exp_name):
    docs = docs_paths(exp_name)
    exp = experiment_paths(exp_name)

    if docs["json"].exists():
        json_path = docs["json"]
    elif exp["json"].exists():
        json_path = exp["json"]
    else:
        fail(f"Missing metrics file for {method} {exp_name}. Tried: {docs['json']} and {exp['json']}")

    # Prefer docs resource/config sidecars when present, but allow fallback to
    # experiments/configs because older B6 runs may not have been copied yet.
    md_path = docs["md"] if docs["md"].exists() else (exp["md"] if exp["md"].exists() else None)
    yaml_path = docs["yaml"] if docs["yaml"].exists() else (exp["yaml"] if exp["yaml"].exists() else None)
    return json_path, md_path, yaml_path


def extract_run(method, protocol, seed, exp_name):
    json_path, md_path, yaml_path = resolve_run_files(method, exp_name)
    data = load_json(json_path)
    md_metrics = parse_md_metrics(md_path)

    metrics = {}
    missing = []
    for metric in METRICS:
        value = json_metric(data, metric)
        if value is None:
            value = md_metrics.get(metric)
        if value is None:
            missing.append(metric)
            continue
        if metric in PERFORMANCE_METRICS:
            value = as_percent(value)
        elif metric == "params_m":
            value = as_params_m(value)
        elif metric == "flops_g":
            value = as_flops_g(value)
        metrics[metric] = value

    if missing:
        fail(
            "Missing required metrics "
            f"{missing} for {method} {protocol} seed {seed}. "
            f"metrics_json={json_path}, metrics_md={md_path or 'MISSING'}"
        )

    return {
        "method": method,
        "protocol": protocol,
        "seed": seed,
        "experiment_name": exp_name,
        "metrics_source_json": json_path.as_posix(),
        "metrics_source_md": md_path.as_posix() if md_path else "",
        "config_source": yaml_path.as_posix() if yaml_path else "",
        **metrics,
    }


def copy_b6_to_docs(runs):
    copied = []
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for run in runs:
        if run["method"] != "B6":
            continue
        exp_name = run["experiment_name"]
        source_json = Path(run["metrics_source_json"])
        source_md = Path(run["metrics_source_md"]) if run["metrics_source_md"] else None
        source_yaml = Path(run["config_source"]) if run["config_source"] else None
        dest = docs_paths(exp_name)

        if not dest["json"].exists() and source_json.exists():
            shutil.copy(source_json, dest["json"])
            copied.append((source_json.as_posix(), dest["json"].as_posix()))
        if source_md and source_md.exists() and not dest["md"].exists():
            shutil.copy(source_md, dest["md"])
            copied.append((source_md.as_posix(), dest["md"].as_posix()))
        if source_yaml and source_yaml.exists() and not dest["yaml"].exists():
            shutil.copy(source_yaml, dest["yaml"])
            copied.append((source_yaml.as_posix(), dest["yaml"].as_posix()))
    return copied


def stats(values):
    n = len(values)
    mean = sum(values) / n
    if n > 1:
        var = sum((v - mean) ** 2 for v in values) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0
    return {
        "mean": mean,
        "std": std,
        "min": min(values),
        "max": max(values),
        "n": n,
    }


def aggregate_runs(runs):
    aggregates = {}
    for method in METHOD_RUNS:
        aggregates[method] = {}
        method_runs = [r for r in runs if r["method"] == method]
        for protocol in ["S1->S2", "S2->S1"]:
            protocol_runs = [r for r in method_runs if r["protocol"] == protocol]
            if len(protocol_runs) != 3:
                fail(f"Expected 3 runs for {method} {protocol}, found {len(protocol_runs)}")
            aggregates[method][protocol] = {
                metric: stats([r[metric] for r in protocol_runs])
                for metric in METRICS
            }

        bidir_runs = []
        for seed in [42, 2026, 2705]:
            left = next(r for r in method_runs if r["protocol"] == "S1->S2" and r["seed"] == seed)
            right = next(r for r in method_runs if r["protocol"] == "S2->S1" and r["seed"] == seed)
            bidir = {"method": method, "protocol": "Bidirectional Average", "seed": seed}
            for metric in METRICS:
                bidir[metric] = (left[metric] + right[metric]) / 2.0
            bidir_runs.append(bidir)
        aggregates[method]["Bidirectional Average"] = {
            metric: stats([r[metric] for r in bidir_runs])
            for metric in METRICS
        }
    return aggregates


def bidir_mean(aggregates, method, metric):
    return aggregates[method]["Bidirectional Average"][metric]["mean"]


def comparison(aggregates, left_method, right_method):
    return {
        metric: bidir_mean(aggregates, left_method, metric) - bidir_mean(aggregates, right_method, metric)
        for metric in METRICS
    }


def decide(delta_b6_b1):
    rank_delta = delta_b6_b1["rank1"]
    tar_delta = delta_b6_b1["tar_far_1e_3"]
    eer_delta = delta_b6_b1["eer"]
    time_delta = delta_b6_b1["time_ms"]

    if rank_delta >= 1.0 and tar_delta >= 2.0 and eer_delta <= -0.5:
        status = "STRONG_GO"
        reason = (
            f"B6 strongly improves B1: Rank-1 {rank_delta:+.2f} pp, "
            f"TAR@FAR=1e-3 {tar_delta:+.2f} pp, EER {eer_delta:+.2f} pp, "
            f"latency {time_delta:+.2f} ms."
        )
    elif rank_delta >= 0.5 or tar_delta >= 1.0 or eer_delta <= -0.2:
        status = "GO"
        reason = (
            f"B6 meets GO threshold vs B1: Rank-1 {rank_delta:+.2f} pp, "
            f"TAR@FAR=1e-3 {tar_delta:+.2f} pp, EER {eer_delta:+.2f} pp, "
            f"latency {time_delta:+.2f} ms."
        )
    elif rank_delta > 0.0 or tar_delta > 0.0 or eer_delta < 0.0:
        status = "WEAK"
        reason = (
            f"B6 is directionally better on at least one key metric but below GO threshold: "
            f"Rank-1 {rank_delta:+.2f} pp, TAR@FAR=1e-3 {tar_delta:+.2f} pp, "
            f"EER {eer_delta:+.2f} pp, latency {time_delta:+.2f} ms."
        )
    else:
        status = "NO_GO"
        reason = (
            f"B6 does not improve B1 on the key bidirectional decision metrics: "
            f"Rank-1 {rank_delta:+.2f} pp, TAR@FAR=1e-3 {tar_delta:+.2f} pp, "
            f"EER {eer_delta:+.2f} pp, latency {time_delta:+.2f} ms."
        )
    return {"status": status, "best_method": "B6", "reason": reason}


def fmt(value, suffix=""):
    return f"{value:.2f}{suffix}"


def fmt_stat(aggregate_metric, suffix=""):
    return f"{aggregate_metric['mean']:.2f}{suffix} +/- {aggregate_metric['std']:.2f}{suffix}"


def raw_table(runs):
    lines = [
        "| Method | Protocol | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in sorted(runs, key=lambda r: (r["method"], r["protocol"], r["seed"])):
        lines.append(
            f"| {run['method']} | {run['protocol']} | {run['seed']} | "
            f"{fmt(run['rank1'], '%')} | {fmt(run['rank5'], '%')} | {fmt(run['macro_f1'], '%')} | "
            f"{fmt(run['eer'], '%')} | {fmt(run['tar_far_1e_2'], '%')} | {fmt(run['tar_far_1e_3'], '%')} | "
            f"{fmt(run['time_ms'], ' ms')} | {fmt(run['params_m'], 'M')} | {fmt(run['flops_g'], 'G')} |"
        )
    return "\n".join(lines)


def aggregate_table(aggregates):
    lines = [
        "| Method | Protocol | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method in ["B1", "B2", "B6"]:
        for protocol in ["S1->S2", "S2->S1", "Bidirectional Average"]:
            agg = aggregates[method][protocol]
            lines.append(
                f"| {method} | {protocol} | "
                f"{fmt_stat(agg['rank1'], '%')} | {fmt_stat(agg['rank5'], '%')} | "
                f"{fmt_stat(agg['macro_f1'], '%')} | {fmt_stat(agg['eer'], '%')} | "
                f"{fmt_stat(agg['tar_far_1e_2'], '%')} | {fmt_stat(agg['tar_far_1e_3'], '%')} | "
                f"{fmt_stat(agg['time_ms'], ' ms')} | {fmt_stat(agg['params_m'], 'M')} | "
                f"{fmt_stat(agg['flops_g'], 'G')} |"
            )
    return "\n".join(lines)


def comparison_table(comparisons):
    lines = [
        "| Comparison | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@1e-2 | Delta TAR@1e-3 | Delta Time | Delta Params | Delta FLOPs |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    names = {"B6_minus_B1": "B6 - B1", "B6_minus_B2": "B6 - B2"}
    for key in ["B6_minus_B1", "B6_minus_B2"]:
        comp = comparisons[key]
        lines.append(
            f"| {names[key]} | {comp['rank1']:+.2f} pp | {comp['rank5']:+.2f} pp | "
            f"{comp['macro_f1']:+.2f} pp | {comp['eer']:+.2f} pp | "
            f"{comp['tar_far_1e_2']:+.2f} pp | {comp['tar_far_1e_3']:+.2f} pp | "
            f"{comp['time_ms']:+.2f} ms | {comp['params_m']:+.2f}M | {comp['flops_g']:+.2f}G |"
        )
    return "\n".join(lines)


def write_markdown(runs, aggregates, comparisons, decision, copied):
    b6_b1 = comparisons["B6_minus_B1"]
    if decision["status"] in {"STRONG_GO", "GO"}:
        safe_claim = (
            "BNNeck + ArcFace improves cross-session palmprint verification over the "
            "ResNet18 + CE + SupCon baseline under multi-seed Tongji evaluation."
        )
    else:
        safe_claim = (
            "BNNeck + ArcFace is not sufficiently better than the current B1 baseline "
            "under multi-seed Tongji evaluation."
        )

    if decision["status"] == "STRONG_GO":
        paper_direction = (
            "- Recommend write method paper.\n"
            "- Tentative title: \"Margin-Aware BNNeck Embeddings for Cross-Session Palmprint Recognition\""
        )
    elif decision["status"] == "GO":
        paper_direction = (
            "- Recommend add one more validation: IITD B6 + optional session-robust ablation.\n"
            "- Paper possible, but avoid overclaim."
        )
    else:
        paper_direction = "- Recommend move to session-robust metric learning phase."

    copied_section = "\n".join(f"- `{src}` -> `{dst}`" for src, dst in copied) if copied else "- No B6 files needed copying."

    md = f"""# B6 Multi-Seed Tongji Summary

## 1. Scope

- Methods: B1, B2, B6
- Seeds: 42, 2026, 2705
- Protocols: Tongji S1->S2, S2->S1
- B6 = ResNet18 + BNNeck + ArcFace
- No retraining/evaluation done by this aggregate script.
- B6 sidecar copies performed by this script, if needed:
{copied_section}

## 2. Raw Per-Run Metrics

{raw_table(runs)}

## 3. Aggregated Mean +/- Std

{aggregate_table(aggregates)}

## 4. Direct Comparison

{comparison_table(comparisons)}

## 5. Claim Decision

Decision: `{decision['status']}`

Reason: {decision['reason']}

- B6 vs B1 Rank-1 delta: {b6_b1['rank1']:+.2f} pp
- B6 vs B1 TAR@FAR=1e-3 delta: {b6_b1['tar_far_1e_3']:+.2f} pp
- B6 vs B1 EER delta: {b6_b1['eer']:+.2f} pp
- B6 latency overhead vs B1: {b6_b1['time_ms']:+.2f} ms

Safe claim:

{safe_claim}

## 6. Paper Direction

{paper_direction}
"""
    (RESULTS_DIR / "b6_multiseed_summary.md").write_text(md, encoding="utf-8")


def main():
    runs = []
    for method, protocols in METHOD_RUNS.items():
        for protocol, seed_map in protocols.items():
            for seed, exp_name in seed_map.items():
                runs.append(extract_run(method, protocol, seed, exp_name))

    copied = copy_b6_to_docs(runs)
    aggregates = aggregate_runs(runs)
    comparisons = {
        "B6_minus_B1": comparison(aggregates, "B6", "B1"),
        "B6_minus_B2": comparison(aggregates, "B6", "B2"),
    }
    decision = decide(comparisons["B6_minus_B1"])

    summary = {
        "runs": runs,
        "aggregates": aggregates,
        "comparisons": comparisons,
        "decision": decision,
        "copied_b6_files": [{"source": src, "destination": dst} for src, dst in copied],
        "units": {
            "rank1": "percent",
            "rank5": "percent",
            "macro_f1": "percent",
            "eer": "percent",
            "tar_far_1e_2": "percent",
            "tar_far_1e_3": "percent",
            "time_ms": "milliseconds",
            "params_m": "million parameters",
            "flops_g": "GFLOPs",
        },
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_DIR / "b6_multiseed_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    write_markdown(runs, aggregates, comparisons, decision, copied)

    print(f"Wrote {RESULTS_DIR / 'b6_multiseed_summary.json'}")
    print(f"Wrote {RESULTS_DIR / 'b6_multiseed_summary.md'}")
    print(f"Decision: {decision['status']}")
    print(decision["reason"])


if __name__ == "__main__":
    main()
