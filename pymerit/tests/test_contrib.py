import pytest
import pymerit

def test_contrib_platform():
    """
    Test whether platform context object can be created
    """

    h = pymerit.MeritContextPlatform()
    h.validate() 

def test_contrib_process():
    """
    Test whether process context object can be created
    """    
    h = pymerit.MeritContextProcess()
    h.validate()     
    
    
