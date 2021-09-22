## ns1-ftp ##
This script performs a check on an FTP server to determine if a file exists on that server.
If it does, it will set a datafeed on NS1 to up. 
If it does not, it will set that datafeed to down. 

### requirements ###
python3
requests

### usage ###
There are a minimum of two files required to run:

`ns1-ftp-check.py` is the main python script

`ftpcheck.ini` is a check configuration

**for every check you need, you will need a filename which matches ftpcheck\*.ini**

e.g. `ftpcheck1.ini ftpcheck-server2.ini ftpcheck_us_east.ini`

The script will read each matching check file from the directory it lives in, and perform the checks for each one in turn.

This script needs to be added to a crontab for a user or root. 

**note: the requests library needs to be present in the cron environment**
