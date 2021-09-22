import os
import glob
import requests
import configparser
import sys
from ftplib import FTP
import datetime
import json

def _is_down(check, note):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    note = note.rstrip() + ' since ' +  str(now)
    url = 'https://api.nsone.net/v1/feed/' + check['datasource'].rstrip()
    feed_data = json.dumps({check['feed_label'].rstrip():{'up':False, 'note':note}})
    headers = {'x-nsone-key': check['apikey'].rstrip()}
    try:
        r = requests.post(url=url, data=feed_data, headers=headers)
        if r.status_code != 200:
            print(f"{str(now)} ERROR: feed update failure {feed_label} to DOWN status: {r.status_code}")
    except Exception as e:
        print(f"{str(now)} ERROR: feed update failure {feed_label} to DOWN status: {str(e)}")

def _is_up(check, note):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    note = note.rstrip() + ' since ' +  str(now)
    url = 'https://api.nsone.net/v1/feed/' + check['datasource'].rstrip()
    feed_data = json.dumps({check['feed_label'].rstrip():{'up':True, 'note':note}})
    headers = {'x-nsone-key': check['apikey'].rstrip()}
    try:
        r = requests.post(url=url, data=feed_data,headers=headers)
        if r.status_code != 200:
            print(f"{str(now)} ERROR: feed update failure {feed_label} to UP status: {r.status_code}")
    except Exception as e:
        print(f"{str(now)} ERROR: feed update failure {feed_label} to UP status: {str(e)} ")







# find all the configs
checklist = glob.glob('ftpcheck*.ini')
if checklist == []:
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    print(f"{now} ERROR: no ftpcheck*.ini found. unable to continue.")
    sys.exit(1)


# load the configs first
checks = []
for check in checklist:
    try:
        config = configparser.ConfigParser()
        config.read(check)
        hostname = config['ftp']['hostname']
        username = config['ftp']['username'] if config['ftp']['username'] != '' else None
        password = config['ftp']['password'] if config['ftp']['password'] != '' else None
        filename = config['ftp']['filename']
        apikey = config['ns1']['apikey']
        datasource = config['ns1']['datasource']
        feed_label = config['ns1']['feed_label']
        check_dict = {'hostname':hostname, 'username':username, 'password':password, 'filename':filename,
                      'apikey':apikey, 'datasource':datasource, 'feed_label':feed_label}
        checks.append(check_dict)
    except:
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
        print(f"{now} ERROR: {check} is invalid. unable to continue.")
        sys.exit(1)

# run the checks and update the data feeds        
for check in checks:
    try:
        ftp = FTP(check['hostname'])
        if check['username'] is not None and check['password'] is not None:
            ftp.login(user=check['username'],passwd=check['password'])
        else:
            ftp.login()
        ftp.set_pasv(False)
        flist = ftp.nlst()
    except Exception as e:
        flist = []
        _is_down(check, 'exception '+str(e) )
    if check['filename'] not in flist:
        _is_down(check, 'file not found')
    else:
        _is_up(check, 'ok')
