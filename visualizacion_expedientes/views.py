# visualizacion_expedientes/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Cliente
from gestdocu.models import Caso, Expediente, Documento  # ← Importar desde pages

@login_required
def expedientes_jerarquicos(request):
    """
    Vista para mostrar expedientes en estructura jerárquica:
    Cliente → Caso → Expediente → Documentos
    """
    
    # Obtener todos los clientes con sus casos y expedientes relacionados
    clientes_con_casos = []
    
    for cliente in Cliente.objects.all():
        casos_del_cliente = []
        
        # Obtener todos los casos del cliente
        for caso in cliente.casos.all():
            expedientes_del_caso = []
            
            # Obtener todos los expedientes del caso
            for expediente in caso.expedientes.all():
                documentos_del_expediente = expediente.documentos.all()
                
                expedientes_del_caso.append({
                    'expediente': expediente,
                    'documentos': documentos_del_expediente,
                    'total_documentos': documentos_del_expediente.count()
                })
            
            casos_del_cliente.append({
                'caso': caso,
                'expedientes': expedientes_del_caso,
                'total_expedientes': len(expedientes_del_caso),
                'total_documentos': sum(exp['total_documentos'] for exp in expedientes_del_caso)
            })
        
        if casos_del_cliente:  # Solo incluir clientes que tienen casos
            clientes_con_casos.append({
                'cliente': cliente,
                'casos': casos_del_cliente,
                'total_casos': len(casos_del_cliente)
            })
    
    context = {
        'clientes_con_casos': clientes_con_casos,
        'total_clientes': len(clientes_con_casos)
    }
    
    return render(request, 'visualizacion_expedientes/expedientes_jerarquicos.html', context)