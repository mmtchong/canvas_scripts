# Edit module items from a spreadsheet using the Canvas API, given a spreadsheet with module items ids

import requests
import json
import csv
import operator
import urllib
import time
timestr = time.strftime("%Y-%m-%d")
#from course_list import course_list
from secure import oauth_token
# oauth_token is the oauth token from Canvas generated by a user with privileges for the courses

data = []
counter = 0

with open('module_items.csv', 'rb') as csvfile:
    # spreadsheet created by get_modules.py
    reader = csv.reader(csvfile)
    for row in reader:
    # loop over each row in the spreadsheet (module in a course)
        course_id = row[0]
        module_id = row[1]
        module_item_id = row[2]
        link = urllib.quote_plus(row[3])

        url = 'https://harvard.instructure.com/api/v1/courses/%s/modules/%s/items/%s?module_item[external_url]=%s' % (str(course_id), str(module_id), str(module_item_id), str(link))
        # call the API and reaise exceptions as needed
        headers = {
            'Authorization': 'Bearer {}'.format(oauth_token),
        }

        try: 
            resp = requests.put(url, headers=headers )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print e
            raise

        data.append([course_id, module_id, module_item_id, link])
        counter = counter + 1
        print counter

    
# Writing the information from data to a CSV file
with open('module_items_edited_%s.csv' % str(timestr), 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(data)
