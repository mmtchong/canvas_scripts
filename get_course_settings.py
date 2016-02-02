# GET the tabs (left navigation items) from a course from the Canvas API
# what we will do: given a list of courses, search each course for a left navigation item "syllabus", and find the visiblity setting

import requests
import json
import csv
import operator
from course_list import course_list
from secure import oauth_token

#course_list = [59, 6878]
# list of courses

data = []
# list of data we want from the API call
counter = 0
for course_id in course_list:
    # loop over all of the courses in the course list
    url = 'https://harvard.instructure.com/api/v1/courses/%s/tabs' % str(course_id)

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
    	tab_id = position.get('id')
    	# position.get('id') will return none if there none
    	# we're only interested in the syllabus tabs, so when we find those, get the visibility
    	if tab_id == 'syllabus':
    		tab_visibility = position.get('visibility')
    		# append the course id, tab id, and visibility settings to data
    		# note that visibility of public means students can see it and admins is staff only
	    	data.append([course_id, tab_id, tab_visibility])
    counter = counter + 1
    print counter

# Writing the information from data to a CSV file
with open('courses_and_tabs.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(data)