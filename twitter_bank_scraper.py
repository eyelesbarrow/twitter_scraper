
import tweepy


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
  
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
 
user = api.get_user("CouttsandCo")  #Put Twitter handle here, for example @CouttsandCo, but without the @
 
 
def get_all_tweets(user_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
     
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
 
 
 
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
 
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = user_name, count=200,  include_RTs=True, in_reply_to_screen_name=True, is_quote_status=True, include_Favorites=True)
    # if we want to add more parameters to the user_timeline, the list of parameters are at: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
 
    #save most recent tweets
    alltweets.extend(new_tweets)
    #alltweets.append(mentions)
 
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id-1
 
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #print ("getting tweets before %s" % (oldest))
 
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = user_name,count=200, max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #all_tweets.append(mentions)
 
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id-1
 
        #print "...%s tweets downloaded so far" + (len(alltweets))
 
    #transform the tweepy tweets into a 2D array that will populate the csv. Here, we also add the parameters that we included in the user_timeline
    outtweets = [[tweet.id_str, user.screen_name, tweet.created_at, tweet.text.encode("utf-8"), tweet.source, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.is_quote_status] for tweet in alltweets]
 
    with open('%s_tweets.csv' % user_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "screen_name", "date","text", "source", "number_of_favorites", "number_of_rt", "reply_to", "is_quote"]) #here are the names of the columns in our dataframe
        writer.writerows(outtweets)
 
    pass
 
 
if __name__ == '__main__':
    #pass in the username of the account you want to download
        get_all_tweets("CouttsandCo")
 
    
