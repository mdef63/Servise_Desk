from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.

PRIORITY_CHOICES = (
    (1, _('1. Критический')),
    (2, _('2. Высокий')),
    (3, _('3. Нормальный')),
    (4, _('4. Низкий')),
    (5, _('5. Очень низкий')),
)

STATUS_CHOISES = (
    ('Open', _('Открытый')),
    ('Resolved', _('На рассмотрении')),
    ('Closed', _('Закрытый')),
)


class Ticket(models.Model):
    title = models.CharField(
        max_length=150,
        help_text='Заголовок'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        blank=True,
        null=True
    )

    def function(instance):
        return instance.slug

    def function1(value):
        return value.replace(' ', '-')

    slug = AutoSlugField(
        populate_from=function,
        unique_with=['id', 'created'],
        slugify=function1,
        allow_unicode=True
    )

    description = models.CharField(
        max_length=15000,
        help_text='Описание проблемы'
    )

    resolution = models.CharField(
        max_length=15000,
        help_text='Решение проблемы'
    )

    priority = models.IntegerField(_('Priority'), choices=PRIORITY_CHOICES,
                                   default=3,
                                   blank=True,
                                   help_text=_('Приоритет'),
    )

    email_address = models.EmailField(
        blank=True,
        null=True,
        help_text='Email'
    )

    status = models.CharField(_('Status'), choices=STATUS_CHOISES,
                              default='Open',
                              blank=True,
                              max_length=20,
                              help_text='Статус'
    )

    def get_absolute_url(self):
        return reverse('ticket_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ticket_update_url', kwargs={'slug': self.slug})

    def get_resolute_url(self):
        return reverse('ticket_resolute_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('ticket_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['-created']


class UpdatedTicket(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name=_('UpdatedTicket')
    )

    date = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    Resolve = models.CharField(
        max_length=1500
    )

    class Meta:
        ordering = ['date']
