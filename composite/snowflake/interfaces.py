from zope.interface import Interface, Attribute, classImplements

class ISnowflake(Interface):
    """Interface declaration and utility marker for Pyramid, and possible 
       for both Zope 2 and 3
    """
    datacenter_id = Attribute("Datacenter ID")
    worker_id = Attribute("Worker ID")

    def get_id():
        """Get new 64-bit unique ID
        """

    def get_timestamp():
        """Get timestamp from snowflake generation algorithm
        """

# Declare implementations here, avoiding direct dependencies on z.interface
# in snowflake.py
from .snowflake import ThreadSafeSnowflake, Snowflake
classImplements(Snowflake, ISnowflake)
classImplements(ThreadSafeSnowflake, ISnowflake)
