###############################
####        Imports        ####
###############################

from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)
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

app = Flask(__name__)

#initialize redis in-memory connection & installing cache for requests
redis = StrictRedis(host='redis', port=6379, db=0)
requests_cache.install_cache(backend='redis', connection=StrictRedis(host='redis', port=6379, db=0), expire_after=600)

# Folder to save the uploaded txt/csv file
UPLOAD_FOLDER = 'Illuma Offline Interview - DevOps/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###############################
####     Scrape by File    ####
###############################
@app.route("/", methods=["GET", "POST"])
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
        print(urls)
        # An empty dictionary to store the final result
        resultDict={}
        for url in urls:
            #Start webscrapping using requests & bs4
            headers = {'User-Agent': 'wswp'}
            source = requests.get(url, headers=headers).text
            soup = BeautifulSoup(source, 'lxml')
            content = soup.get_text()
            formatted_content = re.sub(r'^(.{1000}).*$', '\g<1>', " ".join(re.split("\s+", re.sub("\n|\r", " ", content), flags=re.UNICODE)))
            #store the result on redis
            redis.set(url, formatted_content.encode('utf-8'), 3600)
            time.sleep(3)

            #### Language Check Code with the help 
            #### of https://www.meaningcloud.com/

            params = (
                ('key', '7a7a2a123dd63a2c4449ad65e56d16a9'),
                ('txt', redis.get(url).decode('utf-8')),
            )
            response = requests.post('http://api.meaningcloud.com/lang-2.0', params=params)
            response_load = json.loads(response.text)

            #Formatting the output from meaningcloud
            newDict={}
            for item in response_load['language_list']:
                newDict.update(item)
            response_load['language_list']=newDict
            article_language = response_load['language_list']['name']
            resultDict[url]=article_language
            print(resultDict)
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
        #Start webscrapping using requests & bs4
        headers = {'User-Agent': 'wswp'}
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, 'lxml')
        content = soup.get_text()
        formatted_content = re.sub(r'^(.{1000}).*$', '\g<1>', " ".join(re.split("\s+", re.sub("\n|\r", " ", content), flags=re.UNICODE)))
        #store the result on redis
        redis.set(url, formatted_content.encode('utf-8'), 3600)
        # An empty dictionary to store the final result
        urlResultDict={}

        #### Language Check Code with the help 
        #### of https://www.meaningcloud.com/

        params = (
            ('key', '7a7a2a123dd63a2c4449ad65e56d16a9'),
            ('txt', redis.get(url).decode('utf-8')),
        )
        response = requests.post('http://api.meaningcloud.com/lang-2.0', params=params)
        response_load = json.loads(response.text)

        #Formatting the output from meaningcloud
        newDict={}
        for item in response_load['language_list']:
            newDict.update(item)
        response_load['language_list']=newDict
        article_language = response_load['language_list']['name']
        urlResultDict[url]=article_language
        return render_template("scrape_by_url.html", result=urlResultDict)
    else:
        return render_template("scrape_by_url.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
