# SDK script to get the numbers of page views and participations in a Canvas course from analytics using the SDK
import csv
from canvas_sdk import RequestContext
from pprint import pprint
from canvas_sdk.methods import analytics
from canvas_sdk.utils import get_all_list_data
from secure import oauth_token

data=[]

canvas_url = 'https://canvas.harvard.edu/api/'  # for production

SDK_CONTEXT = RequestContext(oauth_token, canvas_url)
# use the SDK to make the request to the Canvas API to the canvas instance defined in canvas_url

response = get_all_list_data(SDK_CONTEXT, analytics.get_course_level_student_summary_data, course_id=495)
# save the response from the SDK call for a particular course_id
# use the API to get move through all pages

length = len(response)

# save the id, participation, and page_view data from the response
for c in range(0,length):
	print c
	user_id = response[c]['id']
	participations = response[c]['participations']
	page_views = response[c]['page_views']
	data.append([user_id, participations, page_views])

# write the data saved from the response to a CSV
with open('analytics.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['canvas_user_id','participations','page_views'])
    writer.writerows(data)