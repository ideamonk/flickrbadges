# Create your views here.
import yql
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
    
    social_count, contact_ids = get_photos.get_contacts(nsid)
    pro_count = get_photos.get_pro_friends(nsid, contact_ids, yql.Public())
    
    eliteness = 0.0
    if social_count > 0:
        eliteness = float(pro_count)/ float(social_count) 
    
    org_stats = get_photos.get_organization_stats(nsid, profile['total_photos'])
    
    if not profile['location']:
        profile['location'] = "an unknown place"

    movement = get_photos.get_geo_locs(nsid, yql.Public())
    
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
        "elite": eliteness > 0.5 and (not(profile['is_pro'] == 0)) and social_count>10,
        "pop": org_stats['avg_views'] > 10,
        "org": org_stats['organized'] > 0.66,
        "travel": movement >= 2,
        "globe": movement >= 5,
        })
