import json

from zope import schema
from zope.i18n import translate

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.fields import column
from bb.extjs.scaffolding.fields import form
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeEditGrid


class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IField)

    def __call__(self):
        di = dict(dataIndex=self.field.getName(),
                  text=translate(self.field.title,
                                 context=self.recipe.request),
                  field=dict(xtype='textfield'))
        return json.dumps(di, indent=' ' * 4)


class PasswordField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IPassword)

    def __call__(self):
        di = json.loads(super(PasswordField, self).__call__())
        di.update(dict(inputType='password'))
        return json.dumps(di, indent=' ' * 4)


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IDate)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(dict(field=dict(xtype='datefield')),
                       dateFormat='Y-m-d H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class TimeField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.ITime)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(dict(field=dict(xtype='timefield')),
                       dateFormat='H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = json.loads(super(FloatField, self).__call__())
        di.update(dict(field=dict(xtype='numberfield')))
        return json.dumps(di, indent=' ' * 4)


class IdField(column.DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IId)


class ChoiceField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IChoice)

    def __call__(self):
        di = json.loads(super(ChoiceField, self).__call__())
        # Create a combobox (same as form recipe)
        combobox = form.ChoiceField(self.recipe, self.field)()
        # But with empty fieldLabel
        combobox = combobox.replace(self.field.title, '')
        di.update(field="%combobox%")
        di = json.dumps(di, indent=' ' * 4)
        di = di.replace('"%combobox%"', combobox)
        return di
