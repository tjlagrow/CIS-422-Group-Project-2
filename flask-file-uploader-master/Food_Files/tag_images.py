# Author: Randy Chen
#
# Code adapted from goberoi's CloudyVision. (link: https://github.com/goberoi/cloudy_vision). Many thanks them for 
# providing a way to cache API calls so that no calls are made on duplicate images.
#
# This program will go through photos in a given path and tag them with responses from the Clarifai API.

import json
import os
import time
import vendors.clarifai_


SETTINGS = None
def settings(name):
    """This function will allow us to fetch a settings parameter.
    When working with so many different variables and filepaths, this
    is helpful for keeping track of all the different settings and 
    ensuring that we are working with the correct objects.
    Input:
        name: the name of the setting as a key of a dictionary.
    Output:
        returns SETTING['name'], the value associated with the key 'name'.
    """

    # Initialize settings if necessary.
    global SETTINGS
    if SETTINGS is None:

        # Change this dict to suit your taste.
        SETTINGS = {
            'api_keys_filepath' : './api_keys.json',
            'input_images_dir' : 'Food_Files/input_images',
            'output_dir' : 'Food_Files/output',
            'static_dir' : 'static',
            'output_image_height' : 200,
            'vendors' : {
                'clarifai' : vendors.clarifai_
            },
            'resize': False,
            'statistics': [
                'response_time',
                'tags_count',
            ],
            'tagged_images': False,
            'tags_filepath': './tags.json',
        }
        if SETTINGS['tagged_images']:
            SETTINGS['statistics'] += [
                'matching_tags_count',
                'matching_confidence'
            ]

        # Load API keys
        SETTINGS['api_keys'] = {}

    return SETTINGS[name]


def log_status(filepath, vendor_name, msg):
    """
    This function logs the status of an API call to the console.
    Input:
        filepath: the filepath of the file. Gets us the specific filename we are printing a message for.
        vendor_name: the name of the API used to tag the images. Is Clarifai by default.
        msg: a string in the form of "skipping API call, already cached", or "calling API"
    Output:
        Prints out a message to let the user know about whether the image is new or old, whether a call was made to the API or not. 
    """
    filename = os.path.basename(filepath)
    print("%s -> %s" % ((filename + ", " + vendor_name).ljust(40), msg))


def process_all_images():
    """
    This is the main function. It looks through the images in the input directory and loops through
    various API (default 1 API is used) and calls the API on the images, eventually getting back
    JSON which is written to a .json file to be used by the front end of the application.
    Input:
        Looks in the images located in the directory called 'input_images/' and looks for the API to call
        in the 'vendors/' directory
    Output:
        Writes a .json file into the 'output/' directory, which will be accessed by the application.
    """

    # Read image labels
    if settings('tagged_images'):
        with(open(settings('tags_filepath'), 'r')) as tags_file:
            tags = json.loads(tags_file.read())

    # Create a dictionary to be converted into a .json file after images have been processed.
    recommendations = {}
    # Loop through all input images.
    for filename in os.listdir(settings('input_images_dir')):

        # Only process files that have these image extensions.
        if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Create a full path so we can read these files.
        filepath = os.path.join(settings('input_images_dir'), filename)

        # Read desired tags to compare against if specified
        image_tags = []
        if settings('tagged_images'):
            image_tags = tags.get(filename, [])
        
        vendor_name   = sorted(settings('vendors').items(), reverse=True)[0][0]
        vendor_module = sorted(settings('vendors').items(), reverse=True)[0][1]
        #print(vendor_name, vendor_module)
            
        # Figure out filename to store and retrive cached JSON results.
        output_json_filename = filename + "." + vendor_name + ".json"
        output_json_path = os.path.join(settings('output_dir'), output_json_filename)

        # Check if the call is already cached.
        if os.path.isfile(output_json_path):

            # If so, read the result from the .json file stored in the output dir.
            #pass
            log_status(filepath, vendor_name, "skipping API call, already cached")
            with open(output_json_path, 'r') as infile:
                api_result = json.loads(infile.read())

        else:

            # If not, make the API call for this particular vendor.
            log_status(filepath, vendor_name, "calling API")
            
            api_result = vendor_module.call_vision_api(filepath)

            # And cache the result in a .json file
            log_status(filepath, vendor_name, "success, storing result in %s" % output_json_path)
            with open(output_json_path, 'w') as outfile:
                api_result_str = json.dumps(api_result, sort_keys=True, indent=4, separators=(',', ': '))
                outfile.write(api_result_str)

        # Parse the JSON result we fetched (via API call or from cache)
        standardized_result = vendor_module.get_standardized_result(api_result)
        #print(standardized_result)
        recommendations[filename] = standardized_result
        # Sort tags if found
        if 'tags' in standardized_result:
            sorted(standardized_result['tags'], key=lambda tup: tup[1], reverse=True)
        #print(standardized_result)


    # Write JSON output to be displayed by the application.
    output_json_path = os.path.join(settings('output_dir'), 'foods.json')
    with open(output_json_path, 'w') as outfile:
        api_result_str = json.dumps(recommendations, sort_keys=True, indent=4, separators=(',', ': '))
        outfile.write(api_result_str)

if __name__ == "__main__":
    process_all_images()
