-- Name: NSOne Dynamic DNS AppleScript Updater
-- Description: Finds address for given 'interface_name' and updates dns_record via NSOne API to match.   Relies on calling the command line 'curl' client to make HTTPS requests
-- Creator: J. W. Brinkerhoff <jwb@paravolve.net>

-- START CONFIG
set the interface_name to "tun0" -- Generally OpenVPN will use tun0
set the nsone_api_key to "YOUR_API_SECRET_HERE" -- Get your NSOne API secret from the account settings page of the NSOne portal
set the dns_zone to "example.com"
set the dns_record to "dynamicdns." & dns_zone

set the nsone_api_endpoint to "https://api.nsone.net/v1" -- This shouldn't need to be changed.
-- END CONFIG

-- Build record URL based upon nsone_api_endpoint, dns_zone, dns_record and dns_record_type
set the dns_record_type to "A"
set the record_url to nsone_api_endpoint & "/zones/" & dns_zone & "/" & dns_record & "/" & dns_record_type

-- Call ifconfig for interface_name and parse output for inet address (tested on enX as well as tun0.  ignores inet6 addresses)
-- If calling ifconfig on interface_name fails for some reason, it falls back to en0
-- The funky parsing is necessary for non-enX interfaces (tun0, for example) - Is there a better way?
try
	set the ifconfig_output to do shell script "ifconfig " & interface_name & " inet"
	set parsed_ifconfig to my split(ifconfig_output, "\r\t")
	set ip_address to item 2 of my split(item 2 of parsed_ifconfig, " ")
on error
	set the ip_address to do shell script "ipconfig getifaddr en0"
end try

-- Setup JSON payload and send to REST record_url, authenticating using X-NSONE-Key nsone_api_key
set post_data to "{\"answers\": [{\"answer\": [\"" & ip_address & "\"]}]}"
set curl_command to "curl -X POST -H 'X-NSONE-Key: " & nsone_api_key & "' -d '" & post_data & "' " & record_url

-- Run curl as defined above
do shell script curl_command

-- Function takes a string and a delimiter, returns array containing split string
on split(theString, theDelimiter)
	set oldDelimiters to AppleScript's text item delimiters
	set AppleScript's text item delimiters to theDelimiter
	set theArray to every text item of theString
	set AppleScript's text item delimiters to oldDelimiters
	return theArray
end split
