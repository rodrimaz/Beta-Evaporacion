from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
import pytz

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

# Modelo TABLA DE FALLAS (General para todos los reportes)
class Falla(models.Model):
    id_falla = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    operario = models.CharField(max_length=255)
    area = models.CharField(max_length=255, null=True, blank=True)  
    parcela_sector = models.CharField(max_length=255)
    falla = models.TextField()
    posible_causa = models.TextField()
    posible_solucion = models.TextField()
    estado = models.CharField(max_length=255, null=True, blank=True)
    fecha_conclusion = models.DateTimeField(null=True, blank=True)
    conclusion = models.TextField(null=True, blank=True)
    operario_conclusion = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='fallas/', null=True, blank=True)

# Modelo TABLA EVAPORACION (incluye evaporacion y evaporacion par)
class Evaporacion(models.Model):
    Id_evaporacion = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    operario = models.CharField(max_length=255)
    caudal_vl = models.FloatField()
    PT01_PT02 = models.FloatField()
    PT03 = models.FloatField()
    PT04 = models.FloatField()
    PT05 = models.FloatField()
    ST_EFECTO_2_SALIDA = models.FloatField()
    densidad = models.FloatField()
    observaciones = models.TextField()
    OT_EYECTOR_1 = models.FloatField()
    OT_EYECTOR_2 = models.FloatField()
    potencia_sepevap = models.FloatField()
    totalizador_condensado = models.FloatField()
    filetes_FERM = models.FloatField()
    OT_vva_traspaso_ef1_a_ef3 = models.FloatField()
    viscosidad = models.FloatField()
    temperatura = models.FloatField()
    densidad_LAB = models.FloatField()
    nivel_tk_condensado = models.FloatField()
    OT_BO2101 = models.FloatField()
    presion_BO2101 = models.FloatField()
    presion_ingreso_IC2101 = models.FloatField()
    presion_egreso_IC2101_ingreso_IC2103 = models.FloatField()
    presion_egreso_IC2103 = models.FloatField()
    presion_ingreso_IC2104 = models.FloatField()
    presion_egreso_IC2104 = models.FloatField()
    T_ingreso_agua_IC701 = models.FloatField()
    T_salida_agua_IC701 = models.FloatField()
    presion_ingreso_agua_IC701 = models.FloatField()
    presion_salida_agua_IC701 = models.FloatField()
    presion_salida_vahos_IC701 = models.FloatField()

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.asunto