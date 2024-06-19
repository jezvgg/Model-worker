At first, you need to build projact.
```
pip install --editable .
```

Now, command to create your model:
```
mw <model_path> --ref=<referance_model_path> -f <modificator> <field_name> <field_type> -f <_n> <field_name2> <field_type>...
```
You can create model with fields, when you initialize field, you need to write -f.

If you want to add modificator to the field you can write:
- -_ - to create public field
- -p - to create protacted field
- -g - to create getter to the field and field will be privat
- -s - to create setter to the field abd field will be privat
- -n - to create field with default value = None 
