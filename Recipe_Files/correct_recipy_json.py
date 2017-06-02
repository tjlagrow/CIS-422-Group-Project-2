import json


jsonFile = open('better_output_of_complex_recipe', 'r')
values = json.load(jsonFile)
for criteria in values['results']:
    for key, value in criteria.items():
        print(key, 'is:', value)
    print('')
    print('')
    print('')
jsonFile.close()