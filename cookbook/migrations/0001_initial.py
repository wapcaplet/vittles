# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Recipe'
        db.create_table('cookbook_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('directions', self.gf('django.db.models.fields.TextField')()),
            ('servings', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cookbook', ['Recipe'])

        # Adding model 'Preparation'
        db.create_table('cookbook_preparation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cookbook', ['Preparation'])

        # Adding model 'Ingredient'
        db.create_table('cookbook_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Unit'])),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Food'])),
            ('preparation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cookbook.Preparation'], null=True, blank=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cookbook.Recipe'])),
        ))
        db.send_create_signal('cookbook', ['Ingredient'])


    def backwards(self, orm):
        
        # Deleting model 'Recipe'
        db.delete_table('cookbook_recipe')

        # Deleting model 'Preparation'
        db.delete_table('cookbook_preparation')

        # Deleting model 'Ingredient'
        db.delete_table('cookbook_ingredient')


    models = {
        'cookbook.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Food']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preparation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cookbook.Preparation']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cookbook.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']"})
        },
        'cookbook.preparation': {
            'Meta': {'object_name': 'Preparation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cookbook.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'directions': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'servings': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Category']", 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['cookbook']
