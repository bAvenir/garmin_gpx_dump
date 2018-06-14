#!/usr/bin/python

import sys, getopt, requests, json


def main(argv):
    top_box=0
    bottom_box=0
    left_box=0
    right_box=0
    session_id=''

    try:
        opts, args = getopt.getopt(argv,"ht:b:r:l:s:")
    except getopt.GetoptError:
            print 'garmin_gpx_dump.py -t <top> -b <bottom> -r <right> -l <left> -s <session>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'garmin_gpx_dump.py -t <top> -b <bottom> -r <right> -l <left> -s <session>'
            sys.exit()
        elif opt == '-t':
            top_box =  arg
        elif opt == '-b':
            bottom_box = arg
        elif opt == '-l':
            left_box = arg
        elif opt == '-r':
            right_box = arg
        elif opt == '-s':
            session_id = arg
    print 'Top box: ', top_box
    print 'Bottom box: ', bottom_box
    print 'Left box: ', left_box
    print 'Right box:', right_box
    print 'Session id:', session_id
    garminTrackList = getTracks(top_box, bottom_box, left_box, right_box, session_id)
    bikeTrackIds = getBikeTracksIds(garminTrackList)
    dumpTracks(bikeTrackIds)

def dumpTracks(bikeTrackIds):
    for id in bikeTrackIds:
        url = "https://connect.garmin.com/modern/proxy/course-service/course/gpx/" + str(id)
        print 'Downloading: ' + url

        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "517d3088-c734-4739-a45c-21ca3ed6bb99"
            }

        response = requests.request("GET", url, headers=headers)

        with open('garminTrack_' + str(id) + ".xml", 'w') as f:
            for block in response.iter_content(1024):
                f.write(block)

def getBikeTracksIds(garminTrackList):
    "This extracts the ids from garming track lists"
    print 'Track found: ', len(garminTrackList['courseSummaryDTOs'])
    trackIds = []
    for track in garminTrackList['courseSummaryDTOs']:
        typeId = track['activityType']['typeId']
        if typeId == 5 or typeId == 10:
            trackIds.append(track['courseId'])
            print track['courseId'], track['activityType']['typeId']
    return trackIds


def getTracks(top_box, bottom_box, left_box, right_box, session_id):
    "This downloads list of tracks in given box under given session id"
    print'Downloading file list ...'
    url = "https://connect.garmin.com/modern/proxy/course-service/course/search"

    querystring = {"north":top_box,"south":bottom_box,"east":right_box,"west":left_box,"size":"200"}

    headers = {
        'cookie': "GarminNoCache=true; SESSIONID="+session_id+";",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        'nk': "NT",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'referer': "https://connect.garmin.com/modern/courses",
        'authority': "connect.garmin.com",
        'x-requested-with': "XMLHttpRequest",
        'x-app-ver': "4.7.2.0",
        'x-lang': "en-US",
        'Cache-Control': "no-cache",
        'Postman-Token': "270df8a9-6b70-42bd-8afb-5d1a6e184780"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    garminTrackList = json.loads(response.text)
    print 'done'
    return garminTrackList

if __name__ == "__main__":
    main(sys.argv[1:])
