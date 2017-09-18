
---------------
 UPGRADE GUIDE
---------------

This file documents changes in behaviour to provide guidance to those upgrading from a previous version.
While configuration language stability is an important goal, on occasion changes cannot be avoided.  
This file does not document new features, but only changes that cause concern during upgrades.
The notices take the form:

**CHANGE**
   indicates where configurations files must be changed to get the same behviour as prior to release.

**ACTION** 
   Indicates a maintenance activity required as part of an upgrade process.

**BUG**
  indicates a bug serious to indicate that deployment of this version is not recommended.

*NOTICE*
  a behaviour change that will be noticeable during upgrade, but is no cause for concern.

*SHOULD*
  indicate recommended interventions that are recommended, but not mandatory. If prescribed activity is not done,
  the consequence is either a configuration line that has no effect (wasteful) or the application
  may generate messages.  
   


git origin/master branch
------------------------

**CHANGE**:  default *expire* setting was 0 (infinite) which means never expire.  Now it is 5 minutes.
**It will also result data loss**, by dropping messages should the default be used in cases where the old value
was expected.  A disconnection of more than 5 minutes will cause the queue to be erased.  To configure what was previously 
the default behaviour, use setting::

       *expire 0*

failure to do so, when connecting to configurations with older pumps versions  may result in warning messages about 
mismatched properties when starting up an existing client. 
FIXME: more specific?

**NOTICE**: cache state file format changed and are mutually unintelligible between versions.  
During upgrade, old cache file will be ignored.  This may cause some files to be accepted a second time.
*FIXME*  work-arounds? 

**ACTION**: must run sr_audit --users foreground to correct permissions, since it was broken in previous release.   



2.17.08
-------

**BUG**: avoid this version to administer pumps because of bug 88: sr_audit creates report routing queues 
even when report_daemons is off, they fill up with messages (since they are never emptied.) This can cause havoc.
If report_daemons is true, then there is no issue.  Also no problem for clients. 

**ACTION**: (must run sr_audit --users foreground to correct permissions.)
users now have permission to create exchanges.  
if corrections not updated on broker, warning messages about exchange declaration failures will occur.

*SHOULD*: remove all *declare exchange* statements in configuration files, though they are harmless.
configurations declare broker side resources (exchanges and queues) by *setup* action.  The resources can be freed 
with the *cleanup* action.  Formerly creation and deletion of exchanges was an administrator activity.

*SHOULD*: cluster routing logic removed ( *cluster*, *gateway_for*, and *cluster_aliases* ) these options are now ignored.
If relying on these options to restrict distribution (no known cases), that will stop working.
cluster propagation restriction to be implemented by plugins at a future release.
should remove all these options from configuration files.

*SHOULD*: should remove all *sftp://*  url lines from credentials.conf files. Configuration of sftp should be done
via openssh configuration, and credential file only used as a last resort.  Harmless if they remain, however.



2.17.07
-------


**CHANGE**: sr_sender *mirror* has been repaired.  if no setting present, then it will now mirror.
to preserve previous behavior, add to configuration::

       mirror off

*NOTICE*: switch from traditional init-style ordering to systemd style -->  action comes before configuration.
was::

      sr_subscriber myconfig start --> sr_subscriber start myconfig 

software issues warning message about the change, but old callup still supported.


*NOTICE*: heartbeat log messages will appear every five minutes in logs, by default, to differentiate no activity
from a hung process.

 
2.17.06
-------

**CHANGE**: Review/Modify all plugins, as file variables of sender and subscriber converged.
   on_msg plugin variable for file naming for subscribers (sr_subscribe,sarra,shovel,winnow) changed.  Replace::

      self.msg.local_file --> self.msg.new_dir and self.msg.new_file

   on_msg plugin variable for file naming for senders now same as for subscribers.  Replace::

      self.remote_file --> self.msg.new_dir and self.msg.new_file

**CHANGE**: by default, the modification time of files is now restored on delivery.  To restore previous behaviour::

      preserve_time off

If preserve_time is on (now default) and a message is received, then it will be rejected if the mtime of
the new file is not newer than the one of the existing file.

**CHANGE**: by default, the permission bits of files is now restored on delivery.  To restore previous behaviour::

      preserve_mode off



2.17.02
-------

*NOTICE*: sr_watch re-implementation. now supports symlinks, multiple traversal methods, etc...
many behaviour improvements. FIXME: ?

**CHANGE**: plugins are now stackable. formerly, when two plugin specifications were given, the newer one
would replace the previous one.  Now both plugins will be executed in the order encountered.
 

