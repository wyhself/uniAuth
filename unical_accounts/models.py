import pycountry

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class User(AbstractUser):
    GENDER= (
                ( 'male', _('Maschio')),
                ( 'female', _('Femmina')),
                ( 'other', _('Altro')),
            )

    first_name = models.CharField(_('Name'), max_length=30,
                                  blank=True, null=True)
    last_name = models.CharField(_('Surname'), max_length=30,
                                 blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    email = models.EmailField('email address', blank=True, null=True)
    taxpayer_id = models.CharField(_('Taxpayer\'s identification number'),
                                      max_length=32,
                                      blank=True, null=True)
    gender    = models.CharField(_('Genere'), choices=GENDER,
                                 max_length=12, blank=True, null=True)
    place_of_birth = models.CharField('Luogo di nascita', max_length=30,
                                      blank=True, null=True,
                                      choices=[(i.name, i.name) for i in pycountry.countries])
    birth_date = models.DateField('Data di nascita',
                                  null=True, blank=True)
    original_uid = models.CharField(_('Username used in connectors auth'),
                                    max_length=254,
                                    blank=True, null=True)
    origin = models.CharField(_('from which conenctor this user come from'),
                              max_length=254,
                              blank=True, null=True)
    
    class Meta:
        ordering = ['username']
        verbose_name_plural = _("Users")

    @property
    def uid(self):
        return self.username.split('@')[0]

    def persistent_id(self, entityid):
        """ returns persistent id related to a recipient (sp) entity id
        """
        pid = PersistentId.objects.filter(user=self,
                                          recipient_id=entityid).last()
        if pid:
            return pid.persistent_id
        
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class PersistentId(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    persistent_id = models.CharField(_('SAML Persistent Stored ID'),
                                 max_length=254,
                                 blank=True, null=True)
    recipient_id = models.CharField(_('SAML ServiceProvider entityID'),
                                 max_length=254,
                                 blank=True, null=True)
    
