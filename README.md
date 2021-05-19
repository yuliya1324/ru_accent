# ru_accent_poet

This is a tool for putting stress marks in russian poetic texts 

### Installation
```
pip install ru-accent-poet
```
### Usage example

To put stress marks in text
```
>>> from ru_accent_poet import ru_accent
>>> ru_accent.accent_line('Это инструмент для разметки ударений')
Э'то инструме'нт для разме'тки ударе'ний
```

To put stress marks in files
```
>>> ru_accent.write_file(['my_file_1.txt'])
```

This will return new file called 
"my_file.accented.txt" with the same text 
where stress marks are put
