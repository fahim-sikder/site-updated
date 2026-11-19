"""Lab 1, part A: train CTGAN and TVAE on the Adult data and compare their output.

Run from a terminal:

    python lab1_tabular.py --epochs 100

The script writes the data splits, the synthetic data, the figures and the
CodeCarbon log to the folder given by --out (default: outputs).
"""

import argparse
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # write figures to files, no window needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from codecarbon import OfflineEmissionsTracker
from ctgan import CTGAN, TVAE
from scipy.stats import chi2_contingency
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
CATEGORICAL = [
    "workclass", "education", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country", "class",
]


def load_adult(n_train=5000, n_holdout=5000, seed=0):
    """Load Adult (OpenML data set 1590) and split it into three disjoint parts.

    The same seed gives the same rows in every lab, so the files that this
    script writes can be reused in Labs 2 to 4.
    """
    data = fetch_openml(data_id=1590, as_frame=True, parser="auto").frame
    data = data.drop(columns=["fnlwgt"])  # a census sampling weight, not a personal attribute
    data = data.dropna().reset_index(drop=True)  # 45,222 complete rows remain
    for col in CATEGORICAL:
        data[col] = data[col].astype(str)
    data = data.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    train = data.iloc[:n_train].reset_index(drop=True)
    holdout = data.iloc[n_train:n_train + n_holdout].reset_index(drop=True)
    reference = data.iloc[n_train + n_holdout:n_train + 2 * n_holdout].reset_index(drop=True)
    return train, holdout, reference


def train_model(name, model, train, out):
    """Train one model inside a CodeCarbon tracker and return the synthetic data."""
    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE",
        project_name=f"lab1-{name}",
        output_dir=str(out),
        log_level="error",
    )
    tracker.start()
    start = time.perf_counter()
    model.fit(train, discrete_columns=CATEGORICAL)
    seconds = time.perf_counter() - start
    tracker.stop()
    energy_kwh = tracker.final_emissions_data.energy_consumed
    print(f"{name}: trained in {seconds:.0f} s, {energy_kwh * 1000:.2f} Wh")
    synthetic = model.sample(len(train))
    return synthetic, seconds, energy_kwh


def cramers_v(x, y):
    """Cramér's V between two categorical columns (bias is not corrected)."""
    table = pd.crosstab(x, y)
    if min(table.shape) < 2:
        return 0.0
    chi2 = chi2_contingency(table, correction=False)[0]
    return float(np.sqrt(chi2 / (table.values.sum() * (min(table.shape) - 1))))


def association_matrices(df):
    """Pearson correlation for numeric pairs, Cramér's V for categorical pairs."""
    pearson = df[NUMERIC].corr()
    cramer = pd.DataFrame(index=CATEGORICAL, columns=CATEGORICAL, dtype=float)
    for a in CATEGORICAL:
        for b in CATEGORICAL:
            cramer.loc[a, b] = 1.0 if a == b else cramers_v(df[a], df[b])
    return pearson, cramer


def plot_marginals(real, synth, out):
    columns = ["age", "hours-per-week", "capital-gain", "sex", "race", "education"]
    fig, axes = plt.subplots(len(synth), len(columns), figsize=(4 * len(columns), 3.2 * len(synth)))
    for row, (name, df) in enumerate(synth.items()):
        for col_idx, col in enumerate(columns):
            ax = axes[row, col_idx]
            if col in NUMERIC:
                # capital-gain is zero for most people, so plot log10(1 + value);
                # negative synthetic values are drawn in the bin at 0
                f = (lambda x: np.log10(1 + x.clip(lower=0))) if col == "capital-gain" else (lambda x: x)
                bins = np.histogram_bin_edges(f(real[col]), bins=30)
                ax.hist(f(real[col]), bins=bins, alpha=0.5, density=True, label="real")
                ax.hist(f(df[col]), bins=bins, alpha=0.5, density=True, label=name)
            else:
                shares = pd.DataFrame({
                    "real": real[col].value_counts(normalize=True),
                    name: df[col].value_counts(normalize=True),
                }).fillna(0).sort_values("real", ascending=False).head(8)
                shares.plot.bar(ax=ax, legend=False)
                ax.tick_params(axis="x", labelrotation=60, labelsize=7)
            title = "log10(1 + capital-gain), negatives at 0" if col == "capital-gain" else col
            ax.set_title(f"{title} ({name})", fontsize=9)
        axes[row, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "marginals.png", dpi=120)
    plt.close(fig)


