# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
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

from default import Test, db, with_context
from nose.tools import assert_raises
from sqlalchemy.exc import IntegrityError
from pybossa.model.user import User
from pybossa.model.project import Project
from pybossa.model.category import Category
from pybossa.model.submission import Submission



class TestModelSubmission(Test):

    @with_context
    def test_submission_model(self):
        user = User(
            email_addr=u"john.doe@example.com",
            name=u"johndoe",
            fullname=u"John Doe",
            locale=u"en"
        )
        db.session.add(user)
        db.session.commit()
        user = db.session.query(User).first()

        category = Category(name=u'cat', short_name=u'cat', description=u'cat')
        db.session.add(category)
        db.session.commit()
        category = db.session.query(Category).first()
        project = Project(name=u'Application', short_name=u'app', description=u'desc',
                  owner_id=user.id, category=category)
        db.session.add(project)
        db.session.commit()
        project = db.session.query(Project).first()

        s1 = Submission(author=user,
                        project=project,
                        model_tag=u'model',
                        model_revision=u'revision',
                        predictions=u'lek')

        db.session.add(s1)
        db.session.commit()
        submitted = db.session.query(Submission).first()

        assert submitted in user.submissions
        assert submitted in project.submissions
        assert any(submitted in p.submissions for p in category.projects)
        assert submitted.author_id == user.id
        assert submitted.model_tag == s1.model_tag
        assert submitted.model_revision == s1.model_revision
        assert submitted.predictions == s1.predictions

    @with_context
    def test_constraints(self):
        user = User(
            email_addr=u"john.doe@example.com",
            name=u"johndoe",
            fullname=u"John Doe",
            locale=u"en"
        )
        db.session.add(user)
        db.session.commit()
        user = db.session.query(User).first()

        category = Category(name=u'cat', short_name=u'cat', description=u'cat')
        db.session.add(category)
        db.session.commit()
        category = db.session.query(Category).first()
        project = Project(name=u'Application', short_name=u'app', description=u'desc',
                          owner_id=user.id, category=category)
        db.session.add(project)
        db.session.commit()
        project = db.session.query(Project).first()

        model_tag = u'model'
        model_revision = u'revision'
        predictions = [1.0, -1.0]

        s1 = Submission(author_id=user.id,
                        project_id=project.id,
                        model_tag=model_tag,
                        model_revision=model_revision,
                        predictions=predictions)

        for value in (None, 12345):
            s1.author_id = value
            db.session.add(s1)
            assert_raises(IntegrityError, db.session.commit)
            db.session.rollback()
        s1.author_id = user.id

        for value in (None, 12345):
            s1.project_id = value
            db.session.add(s1)
            assert_raises(IntegrityError, db.session.commit)
            db.session.rollback()
            s1.project_id = project.id

        s1.model_tag = None
        db.session.add(s1)
        assert_raises(IntegrityError, db.session.commit)
        db.session.rollback()
        s1.model_tag = model_tag

        s1.model_revision = None
        db.session.add(s1)
        assert_raises(IntegrityError, db.session.commit)
        db.session.rollback()
        s1.model_revision = model_revision

        s1.predictions = None
        db.session.add(s1)
        assert_raises(IntegrityError, db.session.commit)
        db.session.rollback()
        s1.predictions = predictions

        db.session.add(s1)
        db.session.commit

        s2 = Submission(author_id=user.id,
                        project_id=project.id,
                        model_tag=model_tag,
                        model_revision=model_revision,
                        predictions=[1.0, 1.0])

        db.session.add(s2)
        assert_raises(IntegrityError, db.session.commit)
        db.session.rollback()


        s3 = Submission(author_id=user.id,
                        project_id=project.id,
                        model_tag=model_tag,
                        model_revision="new revision",
                        predictions=[1.0, 1.0])
        db.session.add(s3)
        db.session.commit()
