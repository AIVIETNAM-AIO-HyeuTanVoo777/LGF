import random
import torch
from torch.utils.data import Sampler
from collections import defaultdict

class RandomIdentitySampler(Sampler):
    """
    Randomly sample P identities, and for each identity sample K images.
    Batch size = P * K.
    """
    def __init__(self, dataset, num_instances=2, num_identities=8, fallback_identities=4):
        """
        Args:
            dataset: PyTorch Dataset, must return a dict with a 'label' key or have a targets/labels attribute.
            num_instances (K): Number of images per identity in a batch.
            num_identities (P): Number of identities in a batch.
            fallback_identities: Fallback P if the default P is too large for the dataset.
        """
        self.dataset = dataset
        self.K = num_instances
        
        # Determine labels/targets from dataset
        self.labels = []
        for i in range(len(dataset)):
            # Handle list/dict or dataset attributes
            if hasattr(dataset, "samples"):
                # Fast path for PalmDataset
                label = dataset.samples[i]["class_id"]
                if dataset.remap_classes and dataset.class_mapping is not None:
                    label = dataset.class_mapping.get(label, -1)
            elif hasattr(dataset, "metadata"):
                # Fast path for PalmprintDataset
                label = dataset.metadata.iloc[i]["class_id"]
            else:
                # Fallback to indexing (might be slow but robust)
                sample = dataset[i]
                if isinstance(sample, dict):
                    label = sample["label"]
                else:
                    label = sample[1]
            self.labels.append(int(label))
            
        # Group indices by label
        self.label_to_indices = defaultdict(list)
        for idx, label in enumerate(self.labels):
            self.label_to_indices[label].append(idx)
            
        self.unique_labels = sorted(list(self.label_to_indices.keys()))
        num_unique_labels = len(self.unique_labels)
        
        # Choose P (number of identities)
        if num_unique_labels >= num_identities:
            self.P = num_identities
        elif num_unique_labels >= fallback_identities:
            self.P = fallback_identities
            print(f"RandomIdentitySampler: Number of unique labels ({num_unique_labels}) is less than requested P ({num_identities}). Using fallback P ({fallback_identities}).")
        else:
            self.P = max(1, num_unique_labels)
            print(f"RandomIdentitySampler: Extremely small dataset! Using P = {self.P}.")
            
        self.batch_size = self.P * self.K
        
    def __iter__(self):
        # Shuffle unique labels
        shuffled_labels = list(self.unique_labels)
        random.shuffle(shuffled_labels)
        
        # Shuffle indices for each label and set up generators/pointers
        label_indices_shuffled = {}
        label_pointers = {}
        for label, indices in self.label_to_indices.items():
            shuffled_idx = list(indices)
            random.shuffle(shuffled_idx)
            label_indices_shuffled[label] = shuffled_idx
            label_pointers[label] = 0
            
        # We will yield batches of size P * K
        # Number of batches we can yield is floor(len(unique_labels) / P)
        num_batches = len(shuffled_labels) // self.P
        
        for batch_idx in range(num_batches):
            batch_indices = []
            selected_labels = shuffled_labels[batch_idx * self.P : (batch_idx + 1) * self.P]
            
            for label in selected_labels:
                indices = label_indices_shuffled[label]
                ptr = label_pointers[label]
                
                # Retrieve K indices
                samples_needed = self.K
                while samples_needed > 0:
                    available = len(indices) - ptr
                    take = min(samples_needed, available)
                    
                    batch_indices.extend(indices[ptr : ptr + take])
                    ptr += take
                    samples_needed -= take
                    
                    if ptr >= len(indices):
                        # Reshuffle and reset pointer
                        random.shuffle(indices)
                        ptr = 0
                        
                label_pointers[label] = ptr
                
            yield batch_indices

    def __len__(self):
        # Returns the number of batches * batch_size (number of total samples in one epoch)
        num_batches = len(self.unique_labels) // self.P
        return num_batches * self.batch_size
