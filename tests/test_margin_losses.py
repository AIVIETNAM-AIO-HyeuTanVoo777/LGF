import torch

from palmrec.losses.margin import ArcFaceLoss, CosFaceLoss, build_loss


def test_arcface_loss_backward():
    loss_fn = ArcFaceLoss(embedding_dim=16, num_classes=4, scale=30.0, margin=0.5)
    embeddings = torch.randn(8, 16, requires_grad=True)
    labels = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3])

    loss, logits = loss_fn(embeddings, labels)
    loss.backward()

    assert torch.isfinite(loss)
    assert logits.shape == (8, 4)
    assert embeddings.grad is not None
    assert loss_fn.weight.grad is not None


def test_cosface_loss_backward():
    loss_fn = CosFaceLoss(embedding_dim=16, num_classes=4, scale=30.0, margin=0.35)
    embeddings = torch.randn(8, 16, requires_grad=True)
    labels = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3])

    loss, logits = loss_fn(embeddings, labels)
    loss.backward()

    assert torch.isfinite(loss)
    assert logits.shape == (8, 4)
    assert embeddings.grad is not None
    assert loss_fn.weight.grad is not None


def test_build_loss_supports_training_loss_type_arcface():
    cfg = {
        "training": {
            "loss_type": "arcface",
            "lambda_supcon": 0.05,
            "temperature": 0.07,
        }
    }
    loss_fn = build_loss(cfg, num_classes=4, embedding_dim=16)
    embeddings = torch.randn(8, 16, requires_grad=True)
    logits = torch.randn(8, 4)
    labels = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3])

    loss, loss_dict = loss_fn(logits, embeddings, labels)

    assert torch.isfinite(loss)
    assert "loss_margin" in loss_dict
    assert loss_dict["loss_supcon"] >= 0.0
