SAM Nagios BDII service updater
===============================

The aim of the application is to provide a means to dinamically add hosts to a SAM
Nagios box relying `Nagios configuration generator (NCG) 
<https://github.com/ARGOeu/ncg>`_ functionality. Since NCG
can add to Nagios the list of hosts being published in a site-BDII, this app allows
to add BDII endpoints to a given site-BDII site-urls file and subsequently run NCG
to re-create the Nagios configuration.

The ultimate use case is for `UMD <http://repository.egi.eu>`_ software verfication: 
once a given UMD product is deployed, it needs to be monitored by Nagios in order to
successfully fulfill the `quality criteria <http://egi-qc.github.io/>`_ for that 
product. By using the service's API, this product can be monitored by Nagios with no
human intervention.
