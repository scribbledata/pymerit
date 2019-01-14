import pytest
import pymerit

def test_default_create():
    """
    Test create default  
    """
    assert pymerit.MeritDefault() 
        

def test_default_serialize_no_namespace():
    """
    Serialization with invalid data
    """
    h = pymerit.MeritDefault()
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        h.dumps()

    assert "Missing: namespace" in str(exc) 

def test_default_serialize_with_no_path():
    """
    Serialization with valid data 
    """
    h = pymerit.MeritDefault()
    h.namespace = "test"
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        h.dumps()    
        
    assert "Missing: path" in str(exc) 

def test_default_serialize_with_no_name():
    """
    Serialization with valid data 
    """
    h = pymerit.MeritDefault()
    h.namespace = "test"
    h.path = "project=alpha/run=20134" 
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        h.dumps()    
        
    assert "Missing: name" in str(exc) 
    

def test_default_serialize_with_no_description():
    """
    Serialization with valid data 
    """
    h = pymerit.MeritDefault()
    h.namespace = "test"
    h.path = "project=alpha/run=20134"
    h.name = "Run output" 
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        h.dumps()    
        
    assert "Missing: description" in str(exc) 
    
def test_default_serialize_with_no_description():
    """
    Serialization with valid data 
    """
    h = pymerit.MeritDefault()
    h.namespace = "test"
    h.path = "project=alpha/run=20134"
    h.name = "Run output" 
    with pytest.raises(pymerit.MeritInvalidMetadata) as exc: 
        h.dumps()    
        
    assert "Missing: description" in str(exc) 
    
    
    
def test_default_serialize_with_no_contexts():
    """
    Serialization with valid data 
    """
    h = pymerit.MeritDefault()
    h.namespace = "test"
    h.path = "project=alpha/run=20134"
    h.name = "Run output"
    h.description = "Run output" 
    assert h.dumps() is not None
    assert isinstance(h.dump(), dict)

    
def test_valid_serialized():
    """
    Check loading of serialized object
    """
    metadata = {
        "schema": "global:default:v1",
        "namespace": "test",
        "path": "project=alpha/run=20134",
        "name": "Run output",
        "description": "Run output",
        "contexts": [
            {
                "schema": "context:platform:v1",
                "name": "PlatformContext",
                "description": "Host on which the execution took place",
                "python": "3.5.2",
                "platform": "Linux-4.15.0-42-generic-x86_64-with-Ubuntu-16.04-xenial",
                "node": "whale"
            },
            {
                "schema": "context:process:v1",
                "name": "ProcessContext",
                "description": "Process generating this metadata",
                "ppid": 14929,
                "pid": 4557,
                "cmdline": [
                    "/home/pingali/.virtualenvs/dev/bin/pytest",
                    "-s",
                    "-vv"
                ]
            }
        ],
        "resources": []
    }

    obj = pymerit.new(metadata)
