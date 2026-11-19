---
title: 2.1 Generative adversarial networks
linkTitle: 2.1 GANs
weight: 21
---

A generative adversarial network (GAN) trains two networks at once. The generator $G$ maps random noise $z$ to a sample $G(z)$. The discriminator $D$ receives a sample and estimates the probability that it came from the real data.

## The objective

The two networks play a minimax game:

$$
\min_G \max_D \; \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]
$$

In this game, the discriminator tries to tell real samples from generated ones, while the generator tries to produce samples that the discriminator accepts as real.

## A minimal training step

```python
import torch
import torch.nn as nn

loss_fn = nn.BCEWithLogitsLoss()

def train_step(G, D, real, opt_G, opt_D, z_dim=64):
    batch = real.size(0)
    z = torch.randn(batch, z_dim)
    fake = G(z)

    # Update the discriminator
    opt_D.zero_grad()
    loss_D = loss_fn(D(real), torch.ones(batch, 1)) + \
             loss_fn(D(fake.detach()), torch.zeros(batch, 1))
    loss_D.backward()
    opt_D.step()

    # Update the generator
    opt_G.zero_grad()
    loss_G = loss_fn(D(fake), torch.ones(batch, 1))
    loss_G.backward()
    opt_G.step()
    return loss_D.item(), loss_G.item()
```

## Known problems

GANs are hard to train. The generator can collapse onto a few modes of the data, and the losses of the two networks give little sign of sample quality. For tabular data, mixed discrete and continuous columns need extra care in the generator design.
