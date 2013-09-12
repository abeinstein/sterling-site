# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FbNode.current_app'
        db.delete_column(u'fbNodes_fbnode', 'current_app')

        # Adding field 'FbNode.current_app_id'
        db.add_column(u'fbNodes_fbnode', 'current_app_id',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'FbNode.current_app'
        db.add_column(u'fbNodes_fbnode', 'current_app',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Deleting field 'FbNode.current_app_id'
        db.delete_column(u'fbNodes_fbnode', 'current_app_id')


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
            'current_app_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
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