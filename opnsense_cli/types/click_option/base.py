from abc import ABC, abstractmethod
from bs4.element import Tag
from string import Template
import textwrap


class ClickOptionCodeFragment(ABC):
    def __init__(self, tag: Tag):
        self._tag_content = tag
        self.__name = tag.name
        self.__template = Template(textwrap.dedent(self.TEMPLATE_CREATE))

    @property
    @abstractmethod
    def TEMPLATE_CREATE(self):
        """ This property should be implemented. """

    def get_code_for_create(self):
        self._template = self.TEMPLATE_CREATE
        return self._render_template()

    @property
    @abstractmethod
    def TEMPLATE_UPDATE(self):
        """ This property should be implemented. """

    def get_code_for_update(self):
        self._template = self.TEMPLATE_UPDATE
        return self._render_template()

    @abstractmethod
    def _render_template(self):
        """ This method should be implemented. """

    @property
    def _template(self):
        return self.__template

    @_template.setter
    def _template(self, _template):
        self.__template = Template(textwrap.dedent(_template))

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, name):
        self.__name = name

    @property
    def _required(self):
        if self._tag_content.find(name='Required', text='Y'):
            return "required=True,"
        return "required=False,"

    @property
    def _default(self):
        if self._tag_content.find(name='default'):
            return f"default={self._tag_content.default.string},"
        return "default=None,"

    @property
    def _multiple(self):
        if self._tag_content.find(name='Multiple', text='Y') or self._tag_content.find(name='multiple', text='Y'):
            return "multiple=True,"
        return "multiple=False,"