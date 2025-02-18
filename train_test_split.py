import glob
import random
import os
import shutil

def mkdir_safe(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False

blacklist_data_names = ['train', 'valid']
train_test_split_ratio = 0.1

data_names = [path.split('/')[-1] for path in glob.glob('dataset/*')]
random.shuffle(data_names)

for bl in blacklist_data_names:
    if bl in data_names:
        data_names.remove(bl)
print(data_names[:10])

newton_wood_idx = int(len(data_names) * train_test_split_ratio) + 1

mkdir_safe('./dataset/train')
mkdir_safe('./dataset/valid')


print(newton_wood_idx, len(data_names))

# train
for folder_name in data_names[newton_wood_idx:]:
    shutil.move(f'./dataset/{folder_name}', f'./dataset/train/{folder_name}')

# valid
for folder_name in data_names[:newton_wood_idx]:
    shutil.move(f'./dataset/{folder_name}', f'./dataset/valid/{folder_name}')