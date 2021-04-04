from django.forms import fields, models, Form, ModelForm


class BS4BaseForm:
    """ Simple base form class for Bootstrap 4 forms"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = []
            if type(field) == fields.BooleanField: # or type(field) == fields.TypedChoiceField:
                css.append('form-check-input')
            elif type(field) == models.ModelMultipleChoiceField:
                #css += ' '
                pass
            else:
                css.append('form-control')
            if type(field) == fields.DateField:
                css.append('ff-datepicker')
            field.widget.attrs['class'] = ' '.join(css)


class BS4Form(BS4BaseForm, Form):
    pass


class BS4ModelForm(BS4BaseForm, ModelForm):
    pass
