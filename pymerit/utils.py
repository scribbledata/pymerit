"""
Utils
-----

Helper functions 
"""
import json
import yaml 
from .exceptions import *

def all_subclasses(cls):
    """
    Find all subclasses of a class 

    :rtype: object
    :return: "Set of subclasses" 

    :param object cls: Baseclass 
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])

def get_metadata_attribute(name):

    if name is None:
        raise MeritInvalidAttribute("Invalid attribute: None")     
    @property
    def prop(self):
        if name not in self.metadata:
            raise MeritNoAttribute("Missing attribute: {}".format(name))
        return self.metadata[name] 
    
    @prop.setter
    def prop(self, value):
        self.metadata[name] = value 

    return prop 

def new(metadata, mode="json"):
    """
    Create Merit object from dictionary
    
    :param dict metadata: Metadata to be loaded 
    """

    from pymerit import MeritBase

    # => If it is a file descriptor, then load it as a json
    if hasattr(metadata, 'read'):
        if mode == "json": 
            metadata = json.load(metadata)
        elif mode == "yaml":
            metadata = yaml.load(metadata)            
    
    cls = MeritBase.find_handler_for_dict(metadata)
    obj = cls() 
    obj.load(metadata)
    return obj 
    
def schema_register(cls):
    """
    Register a new handler class

    :param class cls: Handler class 
    """

    from pymerit import MeritBase
    
    return MeritBase.schema_register(cls)

def schema_unregister(cls):
    """
    Unregister a handler class 

    :param class cls: Handler class 
    """
    from pymerit import MeritBase
    
    return MeritBase.schema_unregister(cls)

def find_handler(schema):
    """
    Find handler classes 

    :param str schema: Schema to find handler for 
    """
    from pymerit import MeritBase

    return MeritBase.find_handler(schema) 
