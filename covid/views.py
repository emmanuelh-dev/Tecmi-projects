import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import RegistroCovid
from .models import RegistroCovid
from .models import RegistroCovid
from django.core.paginator import Paginator
from django.db.models import Count

def home(request):
    return render(request, 'covid_home.html')


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = pd.read_csv(file)

            for _, row in data.iterrows():
                RegistroCovid.objects.create(
                    fecha_actualizacion=row['FECHA_ACTUALIZACION'],
                    id_registro=row['ID_REGISTRO'],
                    origen=row['ORIGEN'],
                    sector=row['SECTOR'],
                    entidad_um=row['ENTIDAD_UM'],
                    sexo=row['SEXO'],
                    entidad_nac=row['ENTIDAD_NAC'],
                    entidad_res=row['ENTIDAD_RES'],
                    municipio_res=row['MUNICIPIO_RES'],
                    tipo_paciente=row['TIPO_PACIENTE'],
                    fecha_ingreso=row['FECHA_INGRESO'],
                    fecha_sintomas=row['FECHA_SINTOMAS'],
                    fecha_def=row['FECHA_DEF'],
                    intubado=row['INTUBADO'],
                    neumonia=row['NEUMONIA'],
                    edad=row['EDAD'],
                    nacionalidad=row['NACIONALIDAD'],
                    embarazo=row['EMBARAZO'],
                    habla_lengua_indig=row['HABLA_LENGUA_INDIG'],
                    indigena=row['INDIGENA'],
                    diabetes=row['DIABETES'],
                    epoc=row['EPOC'],
                    asma=row['ASMA'],
                    inmu_supr=row['INMUSUPR'],
                    hipertension=row['HIPERTENSION'],
                    otra_com=row['OTRA_COM'],
                    cardiovascular=row['CARDIOVASCULAR'],
                    obesidad=row['OBESIDAD'],
                    renal_cronica=row['RENAL_CRONICA'],
                    tabaquismo=row['TABAQUISMO'],
                    otro_caso=row['OTRO_CASO'],
                    toma_muestra_lab=row['TOMA_MUESTRA_LAB'],
                    resultado_pcr=row['RESULTADO_PCR'],
                    resultado_pcr_coinfeccion=row['RESULTADO_PCR_COINFECCION'],
                    toma_muestra_antigeno=row['TOMA_MUESTRA_ANTIGENO'],
                    resultado_antigeno=row['RESULTADO_ANTIGENO'],
                    clasificacion_final_covid=row['CLASIFICACION_FINAL_COVID'],
                    clasificacion_final_flu=row['CLASIFICACION_FINAL_FLU'],
                    migrante=row['MIGRANTE'],
                    pais_nacionalidad=row['PAIS_NACIONALIDAD'],
                    pais_origen=row['PAIS_ORIGEN'],
                    uci=row['UCI']
                )
            return redirect('success_page')
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})

def listar_registros(request):
    registros_list = RegistroCovid.objects.all()
    paginator = Paginator(registros_list, 50)

    page_number = request.GET.get('page')
    registros = paginator.get_page(page_number)

    sectores_data = RegistroCovid.objects.values('sector').annotate(cantidad=Count('sector'))

    sectores = [sector['sector'] for sector in sectores_data]
    cantidades = [sector['cantidad'] for sector in sectores_data]

    return render(request, 'listar_registros.html', {
        'registros': registros,
        'sectores': sectores,
        'cantidades': cantidades
    })