# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AppSettings.mobile_app'
        db.alter_column(u'apps_appsettings', 'mobile_app_id', self.gf('annoying.fields.AutoOneToOneField')(to=orm['apps.MobileApp'], unique=True))

    def backwards(self, orm):

        # Changing field 'AppSettings.mobile_app'
        db.alter_column(u'apps_appsettings', 'mobile_app_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['apps.MobileApp'], unique=True))

    models = {
        u'apps.appsettings': {
            'Meta': {'object_name': 'AppSettings'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes_books': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_games': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_music': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_nature': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_restaurants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_sports': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_technology': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_app': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['apps.MobileApp']", 'unique': 'True'}),
            'political_bias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'same_city': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'social_circle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'apps.devmembership': {
            'Meta': {'object_name': 'DevMembership'},
            'date_joined': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'apps.mobileapp': {
            'Meta': {'object_name': 'MobileApp'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.Algorithm']", 'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'invitation_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['apps.DevMembership']", 'symmetrical': 'False'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'suggestions.algorithm': {
            'Meta': {'object_name': 'Algorithm'},
            'algorithm_method_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number_times_used': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['apps']