# Create your views here.

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response
import flickr_badges.scripts.get_photos as get_photos

def index(request):
    return render_to_response("index.html")
    
def fb(request):
    username = request.POST['flickrid']
    profile = get_photos.user_profile(username)
    nsid = profile['user_id']
    
    social_count = get_photos.get_contacts(nsid)[0]
    
    if not profile['location']:
        profile['location'] = "an unknown place"

    return render_to_response("fb.html", {
        "username": username, 
        "guy_name": profile['realname'],
        "nsid": profile['user_id'],
        "location": profile['location'],
        "buddyurl": profile['buddyiconurl'],
        "is_pro": not(profile['is_pro'] == 0),
        "early": profile['firstdate'] <= 2005,
        "social": social_count > 100,
        "introv": social_count < 2,
        })
