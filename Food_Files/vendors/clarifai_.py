from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# this can be taken as its own if needed.
def call_vision_api(image_filename):
    """
    This function calls the Clarifai API on the provided image.

    Arguments:
        An image file, identified by the image's name.
    Returns:
        A response in JSON to be parsed by get_standardized_result().
    """
    app = ClarifaiApp()
    model = app.models.get('food-items-v1.0')
    image = ClImage(file_obj=open(image_filename, 'rb'))
    result = model.predict([image])
    return result


def get_standardized_result(api_result):
    """
    This function parses the response of Clarifai's image processing API call.

    Arguments:
        api_result, which is the response from making an API call.
    Returns:
        A dictionary which associates the recommended labels (as values) with the image names (as keys).
    """
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
    #print(output['tags'])
    # a dictionary which contains unnecessary or vague recommendations. Used to filter the responses to the user.
    not_specific_ingredients = {'food', 'comestible', 'grass', 'aliment', 'salad', 'pasture', 'vegetable', 'sweet', 'legume', 'dessert', 'berry', 'juice', 'meat'}
    output_list = list(output['tags'])
    confirm_foods = []
    
    max_recs = 7
    #print ("short list", len(output_list))
    for (food, score) in output_list:
        if food not in not_specific_ingredients and max_recs > 0:
            confirm_foods.append(food)
            max_recs -= 1
    print(confirm_foods)
    return confirm_foods
    #return output
