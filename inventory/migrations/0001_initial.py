# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Place'
        db.create_table('inventory_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('inventory', ['Place'])

        # Adding model 'Provision'
        db.create_table('inventory_provision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Unit'], null=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Food'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='provisions', null=True, to=orm['inventory.Place'])),
        ))
        db.send_create_signal('inventory', ['Provision'])


    def backwards(self, orm):
        
        # Deleting model 'Place'
        db.delete_table('inventory_place')

        # Deleting model 'Provision'
        db.delete_table('inventory_provision')


    models = {
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
        },
        'inventory.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'inventory.provision': {
            'Meta': {'object_name': 'Provision'},
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Food']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provisions'", 'null': 'True', 'to': "orm['inventory.Place']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']", 'null': 'True'})
        }
    }

    complete_apps = ['inventory']