def plot_association_differences(real, synth, out):
    real_p, real_c = association_matrices(real)
    fig, axes = plt.subplots(2, len(synth), figsize=(6 * len(synth), 10))
    summary = {}
    for col_idx, (name, df) in enumerate(synth.items()):
        syn_p, syn_c = association_matrices(df)
        diff_p = (real_p - syn_p).abs()
        diff_c = (real_c - syn_c).abs()
        summary[name] = {
            "mean |diff| Pearson (numeric)": diff_p.values[np.triu_indices(len(NUMERIC), 1)].mean(),
            "mean |diff| Cramer's V (categorical)": diff_c.values[np.triu_indices(len(CATEGORICAL), 1)].mean(),
        }
        for row, (diff, labels) in enumerate([(diff_p, NUMERIC), (diff_c, CATEGORICAL)]):
            ax = axes[row, col_idx]
            im = ax.imshow(diff.values.astype(float), vmin=0, vmax=0.5, cmap="viridis")
            ax.set_xticks(range(len(labels)), labels, rotation=90, fontsize=8)
            ax.set_yticks(range(len(labels)), labels, fontsize=8)
            ax.set_title(f"{name}: |real - synthetic|", fontsize=10)
            fig.colorbar(im, ax=ax, shrink=0.7)
    fig.tight_layout()
    fig.savefig(out / "association_differences.png", dpi=120)
    plt.close(fig)
    return pd.DataFrame(summary).T


def plot_pca(real, synth, out, n_points=2000, seed=0):
    """Fit PCA on the encoded real data and project real and synthetic rows."""
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(real[CATEGORICAL])
    scaler = StandardScaler().fit(real[NUMERIC])

    def encode(df):
        return np.hstack([scaler.transform(df[NUMERIC]), encoder.transform(df[CATEGORICAL])])

    pca = PCA(n_components=2).fit(encode(real))
    real_2d = pca.transform(encode(real.sample(n_points, random_state=seed)))
    fig, axes = plt.subplots(1, len(synth), figsize=(6 * len(synth), 5))
    for ax, (name, df) in zip(np.atleast_1d(axes), synth.items()):
        syn_2d = pca.transform(encode(df.sample(n_points, random_state=seed)))
        ax.scatter(real_2d[:, 0], real_2d[:, 1], s=4, alpha=0.4, label="real")
        ax.scatter(syn_2d[:, 0], syn_2d[:, 1], s=4, alpha=0.4, label=name)
        ax.set_title(f"PCA fitted on real data: {name}")
        ax.legend()
    fig.tight_layout()
    fig.savefig(out / "pca.png", dpi=120)
    plt.close(fig)


def education_consistency(df, mapping):
    """Share of rows where education and education-num agree as they do in the real data."""
    return float((df["education"].map(mapping) == df["education-num"]).mean())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--n-train", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    train, holdout, reference = load_adult(n_train=args.n_train, seed=args.seed)
    train.to_csv(args.out / "adult_train.csv", index=False)
    holdout.to_csv(args.out / "adult_holdout.csv", index=False)
    reference.to_csv(args.out / "adult_reference.csv", index=False)
    print(f"train {train.shape}, holdout {holdout.shape}, reference {reference.shape}")

    # In the real data each education level has exactly one education-num value.
    education_map = train.groupby("education")["education-num"].first().to_dict()

    models = {
        "CTGAN": CTGAN(epochs=args.epochs, verbose=False),
        "TVAE": TVAE(epochs=args.epochs),
    }
    synth, rows = {}, []
    for name, model in models.items():
        model.set_random_state(args.seed)
        df, seconds, energy = train_model(name, model, train, args.out)
        df.to_csv(args.out / f"synthetic_{name.lower()}.csv", index=False)
        synth[name] = df
        rows.append({"model": name, "train seconds": round(seconds), "energy Wh": round(energy * 1000, 2)})

    plot_marginals(train, synth, args.out)
    summary = plot_association_differences(train, synth, args.out)
    plot_pca(train, synth, args.out)
    summary["education matches education-num"] = [education_consistency(df, education_map) for df in synth.values()]
    summary["share of '>50K'"] = [(df["class"] == ">50K").mean() for df in synth.values()]
    summary["capital-gain = 0"] = [(df["capital-gain"] == 0).mean() for df in synth.values()]
    summary["capital-gain < 0"] = [(df["capital-gain"] < 0).mean() for df in synth.values()]
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"real: share of '>50K' = {(train['class'] == '>50K').mean():.3f}, "
          f"capital-gain = 0: {(train['capital-gain'] == 0).mean():.3f}, "
          f"capital-gain < 0: {(train['capital-gain'] < 0).mean():.3f}")
    print(summary.round(3).T.to_string())


if __name__ == "__main__":
    main()
