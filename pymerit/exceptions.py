"""
Exceptions 
----------

"""
class MeritNoHandler(Exception):
    """
    Not class to handle metadata with a given schema
    """
    pass

class MeritNoAttribute(Exception):
    """
    Internal metadata does not have the required attribute
    """
    pass

class MeritInvalidAttribute(Exception):
    """
    Invalid name specified to generate the class attribute 
    """
    pass

class MeritInvalidSchema(Exception):
    """
    Invalid schema definition 
    """
    pass

class MeritMissingSchema(Exception):
    """
    Schema not defined in the given merit subclass 
    """
    pass

class MeritDuplicateSchema(Exception):
    """
    Another handler exists for the given schema 
    """
    pass

class MeritInvalidMetadata(Exception):
    """
    Metadata cannot be loaded due to missing fields 
    """
    pass

class MeritInvalidContext(Exception):
    """
    Invalid class specified while adding context
    """
    pass

class MeritInvalidResource(Exception):
    """
    Invalid class specified while adding resource 
    """    
    pass

class MeritNotRegistered(Exception):
    """
    Class not a registered handler for any schema 
    """
    pass
