tuple_dict = [{'Field': 'user_id', 'Type': 'bigint(20)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': 'auto_increment'}, {'Field': 'user_name', 'Type': 'bigint(45)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': ''}, {'Field': 'user_email', 'Type': 'varchar(45)', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}, {'Field': 'user_password', 'Type': 'varchar(255)', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}]

for k in tuple_dict:
    if k['Field'] == 'user_id':
        print(k['Type'])

print(next((item['Type'] for item in tuple_dict if item["Field"] == "user_id"), None))

my_dict = [
    {"name": "Tom", "age": 10},
    {"name": "Mark", "age": 5},
    {"name": "Pam", "age": 7}
]

print(next(filter(lambda obj: obj.get('name') == 'Pam', my_dict), None))