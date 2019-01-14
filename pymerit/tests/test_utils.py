import gc 
import pytest
import pymerit

from pymerit.utils import * 

@pytest.fixture(autouse=True)
def cleanup():
    """
    Cleanup classes 
    """
    gc.collect()
    
def test_get_metadata_valid():
    """
    Check whether get_metadata is working 
    """
    
    class X(object):

        def __init__(self):
            self.metadata = {
                'alpha': None 
            } 

        alpha = get_metadata_attribute('alpha') 

    assert hasattr(X, 'alpha')

def test_get_metadata_valid():
    """
    Check whether get_metadata is working 
    """

    with pytest.raises(pymerit.MeritInvalidAttribute) as exc: 
        class X(object):
            def __init__(self):
                self.metadata = {}
            alpha = get_metadata_attribute(None) 

def test_all_classes():
    """
    Test Subclasses of MeritBase
    """

    subclasses = pymerit.all_subclasses(pymerit.MeritBase)
    assert len(subclasses) > 0
    assert pymerit.MeritGlobalBase in subclasses 

def test_no_schema():
    """
    Test instantiation of new object 
    """

    metadata = {}
    with pytest.raises(pymerit.MeritMissingSchema) as exc: 
        pymerit.new(metadata) 

def test_new_no_handler():
    """
    Test instantiation of new object 
    """

    metadata = {
        'schema': "hello"
    }
    with pytest.raises(pymerit.MeritNoHandler) as exc: 
        pymerit.new(metadata) 
        

def test_not_handler():
    """
    Test with unregistered class
    """

    class HelloMerit(pymerit.MeritBase):
        schema = "hello"
        def initialize(self):
            pass

    with pytest.raises(pymerit.MeritNotRegistered) as exc: 
        pymerit.schema_unregister(HelloMerit) 
