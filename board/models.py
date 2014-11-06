# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from djangotoolbox.fields import ListField, EmbeddedModelField

class Votable(models.Model):
	class Meta:
		abstract = True

	upvotes		= models.IntegerField(default=0)
	downvotes	= models.IntegerField(default=0)
	voters		= ListField(models.ForeignKey(User))

class Group(models.Model):
	class Meta:
		abstract = True

	blocks		= ListField(EmbeddedModelField())

class Post(Votable):
	parent		= models.ForeignKey('self', null=True, blank=True, related_name='replies')
	author		= models.ForeignKey(User)
	title		= models.TextField(null=True, blank=True)
	groups		= ListField(EmbeddedModelField(Group))
	created		= models.DateTimeField(auto_now_add=True)
	modified	= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s (replies:%d)" % (self.title, self.replies.count())

class Block(Votable):
	QUESTION	= 'question'
	ARGUMENT	= 'argument'
	CRITIC		= 'critic'
	ASSERTION	= 'assertion'
	QUOTE		= 'quote'

	BLOCK_TYPES = (
		(QUESTION,'question'),
		(ARGUMENT,'argument'),
		(CRITIC,'critic'),
		(ASSERTION,'assertion'),
		(QUOTE,'quote'),
	)

	type = models.CharField(choices=BLOCK_TYPES, max_length=10)
	body = models.TextField()

	def __unicode__(self):
		return "%s" % (self.type)

class BlockQuote(models.Model):
	author = models.CharField(max_length=200)
	block = EmbeddedModelField()

class Quote(Block):
	author = models.CharField(max_length=200)
#	source = EmbeddedModelField('Source')

# Source är en ny app, typ SourceManager eller liknande.
# Där en rootkälla är en hemsida/bok, och en sida där citat
# hämtats är en källa.
