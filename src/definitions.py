import json
import requests
from options import get_options, get_service_options, remove_html_tags
from request_builder import build_packages_request
from main import headers, start_up
sort_by_help_msg, args = start_up()

def get_module_info(module_name):
    """
    THIS FUNCTIONALITY IS ALREADY IN NIXSCRAPER, AVOID REPEATING THIS WORK
    {
        "name": "Metabase",
        "desc": "The easy, open source way for everyone in your company to ask questions and learn from data",
        "tags": [
            "Analytics"
        ],
        "website": "https://metabase.com",
        "implmented": false,
        "logo": "https://metabase.com/images/favicon.ico",
        "specs": {
            "ram": 0,
            "storage": 0
        },
        "nixName": "metabase",
        "options": [
            ...
        ]
    }
    """
    kwargs = vars(args)

    package_json_data = build_packages_request(**kwargs, search_term=module_name)
                
    response = requests.post('https://search.nixos.org/backend/latest-42-nixos-unstable/_search', headers=headers, json=package_json_data)

    print(response.json())
    for hit in response.json()['hits']['hits']:
        try:
            parsed_module_info = parse_module_info(hit)
            print(parsed_module_info)
        except Exception as e:
            print(e)
        if parse_module_info:
            break

def parse_module_info(hit):
    module_info = {
        "name": hit["_source"]["package_pname"],
        "desc": remove_html_tags(hit["_source"]["package_description"]),
    }
    if len(hit["_source"]["package_homepage"])>0:
        module_info["website"] = hit["_source"]["package_homepage"][0]
    if len(hit["_source"]["package_license"])>0:
        module_info["tags"] = hit["_source"]["package_license_set"][0]

    return module_info


def create_module_definitions(option_list):
    # For a list of options, return a list of modules with the same common top and second level name (eg. networking and firewall)
    
    modules = []
    module_definitions = []
    for option in option_list:
        option_split = option["nixName"].split('.')
        if len(option_split) <= 2:
            print(option_split)
            break
        module_type = option_split[0]
        module_name = option_split[1]
        option_name = option_split[2]
        if module_name in modules:
            # Add the option to the existing module's option list
            # module = get_module_info(module_name)
            #print(module_name)
            for mod_def in module_definitions:
                if type(mod_def) is dict:
                    if mod_def["name"] == module_name:
                        mod_def["options"].append(option)
                else:
                    print(mod_def)
            
        else:
            # Create new module with options list containing the option
            print(module_name)
            #module = get_module_info(module_name)
            modules.append(module_name)

            mod_def = {
                "name": module_name,
                "options":[option]
            }

            module_definitions.append(mod_def)


            
    return module_definitions

module_types = ['boot', 'hardware', 'networking', 'programs', 'system', 'virtualisation', 'security']

# The goal for config_definitions is to create a list of modules with a good description typically pulled from the package info and an accurate options list.
config_definitions = {
    "services": create_module_definitions(get_service_options())
}

for m in module_types:
    module_path = f'data/other-modules/{m}.json'
    config_definitions[m] = create_module_definitions(get_options(module_path)) 

def write_svc_defs():
    with open('data/service-definitions.json', 'w') as file:
        file.write(json.dumps(config_definitions, indent=4))

write_svc_defs()