from neomodel import StructuredNode, UniqueIdProperty, StringProperty, IntegerProperty, \
    RelationshipTo

from authors.models import Author
from crossdb import RDRelationship, CrossDBModel


class Book(
    CrossDBModel,
    StructuredNode,
):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)

    author = RDRelationship('authors.models.Author', 'author_id')
    author_id = IntegerProperty()

    aaaa = RelationshipTo('Book', 'HAS_CHILD')

    # @property
    # def author(self):
    #     if 'author' not in self._data:
    #         self._data['author'] = Author.objects.filter(pk=self.author_id)
    #     return self._data['author']
    # traverse outgoing IS_FROM relations, inflate to Country objects
    # country = RelationshipTo(Country, 'IS_FROM')
