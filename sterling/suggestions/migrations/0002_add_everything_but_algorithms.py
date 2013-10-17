# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("apps", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'AppUser'
        db.create_table(u'suggestions_appuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['AppUser'])

        # Adding M2M table for field friends on 'AppUser'
        m2m_table_name = db.shorten_name(u'suggestions_appuser_friends')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_appuser', models.ForeignKey(orm[u'suggestions.appuser'], null=False)),
            ('to_appuser', models.ForeignKey(orm[u'suggestions.appuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_appuser_id', 'to_appuser_id'])

        # Adding model 'AppUserMembership'
        db.create_table(u'suggestions_appusermembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUser'])),
            ('mobile_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.MobileApp'])),
            ('oauth_token', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['AppUserMembership'])

        # Adding unique constraint on 'AppUserMembership', fields ['app_user', 'mobile_app']
        db.create_unique(u'suggestions_appusermembership', ['app_user_id', 'mobile_app_id'])

        # Adding model 'SuggestionList'
        db.create_table(u'suggestions_suggestionlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_user_membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUserMembership'])),
            ('algorithm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.Algorithm'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('presented_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'suggestions', ['SuggestionList'])

        # Adding unique constraint on 'SuggestionList', fields ['app_user_membership', 'algorithm']
        db.create_unique(u'suggestions_suggestionlist', ['app_user_membership_id', 'algorithm_id'])

        # Adding model 'Suggestion'
        db.create_table(u'suggestions_suggestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('suggestion_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.SuggestionList'])),
            ('app_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suggestions.AppUser'])),
            ('rank', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('times_presented', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_presented_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('times_invited', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_invited_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'suggestions', ['Suggestion'])

        # Adding unique constraint on 'Suggestion', fields ['suggestion_list', 'app_user']
        db.create_unique(u'suggestions_suggestion', ['suggestion_list_id', 'app_user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Suggestion', fields ['suggestion_list', 'app_user']
        db.delete_unique(u'suggestions_suggestion', ['suggestion_list_id', 'app_user_id'])

        # Removing unique constraint on 'SuggestionList', fields ['app_user_membership', 'algorithm']
        db.delete_unique(u'suggestions_suggestionlist', ['app_user_membership_id', 'algorithm_id'])

        # Removing unique constraint on 'AppUserMembership', fields ['app_user', 'mobile_app']
        db.delete_unique(u'suggestions_appusermembership', ['app_user_id', 'mobile_app_id'])

        # Deleting model 'AppUser'
        db.delete_table(u'suggestions_appuser')

        # Removing M2M table for field friends on 'AppUser'
        db.delete_table(db.shorten_name(u'suggestions_appuser_friends'))

        # Deleting model 'AppUserMembership'
        db.delete_table(u'suggestions_appusermembership')

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
            'default_algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.Algorithm']", 'null': 'True', 'blank': 'True'}),
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
            'algorithm_method_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number_times_used': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'suggestions.appuser': {
            'Meta': {'object_name': 'AppUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': u"orm['suggestions.AppUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.MobileApp']", 'through': u"orm['suggestions.AppUserMembership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'suggestions.appusermembership': {
            'Meta': {'unique_together': "(('app_user', 'mobile_app'),)", 'object_name': 'AppUserMembership'},
            'algorithms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['suggestions.Algorithm']", 'through': u"orm['suggestions.SuggestionList']", 'symmetrical': 'False'}),
            'app_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'oauth_token': ('django.db.models.fields.TextField', [], {})
        },
        u'suggestions.suggestion': {
            'Meta': {'ordering': "['rank']", 'unique_together': "(('suggestion_list', 'app_user'),)", 'object_name': 'Suggestion'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'app_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_invited_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_presented_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'suggestion_list': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.SuggestionList']"}),
            'times_invited': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'times_presented': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'suggestions.suggestionlist': {
            'Meta': {'unique_together': "(('app_user_membership', 'algorithm'),)", 'object_name': 'SuggestionList'},
            'algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.Algorithm']"}),
            'app_user_membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['suggestions.AppUserMembership']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presented_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'suggested_friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['suggestions.AppUser']", 'through': u"orm['suggestions.Suggestion']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['suggestions']