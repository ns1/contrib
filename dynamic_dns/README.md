Dynamic DNS
===========

All of these scripts provide methods of updating "Dynamic DNS" records via
the NSONE REST API. You will have to modify each to provide your NSONE API Key 
and other details.

See also https://nsone.net/api/

* ddns.sh (bash)
 
   Update based on local ethernet interface address (linux/unix).
   Uses curl. 

* ubntDynDns.py

   Created for Ubiquiti EdgeRouter devices, but it should run on most Linux based platforms.
   Intentionally lightweight with minimal dependencies for embedded / IoT applications.
   To use, schedule execution of the script periodically via cron (or your scheduler of choice).

   For example:

   `*/5 * * * * ns1apikey mydomain.net myhost.mydomain.net`

* ipupdater (Python3)

   Update based on your public ip fetched via https://www.ipify.org/.
   Systemd is used to daemonize the script: https://github.com/josvo/ipupdater