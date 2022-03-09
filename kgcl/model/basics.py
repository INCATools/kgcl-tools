# Auto generated from basics.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-08-19 15:44
# Schema: basics
#
# id: https://w3id.org/kgcl/basics
# description: Core predicates
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (EnumDefinition, PermissibleValue,
                                              PvFormulaOptions)
from linkml_runtime.linkml_model.types import String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import \
    dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (YAMLRoot, extended_float,
                                            extended_int, extended_str)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BASICS = CurieNamespace("basics", "https://w3id.org/kgcl/basics/")
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
XML = CurieNamespace("xml", "http://example.org/UNKNOWN/xml/")
DEFAULT_ = BASICS


# Types
class LanguageTag(str):
    type_class_uri = XML.lang
    type_class_curie = "xml:lang"
    type_name = "language tag"
    type_model_uri = BASICS.LanguageTag


# Class references


# Enumerations


# Slots
class slots:
    pass


slots.id = Slot(
    uri=BASICS.id,
    name="id",
    curie=BASICS.curie("id"),
    model_uri=BASICS.id,
    domain=None,
    range=URIRef,
)

slots.description = Slot(
    uri=DCTERMS.description,
    name="description",
    curie=DCTERMS.curie("description"),
    model_uri=BASICS.description,
    domain=None,
    range=Optional[str],
)
