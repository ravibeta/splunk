# splunk
Introduction
------------
This is an application that lets you provision the Splunk artifacts - index, roles etc and AD security group to provision a private index for your logs. With a private index, you can add users to a security group that can search only this index.


Installation
------------
The application can be deployed with the following steps:
1) tar ball this directory and copy it to the destination Splunk instance under $SPLUNK_HOME/etc/apps
2) use the splunkdj as mentioned in the splunk documentation to create a Splunk Django app by the same name as this application
3) replace the application with the files from this tar ball
4) provision a Splunk index by name 'logstore_metadata'
5) provision a Splunk user by name 'uidev' and password 'uidev'
6) provision a TCP port 8555 to receive data to index logstore_metadata

Usage
-----
The landing page describes the workflow to create a private index.
There is a link on that page that automates it for you by taking a name for the following:
- a Splunk index
- a Splunk role to use with the index
- an AD security group that manages the index
