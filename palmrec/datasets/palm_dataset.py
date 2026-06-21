import os
import json
import random
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import torchvision.transforms.functional as F

class RandomGamma:
    """Apply random gamma correction to an image."""
    def __init__(self, min_gamma=0.9, max_gamma=1.1):
        self.min_gamma = min_gamma
        self.max_gamma = max_gamma
        
    def __call__(self, img):
        gamma = random.uniform(self.min_gamma, self.max_gamma)
        return F.adjust_gamma(img, gamma)

class PalmDataset(Dataset):
    """
    PyTorch Dataset for Palmprint Recognition (LGF-Net Pipeline).
    Loads grayscale images, resizes to 224x224, converts to 3-channel,
    and applies light augmentation for training or normalization for evaluation.
    """
    def __init__(self, split_file: str, split_name: str, transform=None, remap_classes=True, class_mapping=None, root_dir: str = ""):
        """
        Args:
            split_file: Path to the JSON split file.
            split_name: One of 'train', 'val', 'gallery', 'probe', 'support'.
            transform: Optional torchvision transform. If None, default transforms are applied.
            remap_classes: If True, map class_ids in this split to a contiguous range 0..C-1.
            class_mapping: Optional pre-defined mapping from original class_id to contiguous class_id.
            root_dir: Optional root directory to prepend to image paths.
        """
        if not os.path.exists(split_file):
            raise FileNotFoundError(f"Split file not found: {split_file}")
            
        with open(split_file, "r") as f:
            split_data = json.load(f)
            
        if split_name not in split_data:
            raise ValueError(f"Split name '{split_name}' not found in split file. Options: {list(split_data.keys())}")
            
        self.samples = split_data[split_name]
        self.split_name = split_name
        self.remap_classes = remap_classes
        self.root_dir = root_dir
        
        # Build or use class mapping
        if remap_classes:
            if class_mapping is not None:
                self.class_mapping = class_mapping
            else:
                # Find all unique original class_ids in this split (or in the train split if it exists)
                # To be consistent, we sort the unique class_ids
                unique_classes = sorted(list(set(s["class_id"] for s in self.samples)))
                self.class_mapping = {cid: idx for idx, cid in enumerate(unique_classes)}
        else:
            self.class_mapping = None

        if transform is not None:
            self.transform = transform
        else:
            if split_name == "train":
                self.transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.RandomAffine(degrees=(-8, 8), translate=(0.05, 0.05), scale=(0.95, 1.05)),
                    transforms.ColorJitter(brightness=0.1, contrast=0.1),
                    RandomGamma(0.9, 1.1),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
            else:
                self.transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        sample = self.samples[idx]
        path = sample["path"]
        if self.root_dir:
            path = os.path.join(self.root_dir, path)
            
        orig_class_id = sample["class_id"]
        
        if self.remap_classes and self.class_mapping is not None:
            class_id = self.class_mapping.get(orig_class_id, -1)
        else:
            class_id = orig_class_id
            
        # load grayscale ROI
        img = Image.open(path).convert("L")
        # convert to 3-channel
        img = img.convert("RGB")
        
        if self.transform:
            img = self.transform(img)
            
        return {
            "image": img,
            "label": class_id,
            "orig_label": orig_class_id,
            "path": sample["path"]
        }
