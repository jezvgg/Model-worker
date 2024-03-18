import click
from pathlib import Path


file = Path(__file__)
file_dir = file.parent
cwd = Path.cwd().resolve()
patterns_path = file_dir / 'patterns'


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('model_path', type=str)
@click.option('--ref', 'referance', type=str)
@click.option('--patterns', 'patterns', type=str)
@click.option('-f', '--field', 'fields', multiple=True, type=(str, str, str))
def main(model_path: str, referance: str, patterns: str, fields):
    model_path = Path(model_path).resolve()
    model_name = model_path.stem
    _patterns_path = patterns_path
    class_kwargs = {'className':model_name}
    if patterns:
        _patterns_path = Path(patterns)
    class_pattern = _patterns_path / 'default_pattern.txt'
    if referance:
        referance = Path(referance).resolve()
        referance_model = referance.stem
        import_path = Path('/'.join(referance.parts[len(cwd.parts)-1:]))
        class_pattern = _patterns_path / 'import_pattern.txt'
        class_kwargs['referance_path'] = '.'.join(import_path.parts)
        class_kwargs['referance'] = referance_model


    with open(class_pattern) as f:
        pattern = f.read()

    pattern = pattern.format(**class_kwargs)

    with open(file_dir / 'patterns' / 'getter_pattern.txt') as f:
        getter_pattern = f.read()

    with open(file_dir / 'patterns' / 'setter_pattern.txt') as f:
        setter_pattern = f.read()

    fields_pattern = ''
    init_pattern = '    def __init__(self):\n'
    setters_and_getters = ''
    for field in fields:
        class_field = ''
        if 'g' in field[0]:
            class_field = '__' + field[1]
            setters_and_getters += getter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)
        if 's' in field[0]:
            setters_and_getters += setter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)
        if 'p' in field[0] :
            class_field = '_' + field[1]
        fields_pattern += f'    {class_field}: {field[2]}\n'
        init_pattern = init_pattern.replace(')',  f', {field[1]}: {field[2]})')
        init_pattern += f'      self.{class_field}: {field[2]} = {field[1]}\n'


    result = ''
    for line in pattern.split('\n'):
        if f'class {model_name}' in line:
            result += line + '\n'
            result += fields_pattern

        elif '   def __init__' in line:
            result += init_pattern

        else: result += line + '\n'

    result += setters_and_getters

    with open(model_path, 'w') as f:
        f.write(result)

    click.echo('Model created!')


if __name__ == '__main__':
    main()