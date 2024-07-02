import json
import re
import html

def remove_html_tags(self,text):
        
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Convert HTML entities to characters
    clean_text = html.unescape(clean_text)
    clean_text = clean_text.replace('\n', '')
    return clean_text.strip()

letters = 'abcdefghijklmnopqrstuvwxyz'
service_list = []

api_definition = {}

for letter in letters:
    with open(f'data/services/{letter}.json', 'r') as file:
        data = json.load(file)
    if data['hits']:
        for hit in data['hits']['hits']:
            serviceName = hit['_source']['option_name']
            serviceName = serviceName.replace('services.', '').split('.')[0]
            service_list.append(serviceName)

api_definition['services'] = service_list

with open('service-definitions.json', 'w') as file:
    file.write(json.dumps(api_definition, indent=4))