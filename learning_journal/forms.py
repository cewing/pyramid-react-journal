# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import (
    Form,
    HiddenField,
    TextField,
    TextAreaField,
    validators,
    )

strip_filter = lambda x: x.strip() if x else None


class EntryCreateForm(Form):
    title = TextField(
        'Title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter]
    )
    text = TextAreaField(
        'Entry',
        [validators.Length(min=1)],
        filters=[strip_filter]
    )


class EntryUpdateForm(EntryCreateForm):
    id = HiddenField()
