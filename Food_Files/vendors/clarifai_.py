from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# this can be taken as its own if needed.
def call_vision_api(image_filename):
    app = ClarifaiApp()
    model = app.models.get('food-items-v1.0')
    image = ClImage(file_obj=open(image_filename, 'rb'))
    result = model.predict([image])
    return result


def get_standardized_result(api_result):
    output = {
        'tags': []
    }

    concepts = api_result['outputs'][0]['data']['concepts']
    tag_names = []
    tag_scores = []

    for concept in concepts:
        tag_names.append(concept['name'])
        tag_scores.append(concept['value'])

    output['tags'] = zip(tag_names, tag_scores)
    not_specific_ingredients = {'food', 'comestible', 'grass', 'aliment', 'salad', 'pasture', 'vegetable', 'sweet', 'legume', 'dessert', 'berry', 'juice', 'meat'}
    confirm_foods = []
    for (food, score) in list(output['tags']):
        if food not in not_specific_ingredients:
            confirm_foods.append(food)
    #print(confirm_foods)
    return confirm_foods
    #return output
