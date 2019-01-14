"""
Base
----

Base classes for metadata including a metaclass to enable tracking of the schema-specific classes.

"""
import os
import sys
import json
import collections
import abc
import texttable
from .exceptions import *
from .utils import *

class MeritBase(object):
    pass

class MeritMeta(abc.ABCMeta):
    """
    Meta class for all elements with schemas. This allows for
    registration, validation, and tracking of the schema implementors.
    """
    def __init__(cls, name, bases, dct):

        if cls.__name__ in ['MeritBase']:
            super().__init__(name, bases, dct)
            return

        MeritBase.validate_cls(cls, dct)

        # Now initialize
        super().__init__(name, bases, dct)


        # Auto register classes
        if cls.__module__ in ['pymerit.base', 'pymerit.contrib']:
            MeritBase.schema_register(cls)


class MeritBase(metaclass=MeritMeta):
    """
    Base abstract class for pymerit schema implementors
    """
    schema = "default:base:v1"
    """
    Every Merit metadata class should specify a schema (a
    string or a list of strings)
    """

    _registry = []
    """
    Registy of schemas and handler classes
    """

    def __init__(self, *args, **kwargs):
        self.metadata = {}
        """
        Internal dict representation of the metadata

        required elements: name, description
        """
        self.required = [
            'name',
            'description',
        ]
        self.order = []

        # Now initialize
        self.initialize()

    name = get_metadata_attribute('name')
    """
    Property-like access to metadata name element
    """

    description = get_metadata_attribute('description')
    """
    Property-like access to metadata description element
    """

    ####################################################
    # Validation of new handler during class instantiation
    ####################################################
    @classmethod
    def validate_schema(cls, targetcls, dct):

        schema = dct.get('schema', None)
        if not (isinstance(schema, str) or isinstance(schema, list)):
            raise MeritInvalidSchema("Invalid schema type")
        elif ((isinstance(schema, str) and len(schema) == 0) or
            (isinstance(schema, list) and len(schema) == 0)):
            raise MeritInvalidSchema("Schema empty")
        elif isinstance(schema, list) and len(schema) > 0:
            for v in schema:
                if not (isinstance(v, str) and len(v) > 0):
                    raise MeritInvalidSchema("Schema type or value error")

    @classmethod
    def validate_cls(cls, targetcls, dct):
        """
        Validate the class implementing schema
        """
        cls.validate_schema(targetcls, dct)

    ####################################################
    # Schema management
    ####################################################
    @classmethod
    def schema_list(cls):
        """
        List known schemas and handling classes
        """
        summary = [('Schema', 'Class', 'Module')]
        for c in cls._registry:
            mod = sys.modules[c.__module__]
            schemas = c.schema
            if isinstance(schemas, str):
                schemas = [schemas]
            for s in schemas:
                summary.append((s, id(c), c.__name__, mod.__file__))

        return summary

    @classmethod
    def schema_get(cls, schemas):
        """
        List known schemas and handling classes
        """

        if isinstance(schemas, str):
            schemas = [schemas]
        for schema in schemas:
            for c in cls._registry:
                if isinstance(c.schema, str) and c.schema == schema:
                    return c
                elif isinstance(c.schema, list):
                    if schema in c.schema:
                        return c
        raise MeritNoHandler("Unknown schema: {}".format(schema))

    @classmethod
    def schema_unregister(cls, targetcls):
        """
        Unregister cls
        """

        for i, c in enumerate(cls._registry):
            if id(c) == id(targetcls):
                del cls._registry[i]
                return

        raise MeritNotRegistered("Unknown handler")

    @classmethod
    def schema_register(cls, targetcls):
        """
        Register class
        """

        try:
            targetcls.schema_get(targetcls.schema)
            raise MeritDuplicateSchema("Schema already present")
        except MeritNoHandler:
            pass

        # Now register
        cls._registry.append(targetcls)

    def validate(self, metadata=None):
        """
        Check if the metadata is valid

        :param dict metadata: Optional metadata dict to be validated.
              If not specified, will use the class's metadata attribute.
        """

        if metadata is None:
            metadata = self.metadata

        for r in self.required:

            if r not in metadata:
                raise MeritInvalidMetadata("Missing: {}".format(r))

            if hasattr(self, 'validate_' + r):
                func = getattr(self, 'validate_' + r)
                func(metadata[r])


    @abc.abstractmethod
    def initialize(self, *args, **kwargs):
        """
        Initialize the state of the metadata object
        """
        pass

    def dump(self):
        """
        Return the metadata as a dictionary
        """
        self.validate()

        d = [('schema', self.schema)]

        # Take a union of order and required
        order = self.order
        for k in self.required:
            if k not in order:
                order.append(k)

        # => Now follow the order computed
        for k in order:

            if hasattr(self, 'dump_' + k):
                func = getattr(self, 'dump_' + k)
            else:
                func = lambda x: x
            d.append((k, func(self.metadata[k])))

        for k,v in self.metadata.items():
            if k in self.order:
                continue
            if hasattr(self, 'dump_' + k):
                func = getattr(self, 'dump_' + k)
            else:
                func = lambda x: x
            d.append((k, func(v)))

        return collections.OrderedDict(d)

    def load(self, metadata):
        """
        Load a dictionary. Call element-specific handler if it exists.
        """
        if not isinstance(metadata, dict):
            raise MeritInvalidMetadata("Metadata not a dict")

        final = {}
        for k, v in metadata.items():
            if hasattr(self, 'load_' + k):
                func = getattr(self, 'load_' + k)
            else:
                func = lambda x: x
            final[k] = func(v)

        # Check to make sure the metadata is complete and valid
        self.validate(final)

        # Save
        self.metadata = final

    def dumps(self):
        """
        Dump the internal structure into JSON-formatted string
        """
        return json.dumps(self.dump(), indent=4)

    def loads(self, s):
        """
        Load a serialized string into a object
        """
        self.load(json.loads(s))

    def prettyprint(self, max_width=80):
        """
        Dump content in a neat form..
        """

        rows = [
            ('Dimension', 'Summary'),
            ('schema', self.schema)
        ]

        # Take a union of order and required
        order = self.order
        for k in self.required:
            if k not in order:
                order.append(k)

        allkeys = sorted(list(self.metadata.keys()))
        for k in allkeys:
            if k in self.order or k == 'schema':
                continue
            order.append(k)
        # => Now follow the order computed
        for k in order:
            summary = ""
            if isinstance(self.metadata[k],list):
                for v in self.metadata[k]:
                    if hasattr(v, 'prettyprint'):
                        v = v.prettyprint(max_width=max_width-20)
                    else:
                        v = str(v)
                    summary += v + "\n"
            else:
                v = self.metadata[k]
                if hasattr(v, 'prettyprint'):
                    summary = v.prettyprint(max_width=max_width-20)
                else:
                    summary = str(v)
            rows.append((k, summary))

        table = texttable.Texttable(max_width=max_width)
        table.add_rows(rows)
        return table.draw()

    #############################################
    # Helper methods
    #############################################
    @classmethod
    def find_handler_for_schema(cls, schema):
        """
        Find loader for a given schema.

        A class can load one or more schema types.
        """
        for h in cls._registry:
            if ((isinstance(h.schema, str)) and
                (h.schema == schema)):
                return h

            if isinstance(h.schema, list):
                for s in h.schema:
                    if s == schema:
                        return h

        raise MeritNoHandler()

    @classmethod
    def find_handler_for_dict(cls, dct):
        """
        Find the handler class and load dict

        A class can load one or more schema types.
        """
        if not isinstance(dct, dict):
            raise MeritInvalidMetadata("Not a dictionary")

        if 'schema' not in dct:
            raise MeritMissingSchema()

        return cls.find_handler_for_schema(dct['schema'])

    @classmethod
    def find_handler(cls, schema):
        """
        Short form of find_handler_for_schema
        """
        return cls.find_handler_for_schema(schema)


