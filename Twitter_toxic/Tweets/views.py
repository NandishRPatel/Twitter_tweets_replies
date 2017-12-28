from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import tweepy,json
from Tweets.models import Tweets
hash_list=Tweets.objects.values_list('Hashtag')
#print(hash_list)
# Create your views here.

ckey = "0HbmxMUQ5DczFuKbpUt1WFQA9"
csecret = "LjC1kTMY3LrnzBX8cMZrhTWLXXDRLBCa4ZSfXMwO42244V6O5U"
atoken = "2516974466-EyjU0m1wGFYJpYXoi88SGZQTtHk3PEtrkUdE4OK"
asecret = "VZGEEkH7HiytC3abwrTpTDmONsJ7SWbJkHD8XdjGSSzfF"
auth = tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

def index(request):
    template = loader.get_template('form.html')
    return HttpResponse(template.render({},request))

def form_result(request):
    global hash_list
    hash_list = Tweets.objects.values_list('Hashtag')
    #print(hash_list)
    #print("hashlist",hash_list[0].Hashtag)
    if request.GET['hashtag']:
        message=''
        hashtag=request.GET['hashtag']
        if (hashtag,) in hash_list : Tweets.objects.filter(Hashtag=hashtag).delete();#print("del")
        else : pass
        try:all_tweets = tweepy.Cursor(api.search, q=hashtag+' -filter:retweets', tweet_mode='extended').items(100)
        except:print("error")
        d={}
        cnt=0
        for t in all_tweets:
            cnt+=1
            d['tweet_' + str(cnt)] = t._json
        #print(d)
        dump_d=json.dumps(d)
        #print(type(dump_d))
        json_d=json.loads(dump_d)
        print(json_d)
        if json_d:
            x = ""
            for i in json_d:
                x+=str(i)
                x+="<br/>"
                x+=json_d[i]['user']['screen_name']
                x+=" : "
                x+=json_d[i]['full_text']
                x+="<br/>"
                x+="<a href=\\tweets\search_res\\"+str(i)+"\\"+json_d[i]['user']['screen_name']+"\\"+json_d[i]['id_str']+">Replies</a>"
                x+="<br/><br/>"
                list = json_d[i]['created_at'].split()
                #print(type(json_d[i]['lang']), list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1],
                 #     json_d[i]['full_text'], json_d[i]['favorite_count'], json_d[i]['retweet_count'])
                Tweets(Hashtag=hashtag,Lang=str(json_d[i]['lang']),Day_time_date=list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1],Text=json_d[i]['full_text'],Fav_count=json_d[i]['favorite_count'],Ret_count=json_d[i]['retweet_count']).save()
            message+=x
        else:message+="<h3>No tweets of a hashtag</h3>"


    else:
        message = "<script>alert('Empty');</script>"

    return HttpResponse("<h1>Tweets</h1><br/><br/><br/>"+message)


def reply_result(request):
    messege=""
    id=(str(request.get_full_path()).split('/'))[-1]
    name=(str(request.get_full_path()).split('/'))[-2]
    try:replies=tweepy.Cursor(api.search, q=name ,since_id=int(id), tweet_mode='extended').items()
    except:print("error")
    for r in replies:
        if r._json["in_reply_to_status_id"] == int(id):
            #print("-------------yeeeeeeees------------------")
            messege+=r._json['user']['screen_name']
            messege+=" : "
            messege+=r._json['full_text']
            messege+="<br/><br/>"
        else:pass
    if messege:pass
    else:messege+="<h3>No replies of this Tweet</h3>"
    return HttpResponse("<h1>Replies</h1><br/><br/><br/>"+messege)




