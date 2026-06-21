# KCCA Feature Fusion Specification

## 1. Paper requirements

KCCA must fuse:

```text
X = Gabor features
Y = Conformer features
```

Process:

```text
X, Y
→ kernel mapping into high-dimensional spaces
→ CCA in kernel space
→ canonical correlated components
→ fused Gabor-Conformer vector
```

Supported kernel functions:

- cosine
- RBF
- Laplacian

Default kernel:

```text
cosine
```

## 2. Required classes

```python
class KCCAFusion:
    def fit(self, X_train: np.ndarray, Y_train: np.ndarray) -> "KCCAFusion":
        ...

    def transform(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        ...

    def transform_single(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        ...

    def save(self, path: str) -> None:
        ...

    @classmethod
    def load(cls, path: str) -> "KCCAFusion":
        ...
```

## 3. Kernels

```python
def cosine_kernel(X, Y=None, eps=1e-12):
    Xn = normalize(X)
    Yn = normalize(Y if Y is not None else X)
    return Xn @ Yn.T
```

```python
def rbf_kernel(X, Y=None, gamma=None):
    return exp(-gamma * squared_euclidean_distance(X, Y))
```

```python
def laplacian_kernel(X, Y=None, gamma=None):
    return exp(-gamma * manhattan_distance(X, Y))
```

## 4. Training-only fitting

KCCA must be fit on train data only.

```python
kcca.fit(X_gabor_train, Y_conformer_train)
Z_train = kcca.transform(X_gabor_train, Y_conformer_train)
Z_test = kcca.transform(X_gabor_test, Y_conformer_test)
```

## 5. Numerical method

Regularized centered KCCA:

```text
Kx = kernel(X_train, X_train)
Ky = kernel(Y_train, Y_train)

center Kx, Ky

Cxx = Kx Kx + reg I
Cyy = Ky Ky + reg I
Cxy = Kx Ky
Cyx = Ky Kx

solve:
Cxx^-1 Cxy Cyy^-1 Cyx a = rho^2 a

derive alpha and beta
U = Kx_test alpha
V = Ky_test beta
Z = fuse(U, V)
```

## 6. Config

```yaml
kcca:
  kernel: cosine
  n_components: 256
  reg: 1.0e-3
  center_kernels: true

  # IMPLEMENTATION ASSUMPTIONS:
  pre_reduce: true
  reducer: pca
  x_reduce_dim: 1024
  y_reduce_dim: 512
  fusion_strategy: sum
  l2_normalize_output: true
```

## 7. Fusion strategy

Paper does not specify exact operation after canonical components.

Default assumption:

```python
Z = U + V
Z = l2_normalize(Z)
```

Required alternatives for ablation:

```text
concat
weighted_sum
```

## 8. Serialization

Save:

```python
{
    "kernel_name": ...,
    "n_components": ...,
    "reg": ...,
    "scaler_x": ...,
    "scaler_y": ...,
    "reducer_x": ...,
    "reducer_y": ...,
    "X_ref": ...,
    "Y_ref": ...,
    "kernel_centerer_x": ...,
    "kernel_centerer_y": ...,
    "alpha": ...,
    "beta": ...,
    "config": ...
}
```

## 9. Tests

- kernel matrices are symmetric for `kernel(X, X)`.
- diagonal of cosine kernel is close to 1 after normalization.
- `fit()` runs on toy data.
- `transform()` output shape is `[n_samples, n_components]` for sum strategy.
- no singular matrix crash with regularization.
- save/load gives identical transform.
