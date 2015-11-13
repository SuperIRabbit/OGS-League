# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib2 import urlopen
    from urllib2 import HTTPError, URLError
except ImportError:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError

import codecs
import time
import json
import sys
import os
import os.path

def get_page_with_wait(url, wait=3, max_retries=1, current_retry_count=0):
    if wait < 0.01:
        wait = 0.01

    try:
        time.sleep(wait)
        response = urlopen(url)
    except HTTPError as e:
        if e.code == 429:  # too many requests
            print("Too many requests / minute, falling back to {} seconds between fetches.".format(int(1.5 * wait)))
            # exponential falloff
            return get_page_with_wait(url, wait=(1.5 * wait))
        raise
    except URLError as e:
        # sometimes DNS or the network temporarily falls over, and will come back if we try again
        if current_retry_count < max_retries:
            return get_page_with_wait(url, 5, current_retry_count=current_retry_count + 1)  # Wait 5 seconds between retries
        print("Can't fetch '{}'.  Check your network connection.".format(url))
        raise
    else:
        return response.read()

def results(url):
    while url is not None:
        data = json.loads(get_page_with_wait(url, 0).decode('utf-8'))

        for r in data["results"]:
            yield r
        url = data["next"]
        
def tournament_users(tournament_id):
    url = "https://online-go.com/api/v1/tournaments/{}/players/?ordering=player&format=json".format(tournament_id)
    for r in results(url):
        yield r["player"]

if __name__ == "__main__":
    
    f1 = codecs.open("current_ids.txt", "w", "utf-8");
    f2 = codecs.open("current_names.txt", "w", "utf-8");
    f3 = codecs.open("current_ratings.txt", "w", "utf-8");
    
    for u in tournament_users('10864'):
        f1.write("{}\n".format(u["id"]))
        f2.write("{}\n".format(u["username"]))
        f3.write("{}\n".format(u["rating"]))

    f1.close()
    f2.close()
    f3.close()
    
    f1 = codecs.open("previous_ids.txt", "w", "utf-8");

    for u in tournament_users('2475'):
        f1.write("{}\n".format(u["id"]))

    f1.close()
"""
    fh = codecs.open("players.txt", "w", "utf-8")
   
    for u in tournament_usernames('10864'):
        #print("User: {}".format(u));
        #fh.write("{}\n".format(len(u)))
        fh.write("{}\n".format(u))

    fh.close()
"""
"""
    for g in user_games(sys.argv[1]):
        save_sgf(os.path.join(dest_dir, "OGS_game_{}.sgf".format(g)),
                 "https://online-go.com/api/v1/games/{}/sgf".format(g),
                 "game {}".format(g))
        for r in reviews_for_game(g):
            save_sgf(os.path.join(dest_dir, "OGS_game_{}_review_{}.sgf".format(g, r)),
                     "https://online-go.com/api/v1/reviews/{}/sgf".format(g),
                     "review {} of game {}".format(r, g))

    for r, g in user_reviews(sys.argv[1]):
            save_sgf(os.path.join(dest_dir, "OGS_game_{}_review_{}.sgf".format(g, r)),
                     "https://online-go.com/api/v1/reviews/{}/sgf".format(g),
                     "review {} of game {}".format(r, g))
"""
