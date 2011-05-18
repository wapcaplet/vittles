# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('core_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'Food'
        db.create_table('core_food', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Food'])

        # Adding model 'Unit'
        db.create_table('core_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('core', ['Unit'])

        # Adding model 'Equivalence'
        db.create_table('core_equivalence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Unit'])),
            ('to_quantity', self.gf('django.db.models.fields.FloatField')()),
            ('to_unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Unit'])),
        ))
        db.send_create_signal('core', ['Equivalence'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Food'
        db.delete_table('core_food')

        # Deleting model 'Unit'
        db.delete_table('core_unit')

        # Deleting model 'Equivalence'
        db.delete_table('core_equivalence')


    models = {
        'core.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Category']", 'null': 'True', 'blank': 'True'})
        },
        'core.equivalence': {
            'Meta': {'object_name': 'Equivalence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_quantity': ('django.db.models.fields.FloatField', [], {}),
            'to_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']"})
        },
        'core.food': {
            'Meta': {'object_name': 'Food'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'core.unit': {
            'Meta': {'object_name': 'Unit'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']
