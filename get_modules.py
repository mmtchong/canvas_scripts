# GET the tabs (left navigation items) from a course from the Canvas API
# what we will do: given a list of courses, search each course for a left navigation item "syllabus", and find the visiblity setting

import requests
import json
import csv
import operator
#from course_list import course_list
from secure import oauth_token
# oauth_token is the oauth token from Canvas generated by a user with privileges for the courses

course_list = []
# INSERT HERE list of courses

data = []
# list of data we want from the API call
counter = 0
new_counter = 0
for course_id in course_list:
    # loop over all of the courses in the course list
    url = 'https://harvard.instructure.com/api/v1/courses/%s/modules' % str(course_id)

    # call the API and reaise exceptions as needed
    headers = {
        'Authorization': 'Bearer {}'.format(oauth_token),
    }

    try: 
        resp = requests.get(url, headers=headers )
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print e
        raise

    # save json response as a list of objects
    api_response = resp.json()

    # go through each json object 
    for position in api_response:
    	module_id = position.get('id')
    	# position.get('id') will return none if there none
    	# looking for all of the module ids
    	data.append([course_id, module_id])
    counter = counter + 1
    print counter

    
# Writing the information from data to a CSV file
with open('modules.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(data)
