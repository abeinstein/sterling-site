# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SignUp'
        db.create_table(u'splash_signup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'splash', ['SignUp'])


    def backwards(self, orm):
        # Deleting model 'SignUp'
        db.delete_table(u'splash_signup')


    models = {
        u'splash.signup': {
            'Meta': {'object_name': 'SignUp'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['splash']