from django.db import models


class Projeto(models.Model):
    nome_proj = models.CharField(max_length=50)
    desc_proj = models.TextField()
   
    def __unicode__(self):
        return u'%s' % self.nome_proj


class Funcionario(models.Model):
    nome_func = models.CharField(max_length=20)
    sobrenome_func = models.CharField(max_length=100)
    participa = models.ManyToManyField(Projeto, through='Membro')

    def __unicode__(self):
        return u'%s %s' %(self.nome_func, self.sobrenome_func)
       
class Membro(models.Model):
    proj_id=models.ForeignKey(Projeto)
    func_id=models.ForeignKey(Funcionario)


class Andamento(models.Model):
   
    tipo = models.CharField(max_length=30)
   
    def __unicode__(self):
        return u'%s' % self.tipo

class OS(models.Model):
    proj_id=models.ForeignKey(Projeto)
    adamento_id=models.ForeignKey(Andamento)
    participa = models.ManyToManyField(Funcionario, through='Desenvolve')
    num_os= models.CharField(max_length=50)
    data_ini = models.DateTimeField()
    data_fim = models.DateTimeField()
    desc_os = models.TextField()
   
    def __unicode__(self):
        return u'%s' % self.num_os
   
    def save(self):
        os_save=super(OS,self).save()
       
class Desenvolve(models.Model):
    os_id=models.ForeignKey(OS)
    func_id=models.ForeignKey(Funcionario)
