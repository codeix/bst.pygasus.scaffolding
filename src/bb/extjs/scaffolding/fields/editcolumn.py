from zope import schema
from zope.i18n import translate

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.fields import column
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeEditGrid


class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IField)

    def __call__(self):
        return dict(dataIndex=self.field.getName(),
                    text=translate(self.field.title, context=self.recipe.request),
                    field=dict(xtype='textfield'))


class PasswordField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IPassword)

    def __call__(self):
        di = super(PasswordField, self).__call__()
        di.update(dict(inputType='password'))
        return di


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IDate)

    def __call__(self):
        di = super(DateField, self).__call__()
        di.update(dict(dict(field=dict(xtype='datefield')),
                       dateFormat='Y-m-d H:i:s.u'))
        return di


class TimeField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.ITime)

    def __call__(self):
        di = super(DateField, self).__call__()
        di.update(dict(dict(field=dict(xtype='timefield')),
                       dateFormat='H:i:s.u'))
        return di


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = super(FloatField, self).__call__()
        di.update(dict(field=dict(xtype='numberfield')))
        return di


class IdField(column.DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IId)
