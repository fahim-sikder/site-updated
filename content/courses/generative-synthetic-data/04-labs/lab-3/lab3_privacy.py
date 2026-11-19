"""Lab 3: train private generative models and evaluate privacy.

Run from a terminal after Lab 1, pointing --data-dir at the Lab 1 output folder:

    python lab3_privacy.py --data-dir ../lab-1/outputs

Part 1 trains DPGAN, a GAN whose discriminator is trained with differentially
private stochastic gradient descent, at several values of epsilon.
Part 2 measures how much utility the privacy costs.
Part 3 runs two privacy evaluations on every synthetic data set: distance to
the closest record (DCR) and the DOMIAS membership inference attack.
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from codecarbon import OfflineEmissionsTracker
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

NUMERIC = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
CATEGORICAL = [
    "workclass", "education", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country",
]
TARGET, POSITIVE = "class", ">50K"


# ---------------------------------------------------------------- part 1
def train_dpgan(train, epsilon, n_iter, units, seed, out):
    """Train synthcity's DPGAN plugin inside a CodeCarbon tracker.

    synthcity sets delta = 1 / (number of training rows) when delta is not given.
    The hidden layers are smaller than the plugin default (500 units), because
    per-example gradients make DP training slow on a CPU.
    """
    from synthcity.plugins import Plugins

    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE", project_name=f"lab3-dpgan-eps{epsilon:g}",
        output_dir=str(out), log_level="error",
    )
    tracker.start()
    start = time.perf_counter()
    model = Plugins().get(
        "dpgan", epsilon=epsilon, n_iter=n_iter, random_state=seed, device="cpu",
        generator_n_units_hidden=units, discriminator_n_units_hidden=units,
    )
    model.fit(train)
    synthetic = model.generate(count=len(train)).dataframe()
    seconds = time.perf_counter() - start
    tracker.stop()
    energy = tracker.final_emissions_data.energy_consumed
    print(f"DPGAN epsilon={epsilon:g}: {seconds:.0f} s, {energy * 1000:.2f} Wh")
    return synthetic, seconds, energy


# ---------------------------------------------------------------- part 2
def tstr_auroc(train_df, holdout, real):
    """AUROC on the real holdout of a logistic regression trained on train_df."""
    onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(real[CATEGORICAL])
    scaler = StandardScaler().fit(real[NUMERIC])

    def encode(df):
        X = np.hstack([scaler.transform(df[NUMERIC]), onehot.transform(df[CATEGORICAL])])
        return X, (df[TARGET] == POSITIVE).astype(int).to_numpy()

    X, y = encode(train_df)
    if len(np.unique(y)) < 2:
        return float("nan")
    model = LogisticRegression(max_iter=2000).fit(X, y)
    X_hold, y_hold = encode(holdout)
    return roc_auc_score(y_hold, model.predict_proba(X_hold)[:, 1])


# ---------------------------------------------------------------- part 3
class DistanceEncoder:
    """Min-max scaled numeric columns and one-hot categorical columns, so that
    every column contributes at most 1 to the squared distance."""

    def __init__(self, real):
        self.onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(real[CATEGORICAL + [TARGET]])
        self.scaler = MinMaxScaler().fit(real[NUMERIC])

    def __call__(self, df):
        return np.hstack([self.scaler.transform(df[NUMERIC]), self.onehot.transform(df[CATEGORICAL + [TARGET]])])


def dcr(synthetic, train, holdout, encode):
    """Distance from each synthetic row to its closest training row and closest holdout row."""
    S, T, H = encode(synthetic), encode(train), encode(holdout)
    # A k-d tree computes each distance directly, so identical rows get a distance of exactly 0.
    d_train = NearestNeighbors(n_neighbors=1, algorithm="kd_tree").fit(T).kneighbors(S)[0][:, 0]
    d_hold = NearestNeighbors(n_neighbors=1, algorithm="kd_tree").fit(H).kneighbors(S)[0][:, 0]
    copies = synthetic.merge(train.drop_duplicates(), how="inner", on=list(train.columns))
    return {
        "exact copies of training rows": len(copies),
        "median DCR to train": float(np.median(d_train)),
        "median DCR to holdout": float(np.median(d_hold)),
        "share closer to train than holdout": float((d_train < d_hold).mean()),
    }


def domias(synthetic, train, holdout, reference, n, seed):
    """DOMIAS membership inference attack (van Breugel et al., 2023), synthcity's KDE version.

    Members are n training rows; non-members are n holdout rows. The attack
    scores each row by p_synthetic(x) / p_reference(x) and reports the AUROC.
    """
    from synthcity.metrics.eval_privacy import DomiasMIAKDE
    from synthcity.plugins.core.dataloader import GenericDataLoader

    # synthcity encodes categorical columns as integer codes, as it does in Metrics.evaluate.
    every = pd.concat([train, holdout, reference, synthetic])
    codes = {c: {v: i for i, v in enumerate(sorted(every[c].astype(str).unique()))} for c in CATEGORICAL + [TARGET]}

    def encode(df):
        df = df.copy()
        for c, mapping in codes.items():
            if c in df.columns:
                df[c] = df[c].astype(str).map(mapping)
        return GenericDataLoader(df.astype(float).reset_index(drop=True))

    members = train.sample(n, random_state=seed)
    non_members = holdout.sample(n, random_state=seed)
    ref = reference.sample(n, random_state=seed)
    syn = synthetic.sample(min(len(synthetic), 2 * n), random_state=seed)
    half = len(syn) // 2
    # A Gaussian KDE needs every column to vary. Columns that are constant in the
    # synthetic sample or in the reference sample are left out of the attack.
    keep = [c for c in train.columns if syn[c].iloc[:half].nunique() > 1 and ref[c].nunique() > 1]
    dropped = sorted(set(train.columns) - set(keep))
    if dropped:
        print(f"DOMIAS: columns without variation left out: {dropped}")
    # synthcity takes the first n rows of X_gt as non-members and the last n rows as the reference set.
    X_gt = encode(pd.concat([non_members, ref])[keep])
    try:
        result = DomiasMIAKDE(use_cache=False).evaluate(
            X_gt, encode(syn.iloc[:half][keep]), encode(members[keep]), encode(syn.iloc[half:][keep]),
            reference_size=n,
        )
    except np.linalg.LinAlgError as err:
        print(f"DOMIAS failed: {err}")
        return {"DOMIAS AUROC": float("nan"), "DOMIAS accuracy": float("nan")}
    return {"DOMIAS AUROC": result["aucroc"], "DOMIAS accuracy": result["accuracy"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("../lab-1/outputs"))
    parser.add_argument("--epsilons", type=float, nargs="+", default=[1.0, 10.0])
    parser.add_argument("--n-iter", type=int, default=100, help="DPGAN training epochs")
    parser.add_argument("--units", type=int, default=100, help="hidden units per layer in DPGAN")
    parser.add_argument("--attack-size", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("outputs_lab3"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(args.data_dir / "adult_train.csv")
    holdout = pd.read_csv(args.data_dir / "adult_holdout.csv")
    reference = pd.read_csv(args.data_dir / "adult_reference.csv")
    datasets = {
        "CTGAN (no DP)": pd.read_csv(args.data_dir / "synthetic_ctgan.csv"),
        "TVAE (no DP)": pd.read_csv(args.data_dir / "synthetic_tvae.csv"),
        "copy of train": train.copy(),
    }

    # Part 1: private generators.
    for eps in args.epsilons:
        df, _, _ = train_dpgan(train, eps, args.n_iter, args.units, args.seed, args.out)
        df.to_csv(args.out / f"synthetic_dpgan_eps{eps:g}.csv", index=False)
        datasets[f"DPGAN eps={eps:g}"] = df

    # Parts 2 and 3: utility and privacy of every data set.
    rows = []
    encode = DistanceEncoder(train)
    for name, df in datasets.items():
        row = {"data": name, "TSTR AUROC": tstr_auroc(df, holdout, train)}
        row.update(dcr(df, train, holdout, encode))
        row.update(domias(df, train, holdout, reference, args.attack_size, args.seed))
        rows.append(row)
    rows.append({"data": "real (TRTR)", "TSTR AUROC": tstr_auroc(train, holdout, train)})
    table = pd.DataFrame(rows).set_index("data")
    table.to_csv(args.out / "privacy_utility.csv")
    print(table.round(3).to_string())


if __name__ == "__main__":
    main()
