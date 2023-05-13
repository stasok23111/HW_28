import csv
import json


def converter(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            if 'location_id' in row:
                row['locations'] = [row['location_id']]
                del row['location_id']

            result.append({'model': model, 'fields': row})

    with open(json_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':

    converter('ad.csv', 'ad.json', 'ads.ad')
    converter('category.csv', 'category.json', 'ads.category')
    converter('location.csv', 'location.json', 'users.location')
    converter('user.csv', 'user.json', 'users.user')