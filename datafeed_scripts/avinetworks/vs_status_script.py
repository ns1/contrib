#!/usr/bin/env python
"""
AVI ControlScript that updates the `UP` meta of an NS1 Datafeed.

Invoked by the AVI Controller when a "VS_UP" or "VS_DOWN" alert is raised
(alert action configured as ControlScript) and updates `UP` meta accordingly.

`datasource_id` and `ns1_apikey` global vars must be configured in order to
update the datafeed.  `ns1_endpoint` can optionally be configured to the FQDN
of a custom API endpoint if using Private DNS or DDI.
"""
import argparse
import json
import sys

from ns1 import Config, NS1

# ID of the datasource in NS1 to publish updates to
datasource_id = "a53252f9e583c6708331a1daeb172e12"
# NS1 apikey to use when publishing updates
ns1_apikey = "qACMD09OJXBxT7XOuRs8"
# FQDN of NS1 API endpoint.  Leave as is if using Managed DNS.
ns1_endpoint = "api.nsone.net"


def init_api():
    """
    Inititialize NS1 SDK

    :return: Configured NS1 API object
    """
    config = Config()
    config.createFromAPIKey(ns1_apikey)
    config["endpoint"] = ns1_endpoint
    return NS1(config=config)


def update_datafeed(api, alert_info):
    """
    Update `UP` metadata via datafeed

    :param ns1.NS1 api: NS1 API object
    :param dict alert_info: alert information passed by Avi Vantage alert
    """
    up_status = None
    event = alert_info["events"][0]
    label = event["event_details"]["se_hm_vs_details"]["virtual_service"]

    if event["event_id"] == "VS_UP":
        up_status = True
    elif event["event_id"] == "VS_DOWN":
        up_status = False

    if up_status is not None:
        data = {label: {"up": up_status}}
        source_api = api.datasource()
        source_api.publish(datasource_id, data)


def main():
    if not datasource_id:
        raise Exception("datasource_id is undefined")
    if not ns1_apikey:
        raise Exception("ns1_apikey is undefined")
    if not ns1_endpoint:
        raise Exception("ns1_endpoint is undefined")

    parser = argparse.ArgumentParser(
        description="Controlscript to update NS1 datafeed on vs_down or vs_up"
    )
    parser.add_argument(
        "alert_info", help="Dict containing information about the alert"
    )
    parsed = parser.parse_args()

    api = init_api()
    update_datafeed(api, json.loads(parsed.alert_info))


if __name__ == "__main__":
    main()
