# Avi ControlScripts

From [https://avinetworks.com/docs/17.2/configuration-guide/templates/scripts/](https://avinetworks.com/docs/17.2/configuration-guide/templates/scripts/):
> ControlScripts are Python-based scripts which execute on the Avi Vantage Controllers. They are initiated by Alert Actions, which themselves are triggered by events within the system.

The ControlScripts in this directory allow for Alerts triggered within Avi Vantage to update a NS1 Data Source.

# Installation

1. Install the [ns1-python](https://github.com/ns1/ns1-python) SDK on all Avi Vantage Controllers.  This can be installed via pip:
```
pip install ns1-python
```

1. In Avi Vantage, create a new **Alert Action** in **Operations > Alert > Alert Action**

1. In the **ControlScript** drop down, select **Create ControlScript Profile** and upload or paste the ControlScript

1. Configure the necessary global variables in the script (i.e. `ns1_apikey`).

1. Once a ControlScript profile has been applied to an Alert Action, it can be assigned to a new Alert Configuration via  **Operations > Alert > Alert Config**

# Usage

## vs_status_script.py
Updates the `UP` meta key of an NS1 Data Feed.  Intended to be configured as the Alert Action for an alert that it triggered when either the **VS Down** or **VS Up** events occur.

The `datasource_id` and `ns1_apikey` global vars must be configured in order to
update the datafeed.  `ns1_endpoint` can optionally be configured to the FQDN
of a custom API endpoint if using Private DNS or DDI.
