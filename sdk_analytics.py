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

response = get_all_list_data(SDK_CONTEXT, analytics.get_course_level_student_summary_data, course_id=495)
length = len(response)

for c in range(0,length):
	print c
	user_id = response[c]['id']
	participations = response[c]['participations']
	page_views = response[c]['page_views']
	data.append([user_id, participations, page_views])

with open('analytics.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['canvas_user_id','participations','page_views'])
    writer.writerows(data)