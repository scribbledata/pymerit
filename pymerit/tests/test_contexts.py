import pytest
import pymerit

@pytest.fixture
def default_merit():
    h = pymerit.MeritDefault()
    h.namespace = "test"
    h.path = "project=alpha/run=20134"
    h.name = "Run output"
    h.description = "Run output" 
    return h

def test_default_contexts_invalid_1(default_merit): 
    """
    Check None context 
    """
    with pytest.raises(pymerit.MeritInvalidContext) as exc: 
        default_merit.add_context(None) 
    
def test_default_contexts_invalid_2(default_merit): 
    """
    Check dict context 
    """
    with pytest.raises(pymerit.MeritInvalidContext) as exc: 
        default_merit.add_context({})

def test_default_contexts_invalid_3(default_merit):
    """
    check resource context 
    """

    class Context(pymerit.MeritResourceBase):
        schema = "Hello"
            
    with pytest.raises(pymerit.MeritInvalidContext) as exc: 
        default_merit.add_context(Context())
        
def test_default_contexts_invalid_4(default_merit):
    """
    Check context without name 
    """

    class Context(pymerit.MeritContextBase):
        schema = "Hello"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_context(Context())
        
    assert "Missing: name" in str(exc) 

def test_default_contexts_invalid_5(default_merit):
    """
    Check context without description
    """

    class Context(pymerit.MeritContextBase):
        schema = "Hello"

    c = Context()
    c.name = "helloattr"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_context(c)
        
    assert "Missing: description" in str(exc) 

