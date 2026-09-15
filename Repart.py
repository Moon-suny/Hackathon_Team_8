import random
import shutil
from pathlib import Path

random.seed(42)  # pour reproductibilité

data_dir = Path("data")
splits = ["train", "val", "test"]

img_dirs = {s: data_dir / "images" / s for s in splits}
lbl_dirs = {s: data_dir / "labels" / s for s in splits}

# S'assure que tous les dossiers existent
for s in splits:
    img_dirs[s].mkdir(parents=True, exist_ok=True)
    lbl_dirs[s].mkdir(parents=True, exist_ok=True)

# --- 1) Collecte de TOUTES les images annotées, peu importe leur dossier actuel ---
all_pairs = []  # liste de (image_path, label_path)

for s in splits:
    for img_path in sorted(img_dirs[s].glob("*.*")):
        lbl_path = lbl_dirs[s] / f"{img_path.stem}.txt"
        if lbl_path.exists():
            all_pairs.append((img_path, lbl_path))

print(f"Total d'images annotées trouvées (tous dossiers confondus) : {len(all_pairs)}")

if not all_pairs:
    raise SystemExit("Aucune image annotée trouvée, vérifie tes dossiers data/images/* et data/labels/*")

# --- 2) Mélange et calcul des tailles de split ---
random.shuffle(all_pairs)

n_total = len(all_pairs)
n_train = int(n_total * 0.6)
n_val = int(n_total * 0.2)
# le reste va dans test, pour ne perdre aucune image à cause des arrondis
n_test = n_total - n_train - n_val

split_assignment = (
    [("train", p) for p in all_pairs[:n_train]]
    + [("val", p) for p in all_pairs[n_train:n_train + n_val]]
    + [("test", p) for p in all_pairs[n_train + n_val:]]
)

# --- 3) Déplacement vers un dossier temporaire pour éviter les collisions de noms ---
# (utile si deux fichiers différents ont le même nom dans train/ et val/ actuellement)
tmp_dir = data_dir / "_tmp_reshuffle"
tmp_img = tmp_dir / "images"
tmp_lbl = tmp_dir / "labels"
tmp_img.mkdir(parents=True, exist_ok=True)
tmp_lbl.mkdir(parents=True, exist_ok=True)

for i, (split_name, (img_path, lbl_path)) in enumerate(split_assignment):
    new_img = tmp_img / img_path.name
    new_lbl = tmp_lbl / lbl_path.name
    shutil.move(str(img_path), str(new_img))
    shutil.move(str(lbl_path), str(new_lbl))
    split_assignment[i] = (split_name, (new_img, new_lbl))

# --- 4) Nettoyage des anciens dossiers (maintenant vides ou presque) ---
for s in splits:
    for f in img_dirs[s].glob("*.*"):
        f.unlink()
    for f in lbl_dirs[s].glob("*.*"):
        f.unlink()

# --- 5) Déplacement final vers train/val/test ---
counts = {"train": 0, "val": 0, "test": 0}
for split_name, (img_path, lbl_path) in split_assignment:
    shutil.move(str(img_path), str(img_dirs[split_name] / img_path.name))
    shutil.move(str(lbl_path), str(lbl_dirs[split_name] / lbl_path.name))
    counts[split_name] += 1

shutil.rmtree(tmp_dir)

print(f"Répartition finale : train={counts['train']}, val={counts['val']}, test={counts['test']}")