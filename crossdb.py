import sys
from importlib import _bootstrap
from typing import Any

from past.types import basestring


class CrossDBRelationship:

    def __init__(self, cls_path: str, field_name: str, many: bool = False):
        pass

    def generate_fake_fields(self, cls, field_name, many: bool):
        pass

    def generate_setter(self):
        pass




class RelationshipManager(object):
    def __init__(self, source, key, definition, target_class):
        self.source = source
        self.source_class = source.__class__
        self.name = key
        self.definition = definition
        self.target_class = target_class



class RelationalManager(RelationshipManager):
    def all(self):
        print(self.source)
        print(self.source_class)
        print(self.name)
        print(self.definition)
        
        fld = getattr(self.source, self.definition['field_name'])
        return_set = self.target_class.objects.filter(pk=fld)
        return return_set








class RDRelationship:

    def __init__(self,
                 _raw_class,
                 field_name: str,
                 many: bool = False,
                 manager=RelationalManager):
        self._raw_class = _raw_class
        self.module_name = sys._getframe(4).f_globals['__name__']
        self.manager = manager
        self.definition = {
            'field_name': field_name,
        }
        if '__file__' in sys._getframe(4).f_globals:
            self.module_file = sys._getframe(4).f_globals['__file__']

        self.target_class = self._lookup_target_class()
        # self.generate_fake_fields(cls_name, field_name, many)

    def generate_fake_fields(self, cls, field_name, many: bool):
        pass

    def _lookup_target_class(self):
        if not isinstance(self._raw_class, basestring):
            return self._raw_class
        else:
            name = self._raw_class
            if name.find('.') == -1:
                module = self.module_name
            else:
                module, _, name = name.rpartition('.')

            if module not in sys.modules:
                # yet another hack to get around python semantics
                # __name__ is the namespace of the parent module for __init__.py files,
                # and the namespace of the current module for other .py files,
                # therefore there's a need to define the namespace differently for
                # these two cases in order for . in relative imports to work correctly
                # (i.e. to mean the same thing for both cases).
                # For example in the comments below, namespace == myapp, always
                if not hasattr(self, 'module_file'):
                    raise ImportError("Couldn't lookup '{0}'".format(name))

                if '__init__.py' in self.module_file:
                    # e.g. myapp/__init__.py -[__name__]-> myapp
                    namespace = self.module_name
                else:
                    # e.g. myapp/models.py -[__name__]-> myapp.models
                    namespace = self.module_name.rpartition('.')[0]

                # load a module from a namespace (e.g. models from myapp)
                if module:
                    module = import_module(module, namespace).__name__
                # load the namespace itself (e.g. myapp)
                # (otherwise it would look like import . from myapp)
                else:
                    module = import_module(namespace).__name__
            return getattr(sys.modules[module], name)

    def build_cross_manager(self, source, name):
        print("HM?")
        self._lookup_target_class()
        return self.manager(source, name, self.definition, self.target_class)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    level = 0
    if name.startswith('.'):
        if not package:
            msg = ("the 'package' argument is required to perform a relative "
                   "import for {!r}")
            raise TypeError(msg.format(name))
        for character in name:
            if character != '.':
                break
            level += 1
    return _bootstrap._gcd_import(name[level:], package, level)


class CrossDBModel(object):
    GENERATED_ID_FIELDS: dict
    _data = dict()

    def __new__(cls, *args, **kwargs) -> Any:
        cls = super(CrossDBModel, cls).__new__(cls)


        cls.__all_cross_relationships__ = tuple(
            cls.defined_cross_relationships(rels=True).items()
        )

        return cls

    def __init__(self, *args, **kwargs) -> None:

        print("INIT")
        for key, val in self.__all_cross_relationships__:
            print(f"SET dict[{key}]={val}...")
            self.__dict__[key] = val.build_cross_manager(self, key)

        super().__init__(*args, **kwargs)




    @classmethod
    def defined_cross_relationships(cls, rels=False):
        props = {}
        for baseclass in reversed(cls.__mro__):
            props.update(dict(
                (name, property) for name, property in vars(baseclass).items()
                if rels and isinstance(property, RDRelationship)
            ))
        return props


    # def generate_faked_fields(self):
    #     for rel, field in self.GENERATED_ID_FIELDS.values():


