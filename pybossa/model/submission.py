# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2016 SkyDNS LLC.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Integer, Boolean, Float, UnicodeText, Text
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy import null

from pybossa.core import db
from pybossa.model import DomainObject, make_timestamp
from pybossa.model.user import User
from pybossa.model.project import Project


class Submission(db.Model, DomainObject):
    ''' An extension to support ML-contest-like workflow.
    Contains predicted values for objects represented as tasks within a certain project
    '''
    __tablename__ = 'submission'

    #: Submission.ID
    id = Column(Integer, primary_key=True)
    #: In this ML extension, some train/test set is represented by a pybossa project referred here
    project_id = Column(Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    #: Author of the submission
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #: UTC timestamp of the submission
    timestamp = Column(Text, default=make_timestamp)
    #: Model tag to select submissions by a model in development they've been produced with
    model_tag = Column(Text, nullable=False)
    #: Model revision, e.g. a commit hash that is kept for reproducibility
    model_revision = Column(Text, nullable=False)
    #: Force model revision to change on submission
    unique_model = UniqueConstraint(project_id, author_id, model_tag, model_revision)
    #: Optional comment
    comment = Column(UnicodeText)
    #: Submitted predictions
    predictions = Column(JSON, nullable=False, default=null())

    author = relationship(User, backref='submissions')
    project = relationship(Project, backref='submissions')

