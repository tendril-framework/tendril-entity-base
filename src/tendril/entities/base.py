# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
"""

from tendril.validation.base import ValidatableBase


class EntityNotFound(Exception):
    pass


class EntityHasNoStructure(Exception):
    pass


class EntityBase(ValidatableBase):
    """ Placeholder class for potentially track-able objects.

        Depending on the implementation used, this class should inherit from
        an external class built for this purpose instead of from ``object``.

    """
    def __init__(self, vctx=None):
        super(EntityBase, self).__init__(vctx)
        self._defined = False

    def define(self, *args, **kwargs):
        self._defined = True

    @property
    def defined(self):
        """ State of the component. The component should be used only when
        it is fully defined.

        This is a read-only property.
        """
        return self._defined

    @property
    def ident(self):
        raise NotImplementedError

    @property
    def refdes(self):
        raise NotImplementedError

    @property
    def desc(self):
        raise NotImplementedError

    def json(self):
        return {
            'ident': self.ident,
            'refdes': self.refdes,
            'desc': self.desc,
        }

    def _validate(self):
        pass


class StructuredEntityBase(EntityBase):
    def __init__(self):
        self._structure = None
        super(StructuredEntityBase, self).__init__()

    @property
    def structure(self):
        if not self._structure:
            raise EntityHasNoStructure()
        return self._structure

    @structure.setter
    def structure(self, value):
        if self._structure:
            raise ValueError("Structure is already set for this entity.")
        self._structure = value

    def insert(self, item, *args, **kwargs):
        self.structure.insert(item, *args, **kwargs)

    def contents(self):
        return self.structure.contents()

    def _validate(self):
        pass

    def json(self):
        rval = super(StructuredEntityBase, self).json()
        if self._structure:
            rval['children'] = self.structure.json()
        return rval


class GenericEntity(StructuredEntityBase):
    def __init__(self):
        self._domain = None
        self._ident = None
        self._desc = None
        self._refdes = None
        super(GenericEntity, self).__init__()

    @property
    def domain(self):
        return self._domain

    @property
    def ident(self):
        return self._ident

    @property
    def refdes(self):
        return self._refdes

    @property
    def desc(self):
        return self._desc

    def define(self, **kwargs):
        self._ident = kwargs.pop('ident')
        self._refdes = kwargs.pop('refdes', None)
        self._desc = kwargs.pop('desc', "")
        self._domain = kwargs.pop('domain', None)
        super(GenericEntity, self).define(**kwargs)

    def __repr__(self):
        return '<GenericEntityBase {0} : {1}>' \
               ''.format(self.refdes, self.ident)

    def _validate(self):
        pass


class GroupAwareEntity(GenericEntity):
    def __init__(self):
        self._group = None
        super(GroupAwareEntity, self).__init__()

    @property
    def group_name(self):
        return self._group

    def define(self, **kwargs):
        self._group = kwargs.pop('group')
        super(GroupAwareEntity, self).define(**kwargs)

    def _validate(self):
        pass
