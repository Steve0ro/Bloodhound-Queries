import json

def remove_duplicates(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    seen = set()
    unique_data = []

    for entry in data:
        key = (entry.get('name'), entry.get('query'))
        if key not in seen:
            seen.add(key)
            unique_data.append(entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, indent=4)

    print(f"Cleaned data saved to {output_file}")


remove_duplicates('json_with_dups.json', 'cleaned_file.json')
