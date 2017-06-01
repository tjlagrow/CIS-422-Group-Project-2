from jinja2 import FileSystemLoader, Environment
from shutil import copyfile
import json
import os
import time
#import vendors.google
#import vendors.microsoft
import vendors.clarifai_
#import vendors.ibm
#import vendors.cloudsight_
#import vendors.rekognition


SETTINGS = None
def settings(name):
    """Fetch a settings parameter."""

    # Initialize settings if necessary.
    global SETTINGS
    if SETTINGS is None:

        # Change this dict to suit your taste.
        SETTINGS = {
            'api_keys_filepath' : './api_keys.json',
            # Uncomment for pythonanywhere 
            #'input_images_dir' : '/home/422Hopper/CIS-422-Group-Project-2/flask-file-uploader-master/data/',
            'input_images_dir' : 'input_images',
            'output_dir' : 'output',
            'static_dir' : 'static',
            'output_image_height' : 200,
            'vendors' : {
                #'google' : vendors.google,
                #'msft' : vendors.microsoft,
                'clarifai' : vendors.clarifai_,
                #'ibm' : vendors.ibm,
                #'cloudsight' : vendors.cloudsight_,
                #'rekognition' : vendors.rekognition,
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
        #with open(SETTINGS['api_keys_filepath']) as data_file:
        SETTINGS['api_keys'] = {}

    return SETTINGS[name]


def log_status(filepath, vendor_name, msg):
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

    image_results = []

    # Create the output directory
    """if not os.path.exists(settings('output_dir')):
        os.makedirs(settings('output_dir'))"""

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

        # Create an output object for the image
        image_result = {
            'input_image_filepath' : filepath,
            'output_image_filepath' : filename,
            'vendors' : [],
            'image_tags' : image_tags,
        }
        image_results.append(image_result)
        """
        # not used.
        # If there's no output file, then resize or copy the input file over
        output_image_filepath = os.path.join(settings('output_dir'), filename)
        if not(os.path.isfile(output_image_filepath)):
            log_status(filepath, "", "writing output image in %s" % output_image_filepath)
            if settings('resize'):
                resize_and_save(filepath, output_image_filepath)
            else:
                copyfile(filepath, output_image_filepath)
        """

        # Walk through all vendor APIs to call.
        #for vendor_name, vendor_module in sorted(settings('vendors').items(), reverse=True):
        vendor_name   = sorted(settings('vendors').items(), reverse=True)[0][0]
        vendor_module = sorted(settings('vendors').items(), reverse=True)[0][1]
        #print(vendor_name, vendor_module)
            
        # Figure out filename to store and retrive cached JSON results.
        output_json_filename = filename + "." + vendor_name + ".json"
        output_json_path = os.path.join(settings('output_dir'), output_json_filename)

        # Check if the call is already cached.
        if os.path.isfile(output_json_path):

            # If so, read the result from the .json file stored in the output dir.
            pass
            # log_status(filepath, vendor_name, "skipping API call, already cached")
            #with open(output_json_path, 'r') as infile:
            #    api_result = json.loads(infile.read())

        else:

            # If not, make the API call for this particular vendor.
            log_status(filepath, vendor_name, "calling API")
            api_call_start = time.time()
            api_result = vendor_module.call_vision_api(filepath)
            api_result['response_time'] = time.time() - api_call_start

            # And cache the result in a .json file
            log_status(filepath, vendor_name, "success, storing result in %s" % output_json_path)
            with open(output_json_path, 'w') as outfile:
                api_result_str = json.dumps(api_result, sort_keys=True, indent=4, separators=(',', ': '))
                outfile.write(api_result_str)

            # Sleep so we avoid hitting throttling limits
            #time.sleep(1)

        # Parse the JSON result we fetched (via API call or from cache)
        standardized_result = vendor_module.get_standardized_result(api_result)
        #print(standardized_result)
        recommendations[filename] = standardized_result
        # Sort tags if found
        if 'tags' in standardized_result:
            sorted(standardized_result['tags'], key=lambda tup: tup[1], reverse=True)
        #print(standardized_result)


    # Compute global statistics for each vendor
    #vendor_stats = vendor_statistics(image_results)
    #print(recommendations)
    # Sort image_results output by filename (so that future runs produce comparable output)
    image_results.sort(key=lambda image_result: image_result['output_image_filepath'])
    #print(image_results)
    # Render HTML file with all results.

    # Write HTML output.
    """output_html_filepath = os.path.join(settings('output_dir'), 'output.html')
    with open(output_html_filepath, 'wb') as output_html_file:
        output_html_file.write(output_html.encode('utf-8'))"""

    # Write JSON output.
    output_json_path = os.path.join(settings('output_dir'), 'foods.json')
    with open(output_json_path, 'w') as outfile:
        api_result_str = json.dumps(recommendations, sort_keys=True, indent=4, separators=(',', ': '))
        outfile.write(api_result_str)

if __name__ == "__main__":
    process_all_images()
