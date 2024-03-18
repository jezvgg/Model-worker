At first, you need to build projact.
```
pip install --editable .
```

Now, command to create your model:
```
mw {model_path} --ref={referance_model_path} [-f{gsp} {field_name} {field_type}...]
```
You can create model with fields, when you initialize field, you need to write -f.

If you want to add modificator to the field you can write:
- -p - to create protacted field
- -g - to create getter to the field
- -s - to create setter to the field
