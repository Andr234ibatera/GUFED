import os 
import pandas as pd

from tqdm import tqdm


GUFED_ROOT_DIR = "../GUFED Images"
PATH = os.path.join(GUFED_ROOT_DIR, "Original")

OUTPUT_DIR = "./data"


paths = list()
for root, _, _ in tqdm(os.walk(PATH, topdown=False), desc="Generating paths"):
    if root.__contains__("Infrared"):
        paths.append(root)
    
for path in tqdm(paths):
    content = os.listdir(path)
    content = list(map(lambda ctt: int(str(ctt).removesuffix(".png")), content))
    content.sort()
    filenames = list(map(lambda ctt: f"{ctt}.png", content))
    # get properties
    pth, image_type = os.path.split(path)
    pth, expression = os.path.split(pth)
    pth, subject = os.path.split(pth)
    # criate default dataframe
    data_size = len(filenames)
    df = pd.DataFrame({
        "subject": [subject]*data_size,
        "expression": [expression]*data_size,
        "filename": filenames,
        "is_neutral": [False]*data_size
    })
    # create cache
    output_path = os.path.join(OUTPUT_DIR, str(subject))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    # store cache
    df.to_csv(os.path.join(output_path, f"{expression}.csv"), index=False)