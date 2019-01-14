"""
Extensible pymerit libraries 
"""
import os
import sys
import platform

from .base import *

class MeritContextPlatform(MeritContextBase):
    schema = 'context:platform:v1'
    
    def initialize(self, *args, **kwargs):
        self.metadata = {
            "name": "PlatformContext",
            "description": "Host on which the execution took place",
            "node":  platform.node(),
            'platform': platform.platform(),
            "python": platform.python_version(),
        }

class MeritContextProcess(MeritContextBase):
    schema = 'context:process:v1'
    
    def initialize(self, *args, **kwargs):
        self.metadata = {
            "name": "ProcessContext",
            "description": "Process generating this metadata",
            "pid":  os.getpid(),
            "ppid":  os.getppid(),
            "cmdline": list(sys.argv)
        }

class MeritResourceFile(MeritResourceBase):
    schema = 'resource:filebase:v1'
    
    def initialize(self, *args, **kwargs):
        
        super().initialize(*args, **kwargs)
        
        self.metadata = {
            "name": "File",
            "description": "File saved on disk",
            "attributes": {}, 
        }        
        self.required.extend([
            "path",
            "attributes" 
        ])


    path = get_metadata_attribute('path')
    attributes = get_metadata_attribute('attributes')    
    
    def validate_path(self, path):
        """
        Check if the path exists 
        """

        if not isinstance(path, str): 
            raise MeritInvalidMetadata("Invalid path for file resource specified. Not a string")
        
        if not os.path.exists(path):
            raise MeritInvalidMetadata("Invalid path for file resource specified. Missing file") 
        
class MeritResourceS3File(MeritResourceBase):
    schema = 'resource:s3filebase:v1'
    
    def initialize(self, *args, **kwargs):
        self.metadata = {
            "name": "File",
            "description": "S3 file"
        }        
        self.required.extend([
            "s3path",
            "attributes",
        ])        


class MeritDefault(MeritGlobalBase):
    schema = 'global:default:v1'
    
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

        # Add contexts 
        self.add_context(MeritContextPlatform())
        self.add_context(MeritContextProcess())        
