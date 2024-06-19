import click
from pathlib import Path


file = Path(__file__)
file_dir = file.parent
cwd = Path.cwd().resolve()
patterns_path = file_dir / 'patterns'


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('model_path', type=str)
#Имя модели 
@click.option('--ref', 'referance', type=str)
#Класс наследоваия модели 
@click.option('--patterns', 'patterns', type=str)

@click.option('-f', '--field', 'fields', multiple=True, type=(str, str, str))
#Поля класса 
 
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
        import_path = Path('/'.join(referance.with_suffix('').parts[len(cwd.parts):]))
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
    setters_and_getters = ''
    for field in fields:

        #Проверка на то публичный класс или нет
        if "_" in field[0]:
            class_field = field[1]
            
            #Проверка на значение по умолчанию
            if 'n' in field[0]:
                fields_pattern += f'    {class_field}: {field[2]}=None\n'
            else:
                fields_pattern += f'    {class_field}: {field[2]}\n'
        else:
            #Проверка на протектед 
            if 'p' in field[0] :
                class_field = '_' + field[1]

                #Проверка на геттер 
                if 'g' in field[0]:
                    class_field = '_' + field[1]
                    setters_and_getters += getter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)

                #Проверка на сеттер 
                if 's' in field[0]:
                    setters_and_getters += setter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)

                #Проверка на значение по умолчанию
                if 'n' in field[0]:
                    fields_pattern += f'    {class_field}: {field[2]}=None\n'
                else:
                    fields_pattern += f'    {class_field}: {field[2]}\n'
            else:
                class_field = '__' + field[1]
                
                #Проверка на геттер 
                if 'g' in field[0]:
                    class_field = '__' + field[1]
                    setters_and_getters += getter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)
                
                #Проверка на сеттер 
                if 's' in field[0]:
                    class_field = '__' + field[1]
                    setters_and_getters += setter_pattern.format(field_name=field[1], field_type=field[2], true_field_name=class_field)
                
                #Проверка на значение по умолчанию
                if 'n' in field[0]:
                    fields_pattern += f'    {class_field}: {field[2]}=None\n'
                else:
                    fields_pattern += f'    {class_field}: {field[2]}\n'

        

    result = ''
    for line in pattern.split('\n'):
        if f'class {model_name}' in line:
            result += line + '\n'
            result += fields_pattern

        else: result += line + '\n'

    result += setters_and_getters

    with open(model_path, 'w') as f:
        f.write(result)

    click.echo('Model created!')