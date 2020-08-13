###############################
####        Imports        ####
###############################

from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)
from requests.exceptions import ConnectionError
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from redis import StrictRedis
import requests
import requests_cache
import re
import json
import csv
import os
import time
import config

app = Flask(__name__)

#initialize redis in-memory connection & installing cache for requests
redis = StrictRedis(host='redis', port=6379, db=0)
requests_cache.install_cache(backend='redis', connection=redis, expire_after=600)

# Folder to save the uploaded txt/csv file
UPLOAD_FOLDER = 'Illuma Offline Interview - DevOps/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##################################
#### Scrape and Find Language ####
##################################
def check_language(url, t):
    headers = {'User-Agent': 'wswp'}
    try:
        source = requests.get(url, headers=headers, timeout=10).text
    except requests.exceptions.ConnectionError:
        return "!!Connection Refused!!"
    except requests.exceptions.ReadTimeout:
        return "!!Read Timed Out!!"
    soup = BeautifulSoup(source, 'lxml')
    content = soup.get_text()
    formatted_content = re.sub(r'^(.{1000}).*$', '\g<1>', " ".join(re.split("\s+", re.sub("\n|\r", " ", content), flags=re.UNICODE)))
    # store the result on redis
    redis.set(url, formatted_content.encode('utf-8'), 3600)
    # Sleep for t seconds, to avoid request rate limit exceed error
    time.sleep(t)
    #### Language Check Code with the help 
    #### of https://www.meaningcloud.com/
    params = (
        ('key', config.license_key),
        ('txt', redis.get(url).decode('utf-8')),
    )
    response = requests.post('http://api.meaningcloud.com/lang-2.0', params=params)
    response_load = json.loads(response.text)

    #Formatting the output from meaningcloud
    newDict = {}
    for item in response_load['language_list']:
        newDict.update(item)
    response_load['language_list']=newDict
    article_language = response_load['language_list']['name']

    return article_language

###############################
####     Scrape by File    ####
###############################
@app.route("/", methods = ["GET", "POST"])
def welcome():
    if request.method == "POST":
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
            flash('No file part')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        urls = [line.rstrip('\n') for line in open(os.path.join(app.config['UPLOAD_FOLDER'], filename))]
        # Removing first line of csv as it is having `url`
        if urls[0] == 'url':
            urls.pop(0)
        # An empty dictionary to store the final result
        resultDict = {}
        for url in urls:
            #remove double quotes in a URL
            url = re.sub('["]+', '', url)
            resultDict[url] = check_language(url,2)
        return render_template("welcome.html", result=resultDict)
    else:
        return render_template("welcome.html")

###############################
####     Scrape by URL     ####
###############################
@app.route("/url-based", methods=["GET", "POST"])
def scrape_by_url():
    if request.method == "POST":
        url = request.form['text']
        # An empty dictionary to store the final result
        urlResultDict = {}
        urlResultDict[url] = check_language(url, 0)
        return render_template("scrape_by_url.html", result=urlResultDict)
    else:
        return render_template("scrape_by_url.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
