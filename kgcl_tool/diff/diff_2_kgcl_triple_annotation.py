import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
from rdflib import BNode, URIRef, Literal
from model.kgcl import (
    NodeRename,
    NodeObsoletion,
    NodeUnobsoletion,
    NodeDeletion,
    NodeMove,
    NodeDeepening,
    NodeShallowing,
    EdgeCreation,
    EdgeDeletion,
    PredicateChange,
    NodeCreation,
    ClassCreation,
    PlaceUnder,
    RemoveUnder,
    NewSynonym,
    RemovedNodeFromSubset,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from diff.change_detection import (
    detect_renamings,
    detect_node_moves,
    detect_predicate_changes,
)
from diff.owlstar_sublanguage import (
    get_triple_annotations,
    get_bnodes_2_triple_annotations,
)
from diff.graph_diff import (
    get_added_triple_annotations,
    get_deleted_triple_annotations,
    get_added_existentials,
    get_deleted_existentials,
)
from diff.render_operations import render
from model.ontology_model import Edge, Annotation


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


class TripleAnnotationChangeSummary:
    def __init__(self):

        self.triple_annotations_additions = []
        self.triple_annotations_deletions = []
        self.covered_triples_triple_annotations_additions = []
        self.covered_triples_triple_annotations_deletions = []

    def get_commands(self):
        kgcl_commands = []
        for k in self.triple_annotations_additions:
            kgcl_commands.append(k)
        for k in self.triple_annotations_deletions:
            kgcl_commands.append(k)
        return kgcl_commands

    def get_triple_annotation_additions(self):
        return self.triple_annotations_additions

    def get_triple_annotation_deletions(self):
        return self.triple_annotations_deletions

    def get_summary_KGCL_commands(self):
        out = (
            "Triple Annotation Additions: "
            + str(len(self.triple_annotations_additions))
            + "\n"
            "Triple Annotation Deletions: "
            + str(len(self.triple_annotations_deletions))
            + "\n"
        )
        return out

    def get_summary_RDF_triples(self):
        out = (
            "Triple Annotation Additions: "
            + str(len(self.covered_triples_triple_annotations_additions))
            + "\n"
            "Triple Annotation Deletions: "
            + str(len(self.covered_triples_triple_annotations_deletions))
            + "\n"
        )
        return out

    # RDF data

    def get_covered_triples_annotation_additions(self):
        return self.covered_triples_triple_annotations_additions

    def get_covered_triples_annotation_deletions(self):
        return self.covered_triples_triple_annotations_deletions

    def add_covered_triples_annotation_additions(self, triples):
        for t in triples:
            self.covered_triples_triple_annotations_additions.append(t)

    def add_covered_triples_annotation_deletions(self, triples):
        for t in triples:
            self.covered_triples_triple_annotations_deletions.append(t)

    # KGCL data

    def add_triple_annotation_addition(self, i):
        self.triple_annotations_additions.append(i)

    def add_triple_annotation_deletion(self, i):
        self.triple_annotations_deletions.append(i)


def generate_triple_annotation_commands(g1, g2):
    summary = TripleAnnotationChangeSummary()

    added = get_added_triple_annotations(g1, g2)
    deleted = get_deleted_triple_annotations(g1, g2)

    additions, covered = generate_triple_annotation_additions(added)
    summary.add_covered_triples_annotation_additions(covered)

    deletions, covered = generate_triple_annotation_deletions(deleted)
    summary.add_covered_triples_annotation_deletions(covered)

    for a in additions:
        summary.add_triple_annotation_addition(render(a))
    for d in deletions:
        summary.add_triple_annotation_deletion(render(d))

    return summary


def generate_triple_annotation_additions(added):
    covered = rdflib.Graph()
    kgcl = []

    for a in added:
        source = str(a.source)
        property = str(a.property)
        target = str(a.target)
        target_type = get_type(a.target)
        annotation_property = str(a.annotation_property)
        annotation = str(a.annotation)
        annotation_type = get_type(a.annotation)

        id = "test_id_" + str(next(id_gen))

        language = get_language_tag(a.target)
        datatype = get_datatype(a.target)

        annotation = Annotation(
            property=annotation_property, filler=annotation, filler_type=annotation_type
        )

        node = EdgeCreation(
            id=id,
            subject=source,
            predicate=property,
            object=target,
            object_type=target_type,
            annotation_set=annotation,
            language=language,
            datatype=datatype,
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


def generate_triple_annotation_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    for a in deleted:
        source = str(a.source)
        property = str(a.property)
        target = str(a.target)
        target_type = get_type(a.target)
        annotation_property = str(a.annotation_property)
        annotation = str(a.annotation)
        annotation_type = get_type(a.annotation)

        id = "test_id_" + str(next(id_gen))

        language = get_language_tag(a.target)
        datatype = get_datatype(a.target)

        annotation = Annotation(
            property=annotation_property, filler=annotation, filler_type=annotation_type
        )

        node = EdgeDeletion(
            id=id,
            subject=source,
            predicate=property,
            object=target,
            object_type=target_type,
            annotation_set=annotation,
            language=language,
            datatype=datatype,
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


# TODO: factor these out in some kind of utility library


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "IRI"
    elif isinstance(rdf_entity, Literal):
        return "Literal"
    else:
        return "Error"


def get_language_tag(rdf_entity):
    if isinstance(rdf_entity, Literal):
        return rdf_entity.language
    else:
        return None


def get_datatype(rdf_entity):
    if isinstance(rdf_entity, Literal) and rdf_entity.datatype is not None:
        return str(rdf_entity.datatype)
    else:
        return None
