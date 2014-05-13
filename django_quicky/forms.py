# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import


from django import forms



class CleanStringFormMixin(object):
    """
        Strip spaces from all text fields, replace windows line break by
        unix line break and replace MS Office quotes by ASCII single quote.
    """
    def clean(self):
        cleaned_data = super(CleanStringFormMixin, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], basestring):
                cleaned_data[field] = (
                    cleaned_data[field].replace('\r\n', '\n')
                    .replace(u'\u2018', "'").replace(u'\u2019', "'").strip())

        return cleaned_data


class CleanStringModelForm(CleanStringFormMixin, forms.ModelForm):
    pass
