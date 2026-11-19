"""Lab 4: does synthetic data carry or amplify bias in the real data?

Run from a terminal after Lab 1 (and, if you want the private models too, Lab 3):

    python lab4_fairness.py --data-dir ../lab-1/outputs --extra ../lab-3/outputs_lab3/synthetic_dpgan_eps1.csv

Task 1 compares group sizes and base rates in real and synthetic data.
Task 2 trains classifiers on real and on synthetic data and measures their
fairness on the real holdout set, with fairlearn and with FairX.
Task 3 repeats the analysis for intersections of sex and race.
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from codecarbon import OfflineEmissionsTracker
from fairlearn.metrics import (
    MetricFrame, count, demographic_parity_difference, equalized_odds_difference,
    selection_rate, true_positive_rate,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
CATEGORICAL = [
    "workclass", "education", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country",
]
PROTECTED = ["sex", "race"]
TARGET, POSITIVE = "class", ">50K"


class Encoder:
    """One-hot encoding and scaling, fitted on the real training data.
    With drop_protected=True the classifier does not see sex and race."""

    def __init__(self, real, drop_protected=False):
        self.cat = [c for c in CATEGORICAL if not (drop_protected and c in PROTECTED)]
        self.onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(real[self.cat])
        self.scaler = StandardScaler().fit(real[NUMERIC])

    def __call__(self, df):
        X = np.hstack([self.scaler.transform(df[NUMERIC]), self.onehot.transform(df[self.cat])])
        return X, (df[TARGET] == POSITIVE).astype(int).to_numpy()


def base_rates(datasets):
    """Task 1: share of each group, and share of '>50K' within each group."""
    rows = []
    for name, df in datasets.items():
        positive = df[TARGET] == POSITIVE
        for attr in PROTECTED:
            for group, idx in df.groupby(attr).groups.items():
                rows.append({
                    "data": name, "attribute": attr, "group": group,
                    "share of rows": len(idx) / len(df),
                    "P(>50K | group)": positive.loc[idx].mean(),
                })
    return pd.DataFrame(rows).pivot_table(
        index=["attribute", "group"], columns="data", values=["share of rows", "P(>50K | group)"]
    )


def downstream_fairness(datasets, train, holdout, drop_protected):
    """Task 2: train on each data set, measure accuracy and fairness on the real holdout."""
    encode = Encoder(train, drop_protected)
    X_hold, y_hold = encode(holdout)
    rows, predictions = [], {}
    for name, df in datasets.items():
        X, y = encode(df)
        if len(np.unique(y)) < 2:
            print(f"{name}: only one class in the labels, skipped")
            continue
        model = LogisticRegression(max_iter=2000).fit(X, y)
        proba = model.predict_proba(X_hold)[:, 1]
        pred = (proba >= 0.5).astype(int)
        predictions[name] = pred
        row = {"trained on": name, "accuracy": accuracy_score(y_hold, pred), "AUROC": roc_auc_score(y_hold, proba)}
        for attr in PROTECTED:
            s = holdout[attr]
            row[f"DPD {attr}"] = demographic_parity_difference(y_hold, pred, sensitive_features=s)
            row[f"EOD {attr}"] = equalized_odds_difference(y_hold, pred, sensitive_features=s)
        rows.append(row)
    return pd.DataFrame(rows).set_index("trained on"), predictions, y_hold


def fairx_fairness(datasets, train, holdout):
    """Task 2 with FairX: XGBoost trained on each data set, ratios on the real holdout (sex)."""
    from fairx.metrics import FairnessUtils

    encode = Encoder(train)
    X_hold, y_hold = encode(holdout)
    rows = []
    for name, df in datasets.items():
        X, y = encode(df)
        if len(np.unique(y)) < 2:
            continue
        split = (X, X_hold, y, y_hold, df["sex"].to_numpy(), holdout["sex"].to_numpy())
        rows.append({"trained on": name, **FairnessUtils(split).evaluate_fairness()})
    return pd.DataFrame(rows).set_index("trained on")


def intersectional(predictions, y_hold, holdout):
    """Task 3: selection rate and true positive rate for each sex x race group."""
    frames = []
    for name, pred in predictions.items():
        mf = MetricFrame(
            metrics={"n": count, "selection rate": selection_rate, "TPR": true_positive_rate},
            y_true=y_hold, y_pred=pred, sensitive_features=holdout[["sex", "race"]],
        )
        by_group = mf.by_group.copy()
        by_group.columns = pd.MultiIndex.from_product([[name], by_group.columns])
        frames.append(by_group)
        print(f"{name}: largest gap in selection rate over sex x race groups = "
              f"{mf.difference()['selection rate']:.3f}")
    return pd.concat(frames, axis=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("../lab-1/outputs"))
    parser.add_argument("--extra", type=Path, nargs="*", default=[], help="more synthetic CSV files")
    parser.add_argument("--drop-protected", action="store_true", help="train without sex and race")
    parser.add_argument("--out", type=Path, default=Path("outputs_lab4"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 200)

    train = pd.read_csv(args.data_dir / "adult_train.csv")
    holdout = pd.read_csv(args.data_dir / "adult_holdout.csv")
    datasets = {
        "real": train,
        "CTGAN": pd.read_csv(args.data_dir / "synthetic_ctgan.csv"),
        "TVAE": pd.read_csv(args.data_dir / "synthetic_tvae.csv"),
    }
    for path in args.extra:
        datasets[path.stem.replace("synthetic_", "")] = pd.read_csv(path)

    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE", project_name="lab4-evaluation", output_dir=str(args.out), log_level="error"
    )
    tracker.start()
    start = time.perf_counter()

    rates = base_rates(datasets)
    rates.to_csv(args.out / "base_rates.csv")
    print(rates.round(3).to_string(), "\n")

    fairness, predictions, y_hold = downstream_fairness(datasets, train, holdout, args.drop_protected)
    fairness.to_csv(args.out / "downstream_fairness.csv")
    print(fairness.round(3).to_string(), "\n")

    fx = fairx_fairness(datasets, train, holdout)
    fx.to_csv(args.out / "fairx_fairness.csv")
    print(fx.round(3).to_string(), "\n")

    groups = intersectional(predictions, y_hold, holdout)
    groups.to_csv(args.out / "intersectional.csv")
    print(groups.round(3).to_string())

    seconds = time.perf_counter() - start
    tracker.stop()
    print(f"evaluation took {seconds:.0f} s, {tracker.final_emissions_data.energy_consumed * 1000:.2f} Wh")


if __name__ == "__main__":
    main()
