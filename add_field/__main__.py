import argparse
from pathlib import Path


file = Path(__file__)
file_dir = file.parent
getter_pattern_path = file_dir / 'getter_pattern.txt'
setter_pattern_path = file_dir / 'setter_pattern.txt'


parser = argparse.ArgumentParser(description="some command")
parser.add_argument('model_path', type=str)
parser.add_argument('field_name', type=str)
parser.add_argument('field_type', type=str)
parser.add_argument('-g', '--getter',
                    action='store_true')
parser.add_argument('-s', '--setter',
                    action='store_true')
parser.add_argument('-p', '--protacted',
                    action='store_true')
args = parser.parse_args()


model_path = Path(args.model_path)
field_name = args.field_name
field_type = args.field_type
true_field_name = field_name

if not args.getter and args.setter:
    raise Exception("Setter must be with getter! Add -g to the command.")

if args.protacted: true_field_name = '_' + field_name
elif args.getter or args.setter: true_field_name = '__' + field_name

with open(model_path) as f:
    result = ''
    for line in f.readlines():
        result += line
        if f'class {model_path.stem}' in line:
            result += f'    {true_field_name}:{field_type}\n'

print(result)

with open(model_path, 'w') as f:
    f.write(result)

if args.getter:
    with open(getter_pattern_path) as f:
        getter_pattern = f.read()

    with open(model_path, 'a') as f:
        print(getter_pattern.format(field_name=field_name, true_field_name=true_field_name, field_type=field_type))
        f.write(getter_pattern.format(field_name=field_name, true_field_name=true_field_name, field_type=field_type))

if args.setter: 
    with open(setter_pattern_path) as f:
        setter_pattern = f.read()

    with open(model_path, 'a') as f:
        print(setter_pattern.format(field_name=field_name, true_field_name=true_field_name, field_type=field_type))
        f.write(setter_pattern.format(field_name=field_name, true_field_name=true_field_name, field_type=field_type))
    