class MeritContextBase(MeritBase):
    """
    Baseclass for context schemas
    """
    schema = "context:base:v1"

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

class MeritResourceBase(MeritBase):
    """
    Baseclass for resource schemas
    """
    schema = "resource:base:v1"

    def initialize(self, *args, **kwargs):
        pass

class MeritGlobalBase(MeritBase):
    """
    Base abstract class for pymerit schema implementors
    """
    schema = "global:base:v1"

    def __init__(self, *args, **kwargs):
        self.metadata = {}
        self.required = [
            'namespace',
            'path',
            'name',
            'description',
            'contexts',
            'resources'
        ]
        self.order = []

        #
        self.initialize()

    # New attributes
    namespace = get_metadata_attribute('namespace')
    path = get_metadata_attribute('path')

    def initialize(self, *args, **kwargs):
        self.metadata = {
            'contexts': [],
            'resources': []
        }

    def add_context(self, c):
        """
        Add a context (e.g., host info) to metadata
        """
        if c is None:
            raise MeritInvalidContext("Null context")

        if not issubclass(c.__class__, MeritContextBase):
            raise MeritInvalidContext("Not a subclass")

        # Validate the context
        c.validate()

        # => Register if it doesnt already exist
        try:
            MeritBase.schema_register(c.__class__)
        except:
            pass


        self.metadata['contexts'].append(c)

    def add_resource(self, r):
        """
        Add a resource (e.g., file) to metadata
        """
        if r is None:
            raise MeritInvalidResource("Null resource")

        if not issubclass(r.__class__, MeritResourceBase):
            raise MeritInvalidResource("Not a subclass")

        # Validate the resource
        r.validate()

        # => Register if it doesnt already exist
        try:
            MeritBase.schema_register(r.__class__)
        except:
            pass

        self.metadata['resources'].append(r)

    def load_contexts(self, contexts):
        """
        Validate and load contexts
        """
        final = []
        for spec in contexts:
            cls = MeritBase.find_handler_for_dict(spec)
            if not issubclass(cls, MeritContextBase):
                raise MeritInvalidMetadata("Non-context specified in context field")
            c = cls()
            c.load(spec)
            final.append(c)
        return final

    def load_resources(self, resources):
        """
        Validate and load resourcess
        """
        final = []
        for spec in resources:
            cls = MeritBase.find_handler_for_dict(spec)
            if not issubclass(cls, MeritResourceBase):
                raise MeritInvalidMetadata("Non-resource specified in resource field")
            c = cls()
            c.load(spec)
            final.append(c)
        return final

    def dump_contexts(self, contexts):
        """
        Dump contexts
        """
        return [c.dump() for c in contexts]

    def dump_resources(self, resources):
        """
        Dump resources
        """
        return [r.dump() for r in resources]

