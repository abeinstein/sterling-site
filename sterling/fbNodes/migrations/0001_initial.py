# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FbNode'
        db.create_table(u'fbNodes_fbnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.TextField')(max_length=50, primary_key=True)),
            ('o_auth_token', self.gf('django.db.models.fields.TextField')()),
            ('current_app_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'fbNodes', ['FbNode'])

        # Adding M2M table for field apps on 'FbNode'
        m2m_table_name = db.shorten_name(u'fbNodes_fbnode_apps')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fbnode', models.ForeignKey(orm[u'fbNodes.fbnode'], null=False)),
            ('mobileapp', models.ForeignKey(orm[u'apps.mobileapp'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fbnode_id', 'mobileapp_id'])

        # Adding model 'SuggestionsNode'
        db.create_table(u'fbNodes_suggestionsnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.FbNode'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.MobileApp'])),
            ('suggestions_list', self.gf('django.db.models.fields.TextField')()),
            ('algorithm_id', self.gf('django.db.models.fields.TextField')()),
            ('node_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'fbNodes', ['SuggestionsNode'])

        # Adding model 'InvitationNode'
        db.create_table(u'fbNodes_invitationnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.FbNode'])),
            ('invited_id', self.gf('django.db.models.fields.TextField')()),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.MobileApp'])),
            ('link_clicked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('link_clicked_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('join_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('node_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'fbNodes', ['InvitationNode'])

        # Adding model 'InvitationsNode'
        db.create_table(u'fbNodes_invitationsnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.FbNode'])),
            ('invited_list', self.gf('django.db.models.fields.TextField')()),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.MobileApp'])),
            ('node_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'fbNodes', ['InvitationsNode'])


    def backwards(self, orm):
        # Deleting model 'FbNode'
        db.delete_table(u'fbNodes_fbnode')

        # Removing M2M table for field apps on 'FbNode'
        db.delete_table(db.shorten_name(u'fbNodes_fbnode_apps'))

        # Deleting model 'SuggestionsNode'
        db.delete_table(u'fbNodes_suggestionsnode')

        # Deleting model 'InvitationNode'
        db.delete_table(u'fbNodes_invitationnode')

        # Deleting model 'InvitationsNode'
        db.delete_table(u'fbNodes_invitationsnode')


    models = {
        u'apps.membership': {
            'Meta': {'object_name': 'Membership'},
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
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['apps.Membership']", 'symmetrical': 'False'})
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
        u'fbNodes.fbnode': {
            'Meta': {'object_name': 'FbNode'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['apps.MobileApp']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_app_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'o_auth_token': ('django.db.models.fields.TextField', [], {}),
            'user_id': ('django.db.models.fields.TextField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        u'fbNodes.invitationnode': {
            'Meta': {'object_name': 'InvitationNode'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invited_id': ('django.db.models.fields.TextField', [], {}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.FbNode']"}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'link_clicked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link_clicked_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'node_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'fbNodes.invitationsnode': {
            'Meta': {'object_name': 'InvitationsNode'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invited_list': ('django.db.models.fields.TextField', [], {}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.FbNode']"}),
            'node_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'fbNodes.suggestionsnode': {
            'Meta': {'object_name': 'SuggestionsNode'},
            'algorithm_id': ('django.db.models.fields.TextField', [], {}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.MobileApp']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'suggestions_list': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.FbNode']"})
        }
    }

    complete_apps = ['fbNodes']