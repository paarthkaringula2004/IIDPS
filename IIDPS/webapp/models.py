from django.db import models

# Create your models here.
class usertab(models.Model):
	n_a_m_e=models.CharField(max_length=149);
	e_mail=models.CharField(max_length=149);
	pass_word=models.CharField(max_length=149);
	phone=models.CharField(max_length=149);

class files(models.Model):
	user=models.CharField(max_length=49);
	username=models.CharField(max_length=49);
	filename=models.CharField(max_length=149);
	filetitle=models.CharField(max_length=149);
	access=models.CharField(max_length=149);
	filedata=models.TextField();
	stz=models.CharField(max_length=14);


class mails(models.Model):
	sender=models.CharField(max_length=49);
	sendername=models.CharField(max_length=49);
	recipient=models.CharField(max_length=149);
	title=models.CharField(max_length=149);
	data=models.CharField(max_length=149);
	datetime=models.CharField(max_length=149);

class scpattern(models.Model):
	user=models.CharField(max_length=49);
	sc_calls=models.TextField();
	freq=models.IntegerField();

class alerts(models.Model):
	aid=models.CharField(max_length=49);
	user=models.CharField(max_length=49);
	sc_calls=models.TextField();
	datetime=models.CharField(max_length=49);
	hostaddr=models.CharField(max_length=249);
	ipaddr=models.CharField(max_length=49);
	intruder=models.CharField(max_length=149);
	stz=models.CharField(max_length=49);
	
	

