# -*- coding: utf-8 -*-
from django.utils.html import escape
from django.forms import LargeTextField
from django.db.models.fields import Field
from django.dispatch import dispatcher
from django.db.models import signals
from django.conf import settings

class TextFieldWithClass(LargeTextField):
    def __init__(self, css_class='', plaintext_field=None, *args, **kwargs):
        self.css_class, self.plaintext_field = css_class, plaintext_field
        LargeTextField.__init__(self, *args, **kwargs)

    def render(self, data):
        if data is None:
            data = ''
        if isinstance(data, unicode):
            data = data.encode(settings.DEFAULT_CHARSET)

        css_class = ''
        if self.css_class != '':
            css_class = ' ' + self.css_class

        return '<textarea id="%s" class="v%s%s%s" name="%s" rows="%s" cols="%s">%s</textarea>' % \
            (self.get_id(), self.__class__.__name__, self.is_required and ' required' or '',
            css_class, self.field_name, self.rows, self.cols, escape(data))

class RichTextFieldWithClass(Field):

    def __init__(self, css_class='', plaintext_field=None, *args, **kwargs):
        self.css_class, self.plaintext_field = css_class, plaintext_field
        Field.__init__(self, *args, **kwargs)

    def set_plaintext_field(self, instance=None):
        from genshi.core import Markup
	plain = Markup(getattr(instance, self.attname)).striptags().stripentities().encode('utf-8')
        setattr(instance, self.plaintext_field, plain)

    def contribute_to_class(self, cls, name):
        super(RichTextFieldWithClass, self).contribute_to_class(cls, name)
	if self.plaintext_field:
            dispatcher.connect(self.set_plaintext_field, signals.pre_save, sender=cls)

    def prepare_field_objs_and_params(self, manipulator, name_prefix):
        field_objs, params = super(RichTextFieldWithClass, self).prepare_field_objs_and_params(manipulator, name_prefix)
        params['css_class'], params['plaintext_field'] = self.css_class, self.plaintext_field
        return (field_objs, params)

    def get_manipulator_field_objs(self):
        return [TextFieldWithClass]

    def get_internal_type(self):
        return 'TextField'
