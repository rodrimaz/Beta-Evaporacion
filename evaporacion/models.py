from django.db import models
from django.urls import reverse

class Parcelascsv(models.Model):
    parcela = models.AutoField(primary_key=True)
    responsable = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=255)
    descripcion_parcela = models.CharField(db_column='Descripcion Parcela', max_length=255)
    sector = models.CharField(max_length=255)
    auditores = models.CharField(max_length=255)

    class Meta:
        db_table = 'parcelascsv'
        managed = False

    def __str__(self):
        return str(self.parcela)

# Modelo TABLA EVAPORACION (incluye evaporacion y evaporacion par)
class Evaporacion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    operario = models.CharField(max_length=255, verbose_name='Operario')
    totalizador_condensado = models.FloatField(verbose_name='Totalizador condensado (m3)', null=True, default=None, blank=True)
    OT_BO2101 = models.FloatField(verbose_name='OT BO2101 (%)', null=True, default=None, blank=True)
    presion_salida_IC2102 = models.FloatField(verbose_name='Presión Egreso IC2102', null=True, default=None, blank=True)
    presion_BO2101 = models.FloatField(verbose_name='Presion BO2101', null=True, default=None, blank=True)
    presion_ingreso_IC2101 = models.FloatField(verbose_name='Presion Ingreso IC2101', null=True, default=None, blank=True)
    presion_egreso_IC2101_ingreso_IC2103 = models.FloatField(verbose_name='Presion Egreso IC2101/Ingreso IC2103', null=True, default=None, blank=True)
    presion_egreso_IC2103 = models.FloatField(verbose_name='Presion Egreso IC2103', null=True, default=None, blank=True)
    temp_ingreso_agua_IC701 = models.FloatField(verbose_name='Temp Ingreso Agua IC701 (°C)', null=True, default=None, blank=True)
    temp_salida_agua_IC701 = models.FloatField(verbose_name='Temp Salida Agua IC701 (°C)', null=True, default=None, blank=True)
    presion_ingreso_agua_IC701 = models.FloatField(verbose_name='Presion Ingreso Agua IC701 (bar)', null=True, default=None, blank=True)
    presion_salida_agua_IC701 = models.FloatField(verbose_name='Presion Salida Agua IC701 (bar)', null=True, default=None, blank=True)
    presion_salida_vahos_IC701 = models.FloatField(verbose_name='Presion Salida Vahos IC701 (bar)', null=True, default=None, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, default=None, blank=True)

    class Meta:
        db_table = 'evaporacion'
        verbose_name = 'Evaporacion'
        verbose_name_plural = 'Evaporaciones'
        ordering = ['-operario', '-fecha']
    
    def get_absolute_url(self):
        return reverse('evaporaciones', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.operario + " - " + str(self.fecha)