"""Lab 1, part B: train TimeGAN and TransFusion on sine sequences and compare their output.

Run from a terminal, with the TransFusion repository cloned next to this script:

    git clone https://github.com/fahim-sikder/TransFusion.git
    python lab1_timeseries.py --transfusion-dir TransFusion

The script writes the synthetic sequences, the figures and the CodeCarbon log
to the folder given by --out (default: outputs_ts).
"""

import argparse
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from codecarbon import OfflineEmissionsTracker
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def make_sines(n, seq_len, dim, rng):
    """Sine sequences generated as in the TimeGAN code (and TransFusion's data_make.py).

    Each feature is sin(f * t + p) with f and p drawn from U(0, 0.1), rescaled to [0, 1].
    """
    data = np.empty((n, seq_len, dim), dtype=np.float32)
    t = np.arange(seq_len)
    for i in range(n):
        for k in range(dim):
            freq = rng.uniform(0, 0.1)
            phase = rng.uniform(0, 0.1)
            data[i, :, k] = (np.sin(freq * t + phase) + 1) * 0.5
    return data


def tracked(name, out, fn):
    """Run fn() inside a CodeCarbon tracker; return its result, the time and the energy."""
    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE", project_name=f"lab1-{name}", output_dir=str(out), log_level="error"
    )
    tracker.start()
    start = time.perf_counter()
    result = fn()
    seconds = time.perf_counter() - start
    tracker.stop()
    energy = tracker.final_emissions_data.energy_consumed
    print(f"{name}: {seconds:.0f} s, {energy * 1000:.2f} Wh")
    return result, seconds, energy


def run_timegan(real, n_iter, clusters, seed):
    from synthcity.plugins import Plugins
    from synthcity.plugins.core.dataloader import TimeSeriesDataLoader

    n, seq_len, dim = real.shape
    columns = [f"x{k}" for k in range(dim)]
    temporal = [pd.DataFrame(seq, columns=columns) for seq in real]
    times = [list(range(seq_len)) for _ in range(n)]
    # synthcity also models a static part and an outcome; we give it constant dummies.
    static = pd.DataFrame({"static": np.zeros(n)})
    outcome = pd.DataFrame({"outcome": np.zeros(n)})
    loader = TimeSeriesDataLoader(
        temporal_data=temporal, observation_times=times, static_data=static, outcome=outcome
    )
    # Smaller networks than the synthcity defaults (150 and 300 hidden units, 20 clusters)
    # so that training fits in a few minutes on a laptop CPU. encoder_max_clusters sets
    # how many Gaussian mixture modes the data encoder may use for each feature.
    model = Plugins().get(
        "timegan", n_iter=n_iter, batch_size=128, random_state=seed, device="cpu",
        generator_n_units_hidden=50, discriminator_n_units_hidden=50, encoder_max_clusters=clusters,
    )
    model.fit(loader)
    # Passing the observation times fixes the length of every generated sequence.
    _, temporal_syn, _, _ = model.generate(count=n, observation_times=times).unpack()
    return np.stack([df[columns].to_numpy(dtype=np.float32) for df in temporal_syn])


def run_transfusion(real, transfusion_dir, epochs, timesteps, seed):
    sys.path.insert(0, str(Path(transfusion_dir).resolve()))
    from ddpm import GaussianDiffusion1D, TransEncoder  # from the TransFusion repository

    torch.manual_seed(seed)
    n, seq_len, dim = real.shape
    # A small configuration for a laptop CPU; train.py in the repository uses
    # hidden_dim=256, num_layers=6, n_head=8, timesteps=1000 and 5000 epochs.
    model = TransEncoder(features=dim, latent_dim=64, num_heads=4, num_layers=2, ff_size=256)
    diffusion = GaussianDiffusion1D(
        model, seq_length=seq_len, timesteps=timesteps,
        objective="pred_v", loss_type="l2", beta_schedule="cosine",
    )
    optimiser = torch.optim.Adam(diffusion.parameters(), lr=1e-3, betas=(0.9, 0.99))
    # TransFusion expects tensors shaped (batch, features, sequence length) with values in [0, 1].
    loader = torch.utils.data.DataLoader(
        torch.from_numpy(real.transpose(0, 2, 1)).contiguous(), batch_size=64, shuffle=True
    )
    for epoch in range(epochs):
        for batch in loader:
            optimiser.zero_grad()
            loss = diffusion(batch)
            loss.backward()
            optimiser.step()
        if (epoch + 1) % 50 == 0:
            print(f"TransFusion epoch {epoch + 1}: loss {loss.item():.4f}")
    diffusion.eval()
    with torch.no_grad():
        samples = diffusion.sample(batch_size=n)  # values in [0, 1]
    return samples.numpy().transpose(0, 2, 1)


