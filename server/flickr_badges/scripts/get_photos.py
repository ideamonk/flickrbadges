import yql
import json
import random
import urllib2

def fetch_info(user_id, y_cursor) :
    
    query = "SELECT id FROM flickr.photos.search WHERE has_geo = 'true' AND user_id = {user}".format(user = user_id)
    print query
    results = y_cursor.execute(query)
    # print results
    print "processing"
    photo_ids = []
    for row in results.rows:
        photo_ids.append([row['id']])
    
    random.shuffle(photo_ids)
    limit = 1
    return [str(x) for [x] in photo_ids[:limit]]


def user_profile(user_name) :
    y_cursor = yql.Public()
    query = "SELECT * FROM flickr.people.info2 WHERE user_id IN (SELECT id FROM flickr.urls.lookupuser WHERE url='http://www.flickr.com/photos/{user}/')".format(user = user_name)
    
    user_data = y_cursor.execute(query).rows[0]
    print user_data
    return {
        'user_id' : user_data['nsid'], 
        'is_pro' : int(user_data['ispro']), 
        'realname' : user_data['realname'] if 'realname' in user_data else user_data['username'], 
        'first_date' : user_data['photos']['firstdatetaken'], 
        'total_photos' : int(user_data['photos']['count']), 
        'location' : user_data['location'] if 'location' in user_data else None, 
        'buddyiconurl' : user_data['buddyiconurl'],
        'firstdate': int(user_data['photos']['firstdatetaken'].split("-")[0]),
    }
    

def get_exifs(pics, y_cursor):
    query = "SELECT * FROM flickr.photos.exif WHERE photo_id IN ({photo_ids})".format(photo_ids = ','.join(pics))
    print query
    pics_data = y_cursor.execute(query)
    
    # print results.rows
    for pic in pics_data.rows :
        for exif_tag in pic[unicode('exif')] :
            # exec "import {}"
            print "{key} : {value}".format(key = exif_tag[unicode('tag')], value = exif_tag[unicode('raw')])

# def get_locations(pics, y_cursor) :
#     query = "SELECT * FROM flickr.photos"

def get_contacts(user_id) :
    url = "http://api.flickr.com/services/rest/?method=flickr.contacts.getPublicList&api_key=5002b5ef867cb59be9f783357b6b49ca&user_id={user_id}&format=json&nojsoncallback=1".format(user_id = user_id)
    
    try:
        data = urllib2.urlopen(url)
    except:
        return (0, False)

    if data :
        sets = json.loads(data.read())
        # print sets
        count = sets['contacts']['total']
        contact_ids = []
        for contact in sets['contacts']['contact']:
            contact_ids.append(str(contact['nsid']))
        return (count, contact_ids)
            
    return (0, False)

def get_pro_friends(user_id, contact_ids, y_cursor) :
    contact_ids = ["'{}'".format(contact_id) for contact_id in contact_ids ]
    query = "SELECT ispro FROM  flickr.people.info2 WHERE user_id IN ({user_ids})".format(user_ids = ','.join(contact_ids))
    print query
    results = y_cursor.execute(query)
    is_pro_count = 0
    for row in results.rows :
        if int(row['ispro']) == 1 :
            is_pro_count += 1

    return is_pro_count

def get_sets(user_id) :
    url = "http://api.flickr.com/services/rest/?method=flickr.photosets.getList&api_key=5002b5ef867cb59be9f783357b6b49ca&user_id={user_id}&format=json&nojsoncallback=1".format(user_id = user_id)
    
    try:
        data = urllib2.urlopen(url)
    except:
        return (0, False)

    if data :
        sets = json.loads(data.read())
        len(sets['photosets']['photoset'])
        # for row in sets['photosets']['photoset'] :
        #     print row
        
    
    return (0, False)

    
def main(user_name) :
    y_cursor = yql.Public()
    user_data = user_profile(user_name)
    print user_data
    #(contacts, contact_ids) =  get_contacts(user_data['user_id'])
    #pro_friends = get_pro_friends(user_data['user_id'], contact_ids, y_cursor)
    get_sets(user_data['user_id'])
    
    # pics = fetch_info(user_name, y_cursor)
    # print pics
    # get_exifs(pics, y_cursor)
    
    
if __name__ == "__main__" :
    # user_name = "t3rmin4t0r"
    user_name = "jass2cool"
    main(user_name)
    #print get_groups('11414938@N00')