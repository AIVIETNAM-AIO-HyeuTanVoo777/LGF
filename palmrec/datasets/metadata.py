import os
import re
import pandas as pd
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Unified metadata schema columns
METADATA_COLUMNS = [
    "sample_id",
    "dataset",
    "image_path",
    "subject_id",
    "palm_id",
    "class_id",
    "gender",
    "hand_side",
    "session",
    "image_index",
    "is_valid",
    "notes"
]

def parse_casia(image_path: str, gender_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Parse CASIA palmprint filename.
    Typical filename: 001_l_1.jpg, 001_r_2.jpg, or in folder 001/001_l_1.jpg
    """
    filename = os.path.basename(image_path)
    # Regex pattern: subjectID_hand_index
    match = re.match(r"^(\d+)_([lr])_(\d+)\.(?:jpg|png|jpeg|bmp|tiff)$", filename, re.IGNORECASE)
    if not match:
        # Try a more relaxed pattern
        match = re.search(r"(\d+)_([lrLR])_(\d+)", filename)
        
    if match:
        subject_id = match.group(1).zfill(3)
        hand_char = match.group(2).lower()
        hand_side = "left" if hand_char == "l" else "right"
        image_index = int(match.group(3))
    else:
        # Heuristics from path
        parent_dir = os.path.basename(os.path.dirname(image_path))
        if parent_dir.isdigit():
            subject_id = parent_dir.zfill(3)
        else:
            subject_id = "000"
        hand_side = "left" if "l" in filename.lower() else "right" if "r" in filename.lower() else "unknown"
        image_index = 0
        
    palm_id = f"{subject_id}_{hand_side}"
    gender = "unknown"
    if gender_map and subject_id in gender_map:
        gender = gender_map[subject_id]
        
    return {
        "dataset": "CASIA",
        "image_path": os.path.abspath(image_path),
        "subject_id": subject_id,
        "palm_id": palm_id,
        "gender": gender,
        "hand_side": hand_side,
        "session": "1",
        "image_index": image_index,
        "is_valid": True,
        "notes": "Parsed successfully"
    }

def parse_tju(image_path: str) -> Dict[str, Any]:
    """Parse TJU palmprint filename.
    Typical filename: sub_001_l_s1_1.jpg or similar.
    """
    filename = os.path.basename(image_path)
    # Typical TJU pattern: subjectID_hand_session_index
    match = re.search(r"(\d+)_([lrLR])_s?(\d+)_(\d+)", filename)
    if match:
        subject_id = match.group(1).zfill(3)
        hand_char = match.group(2).lower()
        hand_side = "left" if hand_char == "l" else "right"
        session = match.group(3)
        image_index = int(match.group(4))
    else:
        # relaxed parsing
        subject_id = "000"
        hand_side = "unknown"
        session = "unknown"
        image_index = 0
        # Try to find numbers
        digits = re.findall(r"\d+", filename)
        if len(digits) >= 1:
            subject_id = digits[0].zfill(3)
        if "l" in filename.lower():
            hand_side = "left"
        elif "r" in filename.lower():
            hand_side = "right"
            
    palm_id = f"{subject_id}_{hand_side}"
    return {
        "dataset": "TJU",
        "image_path": os.path.abspath(image_path),
        "subject_id": subject_id,
        "palm_id": palm_id,
        "gender": "unknown",
        "hand_side": hand_side,
        "session": session,
        "image_index": image_index,
        "is_valid": True,
        "notes": "Parsed successfully"
    }

def parse_xjtu(image_path: str) -> Dict[str, Any]:
    """Parse XJTU palmprint filename."""
    filename = os.path.basename(image_path)
    # Typical: 001_l_1.jpg, etc.
    match = re.search(r"(\d+)_([lrLR])_(\d+)", filename)
    if match:
        subject_id = match.group(1).zfill(3)
        hand_char = match.group(2).lower()
        hand_side = "left" if hand_char == "l" else "right"
        image_index = int(match.group(3))
    else:
        subject_id = "000"
        hand_side = "unknown"
        image_index = 0
        digits = re.findall(r"\d+", filename)
        if len(digits) >= 1:
            subject_id = digits[0].zfill(3)
        if "l" in filename.lower():
            hand_side = "left"
        elif "r" in filename.lower():
            hand_side = "right"
            
    palm_id = f"{subject_id}_{hand_side}"
    return {
        "dataset": "XJTU",
        "image_path": os.path.abspath(image_path),
        "subject_id": subject_id,
        "palm_id": palm_id,
        "gender": "unknown",
        "hand_side": hand_side,
        "session": "1",
        "image_index": image_index,
        "is_valid": True,
        "notes": "Parsed successfully"
    }

def parse_iitd(image_path: str) -> Dict[str, Any]:
    """Parse IITD palmprint filename.
    IITD is typically organized as:
    raw_dir/001/01.jpg, 001/02.jpg ... (left/right hand side might not be split or has separate folders)
    If folders exist: e.g. 001/01.jpg, we assume left/right based on image index (e.g. 1-5 left, 6-10 right, or all left etc.).
    Let's check if the path has 'left' or 'right' in it.
    """
    filename = os.path.basename(image_path)
    parent_dir = os.path.basename(os.path.dirname(image_path))
    
    subject_id = parent_dir.zfill(3) if parent_dir.isdigit() else "000"
    
    # In IITD, 01.jpg to 05.jpg are typically left hand, or similar.
    # We check filename for index:
    match = re.search(r"(\d+)", filename)
    image_index = int(match.group(1)) if match else 0
    
    # Typical IITD rule: 1-5 is left, 6-10 is right (or similar)
    # Let's assume: index <= 5 is left, index > 5 is right, or if path has hand side indicators
    hand_side = "unknown"
    if "left" in image_path.lower() or "l_" in filename.lower():
        hand_side = "left"
    elif "right" in image_path.lower() or "r_" in filename.lower():
        hand_side = "right"
    else:
        # Default IITD convention: images 1-5 are left, 6-10 are right
        if 1 <= image_index <= 5:
            hand_side = "left"
        elif 6 <= image_index <= 10:
            hand_side = "right"
        else:
            hand_side = "left"
            
    palm_id = f"{subject_id}_{hand_side}"
    return {
        "dataset": "IITD",
        "image_path": os.path.abspath(image_path),
        "subject_id": subject_id,
        "palm_id": palm_id,
        "gender": "unknown",
        "hand_side": hand_side,
        "session": "1",
        "image_index": image_index,
        "is_valid": True,
        "notes": "Parsed successfully"
    }

def parse_toy(image_path: str) -> Dict[str, Any]:
    """Parse synthetic TOY dataset filename."""
    filename = os.path.basename(image_path)
    # Filename format: subjectID_hand_index.jpg
    match = re.search(r"sub_(\d+)_([lr])_(\d+)", filename, re.IGNORECASE)
    if match:
        subject_id = match.group(1).zfill(3)
        hand_char = match.group(2).lower()
        hand_side = "left" if hand_char == "l" else "right"
        image_index = int(match.group(3))
    else:
        subject_id = "000"
        hand_side = "left"
        image_index = 0
        
    palm_id = f"{subject_id}_{hand_side}"
    # We can assign dummy gender (e.g. male/female) based on subject_id
    gender = "male" if int(subject_id) % 2 == 0 else "female"
    
    return {
        "dataset": "TOY",
        "image_path": os.path.abspath(image_path),
        "subject_id": subject_id,
        "palm_id": palm_id,
        "gender": gender,
        "hand_side": hand_side,
        "session": "1",
        "image_index": image_index,
        "is_valid": True,
        "notes": "Parsed successfully"
    }

def parse_image_metadata(
    image_path: str,
    dataset_name: str,
    gender_map: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Dispatch to specific dataset parser and return metadata dictionary."""
    name_upper = dataset_name.upper()
    if name_upper == "CASIA":
        meta = parse_casia(image_path, gender_map)
    elif name_upper == "TJU":
        meta = parse_tju(image_path)
    elif name_upper == "XJTU":
        meta = parse_xjtu(image_path)
    elif name_upper == "IITD":
        meta = parse_iitd(image_path)
    elif name_upper == "TOY":
        meta = parse_toy(image_path)
    else:
        # Generic fallback parser
        filename = os.path.basename(image_path)
        subject_id = "000"
        digits = re.findall(r"\d+", filename)
        if digits:
            subject_id = digits[0].zfill(3)
        hand_side = "left" if "l" in filename.lower() else "right" if "r" in filename.lower() else "unknown"
        palm_id = f"{subject_id}_{hand_side}"
        meta = {
            "dataset": dataset_name,
            "image_path": os.path.abspath(image_path),
            "subject_id": subject_id,
            "palm_id": palm_id,
            "gender": "unknown",
            "hand_side": hand_side,
            "session": "1",
            "image_index": 0,
            "is_valid": True,
            "notes": "Fallback parsed successfully"
        }
        
    # Generate stable sample_id
    filename_no_ext = os.path.splitext(os.path.basename(image_path))[0]
    meta["sample_id"] = f"{meta['dataset']}_{meta['subject_id']}_{meta['hand_side']}_{meta['session']}_{filename_no_ext}"
    
    return meta

def build_metadata_dataframe(
    raw_dir: str,
    dataset_name: str,
    gender_mapping_file: Optional[str] = None
) -> pd.DataFrame:
    """Scan raw directory for images and compile unified metadata DataFrame."""
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")
        
    # Load gender map if provided
    gender_map = None
    if gender_mapping_file and os.path.exists(gender_mapping_file):
        try:
            gender_df = pd.read_csv(gender_mapping_file)
            # assume columns subject_id and gender
            gender_map = dict(zip(gender_df["subject_id"].astype(str).str.zfill(3), gender_df["gender"].astype(str)))
        except Exception as e:
            logger.error(f"Error loading gender mapping file: {e}")
            
    # Find all images
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    image_paths = []
    for root, _, files in os.walk(raw_dir):
        for f in files:
            if f.lower().endswith(image_extensions):
                image_paths.append(os.path.join(root, f))
                
    logger.info(f"Found {len(image_paths)} images in {raw_dir}")
    
    # Parse metadata for all images
    rows = []
    for path in image_paths:
        try:
            row = parse_image_metadata(path, dataset_name, gender_map)
            rows.append(row)
        except Exception as e:
            logger.error(f"Error parsing metadata for {path}: {e}")
            
    if not rows:
        raise ValueError(f"No valid image metadata parsed in {raw_dir}")
        
    df = pd.DataFrame(rows)
    
    # Add class_id: mapping palm_id to integer labels sorted alphabetically
    unique_palms = sorted(df["palm_id"].unique())
    palm_to_class = {palm: idx for idx, palm in enumerate(unique_palms)}
    df["class_id"] = df["palm_id"].map(palm_to_class)
    
    # Reorder columns to match unified schema
    df = df[METADATA_COLUMNS]
    
    return df
