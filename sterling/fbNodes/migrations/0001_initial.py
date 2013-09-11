# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppNode'
        db.create_table(u'fbNodes_appnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('app_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'fbNodes', ['AppNode'])

        # Adding model 'FbNode'
        db.create_table(u'fbNodes_fbnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.TextField')(max_length=50, primary_key=True)),
            ('o_auth_token', self.gf('django.db.models.fields.TextField')()),
            ('current_app', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'fbNodes', ['FbNode'])

        # Adding M2M table for field apps on 'FbNode'
        m2m_table_name = db.shorten_name(u'fbNodes_fbnode_apps')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fbnode', models.ForeignKey(orm[u'fbNodes.fbnode'], null=False)),
            ('appnode', models.ForeignKey(orm[u'fbNodes.appnode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fbnode_id', 'appnode_id'])

        # Adding model 'SuggestionsNode'
        db.create_table(u'fbNodes_suggestionsnode', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.FbNode'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.AppNode'])),
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
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.AppNode'])),
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
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbNodes.AppNode'])),
            ('node_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'fbNodes', ['InvitationsNode'])


    def backwards(self, orm):
        # Deleting model 'AppNode'
        db.delete_table(u'fbNodes_appnode')

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
        u'fbNodes.appnode': {
            'Meta': {'object_name': 'AppNode'},
            'app_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'fbNodes.fbnode': {
            'Meta': {'object_name': 'FbNode'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['fbNodes.AppNode']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_app': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'o_auth_token': ('django.db.models.fields.TextField', [], {}),
            'user_id': ('django.db.models.fields.TextField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        u'fbNodes.invitationnode': {
            'Meta': {'object_name': 'InvitationNode'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.AppNode']"}),
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
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.AppNode']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invited_list': ('django.db.models.fields.TextField', [], {}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.FbNode']"}),
            'node_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'fbNodes.suggestionsnode': {
            'Meta': {'object_name': 'SuggestionsNode'},
            'algorithm_id': ('django.db.models.fields.TextField', [], {}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.AppNode']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'suggestions_list': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbNodes.FbNode']"})
        }
    }

    complete_apps = ['fbNodes']