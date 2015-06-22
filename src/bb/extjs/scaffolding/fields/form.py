import json

from genshi.template import NewTextTemplate

from zope import component
from zope import schema
from zope.i18n import translate
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory

from bb.extjs.core import ext
from bb.extjs.scaffolding import loader
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeForm


class BuilderBaseForm(BuilderBase):
    ext.baseclass()

    def default(self):
        return dict(name=self.field.getName(),
                    fieldLabel=translate(self.field.title, context=self.recipe.request),
                    emptyText=self.field.default,
                    allowBlank=not self.field.required
                    )


class StringField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IField)

    def __call__(self):
        di = self.default()
        di.update(dict(xtype='textfield'))
        if self.field.max_length is not None:
            di['maxLength'] = self.field.max_length
        if self.field.min_length is not None:
            di['minLength'] = self.field.min_length
        return json.dumps(di, indent=' '*4)


class PasswordField(StringField):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IPassword)

    def __call__(self):
        di = super(PasswordField, self).__call__()
        # super class returns an json string
        di = json.loads(di)
        di.update(dict(inputType='password'))
        return json.dumps(di, indent=' '*4)


class DateField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IDate)

    def __call__(self):
        di = self.default()
        di.update(dict(xtype='datefield'))
        return json.dumps(di, indent=' '*4)


class TimeField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.ITime)

    def __call__(self):
        di = self.default()
        di.update(dict(xtype='timefield'))
        return json.dumps(di, indent=' '*4)


class CheckboxField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IBool)

    def __call__(self):
        di = self.default()
        di.update(dict(xtype='checkboxfield'))
        return json.dumps(di, indent=' '*4)


class IntField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IInt)

    def __call__(self):
        di = self.default()
        di.update(dict(xtype='numberfield'))
        return json.dumps(di, indent=' '*4)


class IdField(IntField):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IId)


class ComboboxField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IChoice)

    def __call__(self):
        # Register the corresponding vocabulary
        factory = component.getUtility(IVocabularyFactory,
                                       name=self.field.vocabularyName)
        vocabular = factory(self.recipe.request)
        vr = vocabulary.getVocabularyRegistry()
        vr.register(self.field.vocabularyName, factory)

        # Get the data to construct the store
        fields = str(['value', 'title'])
        data = list()
        for term in vocabular:
            entry = dict()
            entry['value'] = str(term.value)
            entry['title'] = str(term.title)
            data.append(entry)

        # Attributes for the combobox
        self.name = self.field.getName()
        self.fieldLabel = translate(self.field.title,
                                    context=self.recipe.request)
        self.emptyText = self.field.default
        self.allowBlank = not self.field.required
        self.valueField = 'value'
        self.displayField = 'title'
        self.queryMode = 'local'
        self.store = "Ext.create('Ext.data.Store', {fields: %s, data: %s})" % (str(fields), str(data))

        # Render the template
        tmpl = loader.load('combobox.json.tpl', cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        return stream.render()
