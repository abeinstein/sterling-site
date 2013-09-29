# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppUser'
        db.create_table(u'suggestions_appuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['AppUser'])

        # Adding model 'AppUserMembership'
        db.create_table(u'suggestions_appusermembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUser'])),
            ('mobile_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.MobileApp'])),
            ('oauth_token', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['AppUserMembership'])

        # Adding model 'Algorithm'
        db.create_table(u'suggestions_algorithm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('number_times_used', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['Algorithm'])

        # Adding model 'SuggestionList'
        db.create_table(u'suggestions_suggestionlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_user_membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUserMembership'])),
            ('algorithm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.Algorithm'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['SuggestionList'])

        # Adding model 'Suggestion'
        db.create_table(u'suggestions_suggestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('suggestion_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.SuggestionList'])),
            ('app_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUser'])),
            ('rank', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('invited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['Suggestion'])


    def backwards(self, orm):
        # Deleting model 'AppUser'
        db.delete_table(u'suggestions_appuser')

        # Deleting model 'AppUserMembership'
        db.delete_table(u'suggestions_appusermembership')

        # Deleting model 'Algorithm'
        db.delete_table(u'suggestions_algorithm')

        # Deleting model 'SuggestionList'
        db.delete_table(u'suggestions_suggestionlist')

        # Deleting model 'Suggestion'
        db.delete_table(u'suggestions_suggestion')


    models = {
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
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'invitation_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number_times_used': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'suggestions.appuser': {
            'Meta': {'object_name': 'AppUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mobile_apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.MobileApp']", 'through': u"orm['suggestions.AppUserMembership']", 'symmetrical': 'False'})
        },
        u'suggestions.appusermembership': {
            'Meta': {'object_name': 'AppUserMembership'},
            'algorithms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['suggestions.Algorithm']", 'through': u"orm['suggestions.SuggestionList']", 'symmetrical': 'False'}),
            'app_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'oauth_token': ('django.db.models.fields.TextField', [], {})
        },
        u'suggestions.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'app_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'suggestion_list': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.SuggestionList']"})
        },
        u'suggestions.suggestionlist': {
            'Meta': {'object_name': 'SuggestionList'},
            'algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.Algorithm']"}),
            'app_user_membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUserMembership']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suggested_friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['suggestions.AppUser']", 'through': u"orm['suggestions.Suggestion']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['suggestions']