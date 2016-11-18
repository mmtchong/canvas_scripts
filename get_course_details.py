# GET details for a course from the Canvas API

import requests
import json
import csv
import operator
import time
from course_list import dce_course_list, hks_course_list, hsph_course_list, hds_course_list, gse_course_list, fas_course_list, gsd_course_list, hls_course_list
from secure import oauth_token
timestr = time.strftime("%Y-%m-%d")
data = []
# list of data we want from the API call
counter = 0

list_input = raw_input('school: ')

if list_input == 'hks':
	course_list = hks_course_list
elif list_input == 'hsph':
	course_list = hsph_course_list
elif list_input == 'hds':
	course_list = hds_course_list
elif list_input == 'gse':
	course_list = gse_course_list
elif list_input == 'fas':
	course_list = fas_course_list
elif list_input == 'gsd':
	course_list = gsd_course_list
elif list_input == 'hls':
	course_list = hls_course_list
elif list_input == 'dce':
    course_list = dce_course_list
else:
	raise
print course_list
print len(course_list)
for course_id in course_list:
    # loop over all of the courses in the course list
#    url = 'https://harvard.instructure.com/api/v1/courses/%s?include=storage_quota_used_mb' % str(course_id)
    url = 'https://harvard.instructure.com/api/v1/courses/sis_course_id:%s?include=storage_quota_used_mb' % str(course_id)

    # call the API and raise exceptions as needed
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

    course_id = api_response.get('id')
	# position.get('id') will return none if there none
    sis_course_id = api_response.get('sis_course_id')
#    course_name = api_response.get('name')
#    course_code = api_response.get('course_code')
    workflow_state = api_response.get('workflow_state')
    account_id = api_response.get('account_id')
    enrollment_term_id = api_response.get('enrollment_term_id')
    default_view = api_response.get('default_view')
    public = api_response.get('is_public')
    auth_users = api_response.get('is_public_to_auth_users')
    public_syllabus = api_response.get('public_syllabus')
    storage_quota_mb = api_response.get('storage_quota_mb')
    storage_quota_used_mb = api_response.get('storage_quota_used_mb')
    hide_final_grades = api_response.get('hide_final_grades')
#    data.append([course_name, course_code, sis_course_id, course_id, workflow_state, account_id, enrollment_term_id, default_view, public, auth_users, public_syllabus, storage_quota_mb, storage_quota_used_mb, hide_final_grades])
    data.append([sis_course_id, course_id, workflow_state, account_id, enrollment_term_id, default_view, public, auth_users, public_syllabus, storage_quota_mb, storage_quota_used_mb, hide_final_grades])

    counter = counter + 1
    print counter
#data=[('%s').encode('latin-1') for a in data]
# Writing the information from data to a CSV file
with open('%s_course_information_%s.csv' % (list_input, str(timestr)), 'wb') as f:
    writer = csv.writer(f)
#    writer.writerow(['course_name', 'course_code', 'sis_course_id', 'canvas_course_id', 'workflow_state', 'account_id', 'canvas_enrollment_term_id', 'homepage_type', 'public course', 'course open to auth users', 'public syllabus', 'storage_quota_mb', 'storage_quota_used_mb', 'hide_final_grades'])
    writer.writerow(['sis_course_id', 'canvas_course_id', 'workflow_state', 'account_id', 'canvas_enrollment_term_id', 'homepage_type', 'public course', 'course open to auth users', 'public syllabus', 'storage_quota_mb', 'storage_quota_used_mb', 'hide_final_grades'])
    writer.writerows(data)