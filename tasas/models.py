from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy

from tasasrest import settings
from .provincias import PROVINCIAS as provincias

import re

class Universidad(models.Model):

    def __init__(self, *args, **kwargs):
        self.get_siglas_no_centro = self._get_siglas_no_centro
        super(Universidad, self).__init__(*args, **kwargs)

    TIPO_UNIVERSIDAD_CHOICES = ((0, 'Pública'), (1, 'Privada'))

    siglas = models.CharField(max_length=20, unique=True, null=False, blank=False,
                              help_text=ugettext_lazy("Siglas de la universidad"))
    nombre = models.CharField(max_length=200, null=False, blank=False,
                              help_text=ugettext_lazy("Nombre de la universidad"))
    tipo = models.IntegerField(choices=TIPO_UNIVERSIDAD_CHOICES, null=False, blank=False,
                               help_text=ugettext_lazy("Tipo de centro (público/privado)"))
    centro = models.CharField(max_length=200, null=True, blank=True, help_text=ugettext_lazy("Nombre del centro"))
    provincia = models.CharField(max_length=50, choices=provincias, blank=False, null=False,
                                 help_text=ugettext_lazy("Provincia"))
    logo = models.ImageField(upload_to=settings.ESCUDOS_PATH, null=True, blank=True,
                             help_text=ugettext_lazy("Escudo de la universidad"))

    campus = models.CharField(max_length=200, null=True, blank=True,
                              help_text=ugettext_lazy("Nombre del campus")) # TODO: Hacer obligatorio?
    url = models.URLField(max_length=300, null=True, blank=True,
                          help_text=ugettext_lazy("URL del centro"))

    def _get_siglas_no_centro(self):
        return self.get_siglas_no_centro(self.siglas)

    @staticmethod
    def get_siglas_no_centro(siglas):
        """
        Elimina el sufijo del centro, útil para procesar imágenes
        Returns:

        """
        return re.sub(r'\-.*', '', siglas)

    def get_provincia_unicode(self):
        return dict(provincias).get(self.provincia)

    def __str__(self):
        return self.nombre

class Tasa(models.Model):
    TIPOS_TASA = (
		(0, "Precio por crédito"),
		(1, "Pago único"),
		(2, "Misceláneo"),
	)

    TIPOS_TITULACION = (
		(0, "Grado"),
		(0, "Máster"),
	)

    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='tasas',
                                    related_query_name='tasa',
                                    help_text=ugettext_lazy("Universidad asociada a esta tasa"))

    tipo = models.IntegerField(choices=TIPOS_TASA, help_text=ugettext_lazy("Tipo de tasa"))
    tipo_titulacion = models.IntegerField(choices=TIPOS_TITULACION,
                                          help_text=ugettext_lazy("Tipo de titulación (grado/máster)"))

    # El curso se representa con el año en el que da comienzo
    curso = models.IntegerField(validators=RegexValidator(regex=r'^\d{4}$'),
                                help_text=ugettext_lazy("Curso académico en el que esta tasa se aplica"))
    url = models.URLField(blank=True, help_text=ugettext_lazy("URL del documento oficial"))

    tasa_global = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Tasa global"))
    descripcion = models.TextField(null=True, max_length=500, blank=True,
                                   help_text=ugettext_lazy("Texto informativo sobre la tasa"))
    tasas1 = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Primera convocatoria"))
    tasas2 = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Segunda convocatoria"))
    tasas3 = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Tercera convocatoria"))
    tasas4 = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Cuarta convocatoria"))

    def __unicode__(self):
        return self.universidad + ", " + self.TIPOS[int(self.tipo)][1] + ", " + self.curso
