import argparse
import csv
from pathlib import Path
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=str, default="docs/results")
    parser.add_argument("--out-dir", type=str, default="paper/sections")
    return parser.parse_args()

def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def latex_escape_text(s):
    s = str(s)
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    return ''.join(replacements.get(ch, ch) for ch in s)

def format_stat(mean_val, std_val, is_eer=False):
    # Metrics are in range [0, 1] in raw results, convert to percent
    m = mean_val * 100.0
    s = std_val * 100.0
    return f"${m:.2f} \\pm {s:.2f}$"

def format_delta(mean_val, std_val):
    # Deltas are already in percentage points in the CSV
    return f"${mean_val:+.2f} \\pm {std_val:.2f}$"

def main():
    args = parse_args()
    results_dir = Path(args.results_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Method descriptions mapping for the tables
    method_desc = {
        "M0": "ResNet18 + CE",
        "M1": "ResNet18 + CE + SupCon",
        "M2": "ResNet18 + ArcFace",
        "M3": "ResNet18 + CosFace",
        "M4": "ResNet18 + BNNeck + CE",
        "M6": "ResNet18 + BNNeck + ArcFace",
        "M7": "ResNet18 + BNNeck + ArcFace + light SupCon",
        "Gabor": "Fixed Gabor reference"
    }
    
    # Method order in paper tables
    method_order = ["M0", "M1", "M2", "M3", "M4", "M6", "M7"]
    
    # 1. Regenerate strict_tongji_ablation_table.tex
    main_tongji = load_csv(results_dir / "main_tongji_results.csv")
    
    # Group by method
    method_groups = {m: [] for m in method_order}
    for r in main_tongji:
        m = r["method"]
        if m in method_groups:
            method_groups[m].append(r)
            
    # Load Gabor results
    gabor_results = load_csv(results_dir / "classical_reference_results.csv")
    gabor_list = []
    for r in gabor_results:
        gabor_list.append(r)
        
    # Write main Tongji results table
    ablation_tex = out_dir / "strict_tongji_ablation_table.tex"
    with open(ablation_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\scriptsize\n")
        f.write("\\setlength{\\tabcolsep}{3pt}\n")
        f.write("\\caption{Strict Tongji palm-class-disjoint ablation summary over two session directions and three seeds per method. ")
        f.write("Values are mean $\\pm$ standard deviation in percent over six seed-direction units, without pre-averaging directions. ")
        f.write("Lower EER is better; higher values are better for all other metrics. TAR@FAR is computed using the conservative empirical-FAR rule.}\n")
        f.write("\\label{tab:strict_tongji_ablation}\n")
        f.write("\\resizebox{\\textwidth}{!}{\n")
        f.write("\\begin{tabular}{llcccccc}\n")
        f.write("\\toprule\n")
        f.write("Method & Description & Rank-1 (\\%) & Rank-5 (\\%) & Macro-F1 (\\%) & EER (\\%) & TAR@FAR=$10^{-2}$ & TAR@FAR=$10^{-3}$ \\\\\n")
        f.write("\\midrule\n")
        
        # Write Gabor first or as part of the list?
        # In the original, Gabor was in palmprint_specific_baseline_table.tex. Let's keep it separate or append it.
        # Let's write the deep learning methods first:
        for m_id in method_order:
            runs = method_groups[m_id]
            if not runs:
                continue
            r1s = [float(r["rank1"]) for r in runs]
            r5s = [float(r["rank5"]) for r in runs]
            f1s = [float(r["macro_f1"]) for r in runs]
            eers = [float(r["eer"]) for r in runs]
            tar2s = [float(r["tar_far_1e_2"]) for r in runs]
            tar3s = [float(r["tar_far_1e_3"]) for r in runs]
            
            escaped_m_id = latex_escape_text(m_id)
            escaped_desc = latex_escape_text(method_desc[m_id])
            f.write(f"{escaped_m_id} & {escaped_desc} & ")
            f.write(f"{format_stat(np.mean(r1s), np.std(r1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(r5s), np.std(r5s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(f1s), np.std(f1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(eers), np.std(eers, ddof=1), True)} & ")
            f.write(f"{format_stat(np.mean(tar2s), np.std(tar2s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(tar3s), np.std(tar3s, ddof=1))} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}%\n")
        f.write("}\n")
        f.write("\\end{table*}\n")
    print(f"Wrote {ablation_tex}")
    
    # 2. Regenerate strict_tongji_ablation_by_direction_table.tex
    ablation_dir_tex = out_dir / "strict_tongji_ablation_by_direction_table.tex"
    with open(ablation_dir_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\scriptsize\n")
        f.write("\\caption{Direction-specific strict Tongji ablation metrics. Values are mean $\\pm$ standard deviation in percent over three seeds per direction.}\n")
        f.write("\\label{tab:strict_tongji_ablation_by_direction}\n")
        f.write("\\resizebox{\\textwidth}{!}{\n")
        f.write("\\begin{tabular}{llccccccc}\n")
        f.write("\\toprule\n")
        f.write("Method & Description & Direction & Rank-1 (\\%) & Rank-5 (\\%) & Macro-F1 (\\%) & EER (\\%) & TAR@FAR=$10^{-2}$ & TAR@FAR=$10^{-3}$ \\\\\n")
        
        for m_id in method_order:
            runs = method_groups[m_id]
            if not runs:
                continue
                
            f.write("\\midrule\n")
            for direction in ["S1->S2", "S2->S1"]:
                dir_runs = [r for r in runs if r["direction"] == direction]
                if not dir_runs:
                    continue
                r1s = [float(r["rank1"]) for r in dir_runs]
                r5s = [float(r["rank5"]) for r in dir_runs]
                f1s = [float(r["macro_f1"]) for r in dir_runs]
                eers = [float(r["eer"]) for r in dir_runs]
                tar2s = [float(r["tar_far_1e_2"]) for r in dir_runs]
                tar3s = [float(r["tar_far_1e_3"]) for r in dir_runs]
                
                # Format direction for LaTeX table
                dir_lbl = "S1$\\rightarrow$S2" if direction == "S1->S2" else "S2$\\rightarrow$S1"
                
                escaped_m_id = latex_escape_text(m_id)
                escaped_desc = latex_escape_text(method_desc[m_id])
                f.write(f"{escaped_m_id} & {escaped_desc} & {dir_lbl} & ")
                f.write(f"{format_stat(np.mean(r1s), np.std(r1s, ddof=1))} & ")
                f.write(f"{format_stat(np.mean(r5s), np.std(r5s, ddof=1))} & ")
                f.write(f"{format_stat(np.mean(f1s), np.std(f1s, ddof=1))} & ")
                f.write(f"{format_stat(np.mean(eers), np.std(eers, ddof=1), True)} & ")
                f.write(f"{format_stat(np.mean(tar2s), np.std(tar2s, ddof=1))} & ")
                f.write(f"{format_stat(np.mean(tar3s), np.std(tar3s, ddof=1))} \\\\\n")
                
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}%\n")
        f.write("}\n")
        f.write("\\end{table*}\n")
    print(f"Wrote {ablation_dir_tex}")
    
    # 3. Regenerate paired_statistics_component_ablation_table.tex
    paired_deltas = load_csv(results_dir / "paired_deltas.csv")
    paired_tex = out_dir / "paired_statistics_component_ablation_table.tex"
    with open(paired_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\scriptsize\n")
        f.write("\\caption{Paired delta statistics over six matched seed-direction units on strict Tongji. ")
        f.write("Deltas are reported in percentage points (PP). CI95 is the 95\\% percentile bootstrap confidence interval. ")
        f.write("p-value is from the exact sign-flip permutation test. positive Rank/TAR deltas favor the first method.}\n")
        f.write("\\label{tab:paired_statistics_component_ablation}\n")
        f.write("\\begin{tabular}{llccccc}\n")
        f.write("\\toprule\n")
        f.write("Comparison & Metric & Mean Delta (PP) & Std Delta (PP) & CI95 Low & CI95 High & Exact Sign-Flip p \\\\\n")
        
        last_comp = ""
        for r in paired_deltas:
            comp = r["comparison"]
            if comp != last_comp:
                f.write("\\midrule\n")
                last_comp = comp
                
            comp_lbl = comp.replace("_minus_", " $-$ ")
            escaped_metric = latex_escape_text(r['metric'])
            f.write(f"{comp_lbl} & {escaped_metric} & ")
            f.write(f"${float(r['mean_delta_pp']):+.2f}$ & ")
            f.write(f"${float(r['sd_delta_pp']):.2f}$ & ")
            f.write(f"${float(r['bootstrap_ci95_low_pp']):+.2f}$ & ")
            f.write(f"${float(r['bootstrap_ci95_high_pp']):+.2f}$ & ")
            f.write(f"${float(r['exact_sign_flip_p_two_sided']):.5f}$ \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}%\n")
        f.write("\\end{table*}\n")
    print(f"Wrote {paired_tex}")
    
    # 4. Regenerate iitd_subject_disjoint_table.tex
    iitd_results = load_csv(results_dir / "iitd_secondary_results.csv")
    iitd_groups = {}
    for r in iitd_results:
        m = r["method"]
        if m not in iitd_groups:
            iitd_groups[m] = []
        iitd_groups[m].append(r)
        
    iitd_tex = out_dir / "iitd_subject_disjoint_table.tex"
    with open(iitd_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table}[t]\n")
        f.write("\\centering\n")
        f.write("\\caption{Secondary within-session evaluation on the corrected IITD split. "
                "Values are mean $\\pm$ standard deviation in percent over three seeds. "
                "This validation remains within-session and is not cross-session evidence. "
                "TAR columns denote TAR@FAR at the indicated FAR target.}\n")
        f.write("\\label{tab:iitd_subject_disjoint}\n")
        f.write("\\small\n")
        f.write("\\setlength{\\tabcolsep}{4pt}\n")
        f.write("\\resizebox{\\linewidth}{!}{%\n")
        f.write("\\begin{tabular}{lcccccc}\n")
        f.write("\\toprule\n")
        f.write("Method & Rank-1 (\\%) & Rank-5 (\\%) & Macro-F1 (\\%) & EER (\\%) & TAR@$10^{-2}$ & TAR@$10^{-3}$ \\\\\n")
        f.write("\\midrule\n")
        
        for m_id in ["M1", "M6"]:
            runs = iitd_groups.get(m_id, [])
            if not runs:
                continue
            r1s = [float(r["rank1"]) for r in runs]
            r5s = [float(r["rank5"]) for r in runs]
            f1s = [float(r["macro_f1"]) for r in runs]
            eers = [float(r["eer"]) for r in runs]
            tar2s = [float(r["tar_far_1e_2"]) for r in runs]
            tar3s = [float(r["tar_far_1e_3"]) for r in runs]
            
            escaped_m_id = latex_escape_text(m_id)
            f.write(f"{escaped_m_id} & ")
            f.write(f"{format_stat(np.mean(r1s), np.std(r1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(r5s), np.std(r5s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(f1s), np.std(f1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(eers), np.std(eers, ddof=1), True)} & ")
            f.write(f"{format_stat(np.mean(tar2s), np.std(tar2s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(tar3s), np.std(tar3s, ddof=1))} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}%\n")
        f.write("}\n")
        f.write("\\end{table}\n")
    print(f"Wrote {iitd_tex}")
    
    # 5. Regenerate palmprint_specific_baseline_table.tex
    palm_tex = out_dir / "palmprint_specific_baseline_table.tex"
    with open(palm_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table}[t]\n")
        f.write("\\centering\n")
        f.write("\\caption{Gabor reference baseline performance on the strict Tongji split. "
                "Values are mean $\\pm$ standard deviation in percent over six seed-direction units. "
                "TAR columns denote TAR@FAR at the indicated FAR target.}\n")
        f.write("\\label{tab:palmprint_specific_baseline}\n")
        f.write("\\small\n")
        f.write("\\setlength{\\tabcolsep}{4pt}\n")
        f.write("\\resizebox{\\linewidth}{!}{%\n")
        f.write("\\begin{tabular}{lcccccc}\n")
        f.write("\\toprule\n")
        f.write("Method & Rank-1 (\\%) & Rank-5 (\\%) & Macro-F1 (\\%) & EER (\\%) & TAR@$10^{-2}$ & TAR@$10^{-3}$ \\\\\n")
        f.write("\\midrule\n")

        runs = gabor_list
        if runs:
            r1s = [float(r["rank1"]) for r in runs]
            r5s = [float(r["rank5"]) for r in runs]
            f1s = [float(r["macro_f1"]) for r in runs]
            eers = [float(r["eer"]) for r in runs]
            tar2s = [float(r["tar_far_1e_2"]) for r in runs]
            tar3s = [float(r["tar_far_1e_3"]) for r in runs]

            f.write("Gabor & ")
            f.write(f"{format_stat(np.mean(r1s), np.std(r1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(r5s), np.std(r5s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(f1s), np.std(f1s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(eers), np.std(eers, ddof=1), True)} & ")
            f.write(f"{format_stat(np.mean(tar2s), np.std(tar2s, ddof=1))} & ")
            f.write(f"{format_stat(np.mean(tar3s), np.std(tar3s, ddof=1))} \\\\\n")

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}%\n")
        f.write("}\n")
        f.write("\\end{table}\n")
    print(f"Wrote {palm_tex}")

    return 0

if __name__ == "__main__":
    main()
