 <?php

/*
 * NSONE Dynamic DNS update helper
 * Dan Cech <dan@aussiedan.com>
 */

// check a password was provided
if (empty($_SERVER['PHP_AUTH_PW'])) {
    header('WWW-Authenticate: Basic realm="DDNS"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Unauthorized';
    exit;
}

// password is nsone API key, username is ignored
$apikey = $_SERVER['PHP_AUTH_PW'];

// check a valid hostname was provided
if (empty($_REQUEST['hostname']) || !preg_match('/^[a-z0-9-]+\.([.a-z0-9-]+)$/i',$_REQUEST['hostname'],$m)) {
    echo 'A valid hostname is required';
    exit;
}

// record is complete hostname
$record = $m[0];

// zone is everything after the first period
$zone = $m[1];

// if IP was provided, use that
if (!empty($_REQUEST['myip'])) {
    $addr = $_REQUEST['myip'];
// otherwise use caller's IP
} else {
    $addr = $_SERVER['REMOTE_ADDR'];
}

// assemble NSONE API url
$url = 'https://api.nsone.net/v1/zones/'. $zone .'/'. $record .'/A';

// JSON request to set IP as static answer
$params = '{"answers": [{"answer": ["'. $addr .'"]}]}';

// initialize curl
$curl = curl_init($url);
curl_setopt($curl,CURLOPT_POST,1);
curl_setopt($curl,CURLOPT_POSTFIELDS,$params);
curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
curl_setopt($curl,CURLOPT_FAILONERROR,1);

// user-agent & request headers
curl_setopt($curl,CURLOPT_USERAGENT,'aussiedan ddns 0.1');
curl_setopt($curl,CURLOPT_HTTPHEADER,array(
    'Content-type: application/json',
    'X-NSONE-Key: '. $apikey,
));

// make request to NSONE
$response = curl_exec($curl);
$errstr = curl_error($curl);
curl_close($curl);

// request failed
if ($response === false) {
    echo 'cURL Error: '. $errstr;
    exit;
}

echo 'OK';

// end of script
