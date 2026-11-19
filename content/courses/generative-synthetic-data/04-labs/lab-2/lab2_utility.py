"""Lab 2: evaluate the utility and fidelity of synthetic Adult data.

Run from a terminal after Lab 1, pointing --data-dir at the Lab 1 output folder:

    python lab2_utility.py --data-dir ../lab-1/outputs

The script compares four synthetic data sets with the real training data:
CTGAN and TVAE from Lab 1, and two reference cases that the script builds:
"copy" (the training rows themselves) and "marginals" (each column sampled
independently from the real training data).
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from codecarbon import OfflineEmissionsTracker
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
CATEGORICAL = [
    "workclass", "education", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country",
]
TARGET, POSITIVE = "class", ">50K"


class Encoder:
    """One-hot encoding and scaling, fitted on the real training data only."""

    def __init__(self, real):
        self.onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(real[CATEGORICAL])
        self.scaler = StandardScaler().fit(real[NUMERIC])

    def __call__(self, df):
        X = np.hstack([self.scaler.transform(df[NUMERIC]), self.onehot.transform(df[CATEGORICAL])])
        y = (df[TARGET] == POSITIVE).astype(int).to_numpy()
        return X, y


def classifiers(seed):
    return {
        "logistic regression": LogisticRegression(max_iter=2000),
        "random forest": RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=seed, n_jobs=-1),
    }


def scores(model, X, y):
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= 0.5).astype(int)
    return {"AUROC": roc_auc_score(y, proba), "accuracy": accuracy_score(y, pred), "F1": f1_score(y, pred)}


def tstr_trts(datasets, train, holdout, encode, seed):
    """Train on synthetic, test on real (TSTR) and train on real, test on synthetic (TRTS)."""
    X_hold, y_hold = encode(holdout)
    X_train, y_train = encode(train)
    rows = []
    for clf_name, real_model in classifiers(seed).items():
        real_model.fit(X_train, y_train)  # the TRTR baseline model, reused for TRTS
        for name, df in datasets.items():
            X_syn, y_syn = encode(df)
            if len(np.unique(y_syn)) < 2:
                print(f"{name}: only one class in the synthetic labels, TSTR skipped")
                continue
            syn_model = classifiers(seed)[clf_name].fit(X_syn, y_syn)
            row = {"data": name, "classifier": clf_name}
            row.update({f"TSTR {k}": v for k, v in scores(syn_model, X_hold, y_hold).items()})
            row.update({f"TRTS {k}": v for k, v in scores(real_model, X_syn, y_syn).items()})
            rows.append(row)
    return pd.DataFrame(rows)


def synthcity_alpha_precision(train, df, seed):
    """Alpha-precision, beta-recall and authenticity (Alaa et al., 2022) via synthcity."""
    from synthcity.metrics import Metrics

    result = Metrics.evaluate(
        X_gt=train, X_syn=df, metrics={"stats": ["alpha_precision"]},
        random_state=seed, use_cache=False,
    )
    return result["mean"].to_dict()


def fairx_metrics(train_csv, syn_csv, train, holdout, df, encode, utility=True):
    """FairX: utility of an XGBoost model trained on synthetic data, and FairX's
    implementation of alpha-precision, beta-recall and authenticity."""
    from fairx.dataset import CustomDataClass
    from fairx.metrics import DataUtilsMetrics, SyntheticEvaluation

    out = {}
    if utility:  # train on df, test on the real holdout set
        X_syn, y_syn = encode(df)
        X_hold, y_hold = encode(holdout)
        split = (X_syn, X_hold, y_syn, y_hold, df["sex"].to_numpy(), holdout["sex"].to_numpy())
        out.update({f"FairX XGB {k}": v for k, v in DataUtilsMetrics(split).evaluate_utility().items()})

    real_module = CustomDataClass(str(train_csv), "sex", [TARGET])
    syn_module = CustomDataClass(str(syn_csv), "sex", [TARGET])
    fidelity = SyntheticEvaluation(real_module, syn_module, use_cache=False).calculate_alpha_precision()
    out.update({f"FairX {k}": v for k, v in fidelity.items()})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("../lab-1/outputs"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("outputs_lab2"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    train = pd.read_csv(args.data_dir / "adult_train.csv")
    holdout = pd.read_csv(args.data_dir / "adult_holdout.csv")
    datasets = {
        "CTGAN": pd.read_csv(args.data_dir / "synthetic_ctgan.csv"),
        "TVAE": pd.read_csv(args.data_dir / "synthetic_tvae.csv"),
        "copy": train.copy(),
        "marginals": pd.DataFrame({c: rng.choice(train[c].to_numpy(), len(train)) for c in train.columns}),
    }
    for name in ["copy", "marginals"]:
        datasets[name].to_csv(args.out / f"synthetic_{name}.csv", index=False)
    csv_paths = {
        "CTGAN": args.data_dir / "synthetic_ctgan.csv",
        "TVAE": args.data_dir / "synthetic_tvae.csv",
        "copy": args.out / "synthetic_copy.csv",
        "marginals": args.out / "synthetic_marginals.csv",
    }
    encode = Encoder(train)

    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE", project_name="lab2-evaluation", output_dir=str(args.out), log_level="error"
    )
    tracker.start()
    start = time.perf_counter()

    # Task 1: TSTR and TRTS. The row "real" is the train-on-real, test-on-real baseline.
    utility = tstr_trts({"real": train, **datasets}, train, holdout, encode, args.seed)
    utility.to_csv(args.out / "tstr_trts.csv", index=False)
    print(utility.round(3).to_string(index=False))

    # Tasks 2 and 3: sample-level metrics (synthcity) and FairX metrics.
    # The real holdout rows serve as a reference: a fresh sample from the real distribution.
    datasets["real holdout"] = holdout
    csv_paths["real holdout"] = args.data_dir / "adult_holdout.csv"
    rows = []
    for name, df in datasets.items():
        t = time.perf_counter()
        row = {"data": name}
        row.update(synthcity_alpha_precision(train, df, args.seed))
        # The holdout set cannot be both training and test set, so it gets no FairX utility row.
        row.update(fairx_metrics(args.data_dir / "adult_train.csv", csv_paths[name], train, holdout, df, encode,
                                 utility=(name != "real holdout")))
        rows.append(row)
        print(f"{name}: metrics computed in {time.perf_counter() - t:.0f} s")
    fidelity = pd.DataFrame(rows).set_index("data")
    fidelity.to_csv(args.out / "fidelity.csv")

    seconds = time.perf_counter() - start
    tracker.stop()
    print(f"evaluation took {seconds:.0f} s, {tracker.final_emissions_data.energy_consumed * 1000:.2f} Wh")
    keep = [c for c in fidelity.columns if "naive" not in c]
    print(fidelity[keep].round(3).T.to_string())


if __name__ == "__main__":
    main()
