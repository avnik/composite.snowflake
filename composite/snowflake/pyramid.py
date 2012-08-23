from .interfaces import ISnowflake
from .snowflake import ThreadSafeSnowflake

def includeme(config):
    """Initialize and register Snowflake generator
       Just add to you initialization code:
       .. code :: python
          configurator.include("composite.snowflake.pyramid")

       and later 
       .. code :: python

          from composite.snowflake.interfaces import ISnowflake
          snowflake = request.registry.getUtility(ISnowflake)
          id = snowflake.get_id()
        
       for generating fresh snowflakes.

       Snowflake recognize snowflake.worker_id and snowflake.datacenter_id
       in pyramid settings dictionary (.ini settings)
    """
    registry = config.registry
    settings = registry.settings
    worker_id = int(settings.get("snowflake.worker_id", 1))
    datacenter_id = int(settings.get("snowflake.datacenter_id", 1))
    sf = ThreadSafeSnowflake(datacenter_id, worker_id)
    registry.registerUtility(sf, ISnowflake)

