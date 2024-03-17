import argparse
from pathlib import Path

file = Path(__file__)
file_dir = file.parent
choices = [filename.name for filename in file_dir.iterdir() if not filename.name.startswith('_')]
default_pattern = file_dir / 'default_pattern.txt'

parser = argparse.ArgumentParser(description="some command")
parser.add_argument('model_path', type=str)
parser.add_argument('--referance', type=str)
parser.add_argument('--pattern', type=str, choices=choices, default=default_pattern)
args = parser.parse_args()

model_path = Path(args.model_path)
model_name = model_path.stem
kwargs = {'className':model_name}
pattern = args.pattern
if args.referance:
    referance = Path(args.referance)
    referance_class = referance.stem
    referance_import = '.'.join(referance.with_suffix('').parts)
    kwargs['referance_path'] = referance_import
    kwargs['referance'] = referance_class
    pattern = file_dir / 'import_pattern.txt'


with open(pattern) as f:
    st = f.read()


with open(args.model_path, 'w') as f:
    f.write(st.format(**kwargs))

print('model created!')