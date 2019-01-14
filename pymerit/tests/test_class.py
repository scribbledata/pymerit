import gc 
import sys 
import inspect 
import pytest
import pymerit

def test_noschema():
    """
    Test without schema 
    """

    with pytest.raises(pymerit.MeritInvalidSchema) as exc:
        class HelloMerit(pymerit.MeritBase):
            pass        
        h = HelloMerit()

def test_invalid_schema():
    """
    Test without schema 
    """
    with pytest.raises(pymerit.MeritInvalidSchema) as exc:
        class HelloMerit(pymerit.MeritBase):
            schema = {}
            def initialize(self):
                pass
        h = HelloMerit()

def test_no_initialize():
    """
    Test without initialize
    """
    with pytest.raises(TypeError) as exc:
        class HelloMerit(pymerit.MeritBase):
            schema = 'hello' 
        h = HelloMerit()
    
def test_duplicate():
    """
    Test duplicate class
    """

    class HelloMerit1(pymerit.MeritBase):
        schema = 'hello'
        def initialize(self):
            pass

    pymerit.schema_register(HelloMerit1)
    
    with pytest.raises(pymerit.MeritDuplicateSchema) as exc:    
        class HelloMerit2(pymerit.MeritBase):
            schema = 'hello'
            def initialize(self):
                pass
        pymerit.schema_register(HelloMerit2)
        
    pymerit.schema_unregister(HelloMerit1) 
