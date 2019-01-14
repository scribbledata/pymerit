import hashlib 
import tempfile 
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

def test_default_resources_invalid_1(default_merit): 
    """
    Check None resource
    """
    with pytest.raises(pymerit.MeritInvalidResource) as exc: 
        default_merit.add_resource(None) 
    
def test_default_resources_invalid_2(default_merit): 
    """
    Check dict resource 
    """
    with pytest.raises(pymerit.MeritInvalidResource) as exc: 
        default_merit.add_resource({})

def test_default_resources_invalid_3(default_merit):
    """
    Check context resource 
    """

    class Resource(pymerit.MeritContextBase):
        schema = "Hello"
            
    with pytest.raises(pymerit.MeritInvalidResource) as exc: 
        default_merit.add_resource(Resource())
        
def test_default_resources_invalid_4(default_merit):
    """
    Check resource without name
    """

    class Resource(pymerit.MeritResourceBase):
        schema = "Hello"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_resource(Resource())
        
    assert "Missing: name" in str(exc) 

def test_default_resources_invalid_5(default_merit):
    """
    Check resource without description
    """

    class Resource(pymerit.MeritResourceBase):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_resource(r)
        
    assert "Missing: description" in str(exc) 

def test_default_resources_invalid_6(default_merit):
    """
    Check resource with description
    """

    class Resource(pymerit.MeritResourceBase):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    r.description = "Long description"
    
    default_merit.add_resource(r)
    
        

def test_file_resources_invalid_1(default_merit):
    """
    Check resource without description
    """

    class Resource(pymerit.MeritResourceFile):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    r.description = "Long string"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_resource(r)
        
    assert "Missing: path" in str(exc) 
                   
def test_file_resources_invalid_1(default_merit):
    """
    Check resource without description
    """

    class Resource(pymerit.MeritResourceFile):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    r.description = "Long string"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_resource(r)
        
    assert "Missing: path" in str(exc) 
        
        
def test_file_resources_invalid_1(default_merit):
    """
    Check resource with invalid path
    """

    class Resource(pymerit.MeritResourceFile):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    r.description = "Long string"
    r.path = "hello"
    
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        default_merit.add_resource(r)

    assert "Missing file" in str(exc) 
        
def test_file_resources_valid_1(default_merit):
    """
    Check resource with valid path
    """

    class Resource(pymerit.MeritResourceFile):
        schema = "Hello"

    r = Resource()
    r.name = "helloattr"
    r.description = "Long string"

    # Create a temporary file 
    tf = tempfile.NamedTemporaryFile()
    r.path = tf.name 
    
    default_merit.add_resource(r)

    # Cleanup
    tf.close()

def test_file_resources_valid_2(default_merit):
    """
    Check resource with valid path
    """

    class Resource(pymerit.MeritResourceFile):
        schema = "resource:acmefile:v1"

    r = Resource()
    r.name = "runlog"
    r.description = "Run log from execution"

    # Create a temporary file 
    tf = tempfile.NamedTemporaryFile()
    tf.write(b"Hello") 
    r.path = tf.name 
    tf.seek(0)
    
    # Add attributes
    attributes = { 
        'sha256sum': hashlib.sha256(tf.read()).hexdigest()    
    }
    r.attributes = attributes
    
    default_merit.add_resource(r)

    # Cleanup
    tf.close()    

        
    
    
        
    
    
