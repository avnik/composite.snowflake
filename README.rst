Standalone Snowflake Generator
==============================

Overview
--------

composite.snowflake is a simplified Python implementation of Twitter's 
snowflake.  It implemented in pure Python, as simple standalone library.

Pyramid integration
-------------------

Also this package contain Zope interface declaration for ISnowflake, and
optional configuration shim for pyramid. Just include into configuration
``composite.snowflake.pyramid`` and get ISnowflake utility. It automatically
take care on snowflake.datacenter_id and snowflake.worker_id in your paster
.ini file.

But composite.snowflake does not require pyramid or zope.interface unless you
import interface declaration, or activate package from pyramid side.

Installation
------------

Just add composite.snowflake into you buildout.cfg 