def plot_samples(real, synth, out, n_show=4):
    fig, axes = plt.subplots(1 + len(synth), n_show, figsize=(3.2 * n_show, 2.4 * (1 + len(synth))), sharey=True)
    for row, (name, data) in enumerate([("real", real)] + list(synth.items())):
        for j in range(n_show):
            axes[row, j].plot(data[j])
            axes[row, j].set_title(f"{name}, sequence {j}", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "ts_samples.png", dpi=120)
    plt.close(fig)


def plot_projections(real, synth, out, n_points=500, seed=0):
    """PCA and t-SNE of flattened sequences (each sequence becomes one point)."""
    flat_real = real[:n_points].reshape(n_points, -1)
    pca = PCA(n_components=2).fit(flat_real)
    fig, axes = plt.subplots(2, len(synth), figsize=(5.5 * len(synth), 9), squeeze=False)
    for col, (name, data) in enumerate(synth.items()):
        flat_syn = data[:n_points].reshape(n_points, -1)
        r, s = pca.transform(flat_real), pca.transform(flat_syn)
        axes[0, col].scatter(r[:, 0], r[:, 1], s=5, alpha=0.5, label="real")
        axes[0, col].scatter(s[:, 0], s[:, 1], s=5, alpha=0.5, label=name)
        axes[0, col].set_title(f"PCA: {name}")
        axes[0, col].legend()
        emb = TSNE(n_components=2, perplexity=40, random_state=seed).fit_transform(
            np.vstack([flat_real, flat_syn])
        )
        axes[1, col].scatter(emb[:n_points, 0], emb[:n_points, 1], s=5, alpha=0.5, label="real")
        axes[1, col].scatter(emb[n_points:, 0], emb[n_points:, 1], s=5, alpha=0.5, label=name)
        axes[1, col].set_title(f"t-SNE: {name}")
        axes[1, col].legend()
    fig.tight_layout()
    fig.savefig(out / "ts_projections.png", dpi=120)
    plt.close(fig)


def summary_statistics(real, synth):
    """Simple checks: value range, mean, and lag-1 autocorrelation per feature."""
    def lag1(data):
        x, y = data[:, :-1, :].reshape(-1), data[:, 1:, :].reshape(-1)
        return np.corrcoef(x, y)[0, 1]

    rows = []
    for name, data in [("real", real)] + list(synth.items()):
        rows.append({
            "data": name,
            "min": data.min(), "max": data.max(), "mean": data.mean(),
            "std across sequences": data.mean(axis=(1, 2)).std(),
            "lag-1 autocorrelation": lag1(data),
        })
    return pd.DataFrame(rows).set_index("data")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfusion-dir", type=Path, default=Path("TransFusion"))
    parser.add_argument("--n", type=int, default=500, help="number of training sequences")
    parser.add_argument("--seq-len", type=int, default=24)
    parser.add_argument("--dim", type=int, default=5)
    parser.add_argument("--models", nargs="+", default=["timegan", "transfusion"],
                        choices=["timegan", "transfusion"])
    parser.add_argument("--timegan-iter", type=int, default=100)
    parser.add_argument("--timegan-clusters", type=int, default=5)
    parser.add_argument("--transfusion-epochs", type=int, default=200)
    parser.add_argument("--timesteps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("outputs_ts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    real = make_sines(args.n, args.seq_len, args.dim, np.random.default_rng(args.seed))
    np.save(args.out / "real_sines.npy", real)

    synth, rows = {}, []
    if "timegan" in args.models:
        timegan, s, e = tracked(
            "TimeGAN", args.out, lambda: run_timegan(real, args.timegan_iter, args.timegan_clusters, args.seed)
        )
        synth["TimeGAN"] = timegan
        rows.append({"model": "TimeGAN", "seconds": round(s), "energy Wh": round(e * 1000, 2)})
    if "transfusion" in args.models:
        transfusion, s, e = tracked(
            "TransFusion", args.out,
            lambda: run_transfusion(real, args.transfusion_dir, args.transfusion_epochs, args.timesteps, args.seed),
        )
        synth["TransFusion"] = transfusion
        rows.append({"model": "TransFusion", "seconds": round(s), "energy Wh": round(e * 1000, 2)})
    for name, data in synth.items():
        np.save(args.out / f"synthetic_{name.lower()}.npy", data)

    plot_samples(real, synth, args.out)
    plot_projections(real, synth, args.out, seed=args.seed)
    print(pd.DataFrame(rows).to_string(index=False))
    print(summary_statistics(real, synth).round(3).to_string())


if __name__ == "__main__":
    main()
