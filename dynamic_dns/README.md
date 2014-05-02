Dynamic DNS
===========

All of these scripts provide methods of updating "Dynamic DNS" records via
the NSONE REST API. You will have to modify each to provide your NSONE API Key 
and other details.

See also https://nsone.net/api/

* ddns.sh (bash)
 
   Update based on local ethernet interface address (linux/unix).
   Uses curl. 

* NSOne_Dynamic_DNS_AppleScript_Updater.scpt (applescript)

   Update based on local ethernet interface address (OSX).
   Uses curl.

* ddns.php (PHP)

   A PHP script meant to run on a webserver where it can forward standard DDNS 
   updates to NSONE REST API. You can, for example, configure most routers supporting DDNS to contact
   this script (after you've configured it).

   Example screenshot:

   ![DDNS](https://raw.githubusercontent.com/nsone/contrib/master/dynamic_dns/ddns-with-dd-wrt-and-ddns-php.png "DDNS")

