#!/usr/bin/env python
"""
Script para crear datos de prueba para el sistema de clientes
"""
import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civilApp.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User, Cliente

def create_sample_data():
    """Crear datos de prueba"""
    print("Creando datos de prueba...")
    
    # Cliente Persona Natural 1 - Demandante
    try:
        user1 = User.objects.create_user(
            username='1234567',
            nombres='María Elena',
            apellido_paterno='González',
            apellido_materno='López',
            ci='1234567',
            email='maria.gonzalez@email.com',
            celular='71234567',
            direccion='Av. Ballivián #123, Sopocachi',
            fecha_nacimiento=date(1985, 3, 15),
            password='temp123456'  # Contraseña temporal
        )
        
        cliente1 = Cliente.objects.create(
            user=user1,
            tipo_cliente='PERSONA',
            clasificacion_procesal='DEMANDANTE',
            historial='Cliente frecuente del bufete. Casos de derecho familiar.'
        )
        print(f"✅ Cliente creado: {cliente1.user.nombre_completo} (Persona - Demandante)")
        
    except Exception as e:
        print(f"❌ Error creando cliente 1: {e}")
    
    # Cliente Persona Natural 2 - Demandado
    try:
        user2 = User.objects.create_user(
            username='7654321',
            nombres='Carlos',
            apellido_paterno='Mendoza',
            apellido_materno='Ríos',
            ci='7654321-1A',
            email='carlos.mendoza@email.com',
            celular='67890123',
            direccion='Calle Murillo #456, Centro',
            fecha_nacimiento=date(1978, 8, 22),
            password='temp123456'
        )
        
        cliente2 = Cliente.objects.create(
            user=user2,
            tipo_cliente='PERSONA',
            clasificacion_procesal='DEMANDADO',
            historial='Caso de responsabilidad civil por accidente de tránsito.'
        )
        print(f"✅ Cliente creado: {cliente2.user.nombre_completo} (Persona - Demandado)")
        
    except Exception as e:
        print(f"❌ Error creando cliente 2: {e}")
    
    # Cliente Empresa 1 - Demandante
    try:
        user3 = User.objects.create_user(
            username='5555555',
            nombres='Ana',
            apellido_paterno='Vargas',
            apellido_materno='Sánchez',
            ci='5555555',
            email='legal@techsolutions.bo',
            celular='75555555',
            direccion='Zona San Miguel, Edificio Torre Empresarial',
            fecha_nacimiento=date(1982, 12, 5),
            password='temp123456'
        )
        
        cliente3 = Cliente.objects.create(
            user=user3,
            tipo_cliente='EMPRESA',
            nombre_empresa='TechSolutions Ltda.',
            nit='1234567890123',
            clasificacion_procesal='DEMANDANTE',
            historial='Empresa de tecnología. Casos de propiedad intelectual y contratos comerciales.'
        )
        print(f"✅ Cliente creado: {cliente3.nombre_empresa} (Empresa - Demandante)")
        
    except Exception as e:
        print(f"❌ Error creando cliente empresa 1: {e}")
    
    # Cliente Empresa 2 - Demandado
    try:
        user4 = User.objects.create_user(
            username='8888888',
            nombres='Roberto',
            apellido_paterno='Flores',
            apellido_materno='Castro',
            ci='8888888',
            email='gerencia@constructora-andina.bo',
            celular='68888888',
            direccion='Av. 6 de Agosto #789, San Jorge',
            fecha_nacimiento=date(1975, 6, 10),
            password='temp123456'
        )
        
        cliente4 = Cliente.objects.create(
            user=user4,
            tipo_cliente='EMPRESA',
            nombre_empresa='Constructora Andina S.R.L.',
            nit='9876543210987',
            clasificacion_procesal='DEMANDADO',
            historial='Constructora con 20 años de experiencia. Demanda por incumplimiento contractual.'
        )
        print(f"✅ Cliente creado: {cliente4.nombre_empresa} (Empresa - Demandado)")
        
    except Exception as e:
        print(f"❌ Error creando cliente empresa 2: {e}")
    
    # Cliente con clasificación "OTRO"
    try:
        user5 = User.objects.create_user(
            username='9999999',
            nombres='Laura',
            apellido_paterno='Jiménez',
            apellido_materno='Morales',
            ci='9999999',
            email='laura.jimenez@email.com',
            celular='69999999',
            direccion='Zona Miraflores, Calle 21 #234',
            fecha_nacimiento=date(1990, 4, 18),
            password='temp123456'
        )
        
        cliente5 = Cliente.objects.create(
            user=user5,
            tipo_cliente='PERSONA',
            clasificacion_procesal='OTRO',
            historial='Consultoría legal preventiva. Asesoramiento en temas de herencias.'
        )
        print(f"✅ Cliente creado: {cliente5.user.nombre_completo} (Persona - Otro)")
        
    except Exception as e:
        print(f"❌ Error creando cliente 5: {e}")
    
    print("\n" + "="*50)
    print("RESUMEN DE CLIENTES CREADOS:")
    print("="*50)
    
    # Mostrar resumen
    clientes = Cliente.objects.all()
    for cliente in clientes:
        tipo_icon = "🏢" if cliente.tipo_cliente == 'EMPRESA' else "👤"
        clasificacion_color = {
            'DEMANDANTE': '🟡',
            'DEMANDADO': '🔴', 
            'OTRO': '⚪'
        }
        
        nombre = cliente.nombre_empresa if cliente.tipo_cliente == 'EMPRESA' else cliente.user.nombre_completo
        print(f"{tipo_icon} {nombre}")
        print(f"   {clasificacion_color.get(cliente.clasificacion_procesal, '⚪')} {cliente.get_clasificacion_procesal_display()}")
        print(f"   📧 {cliente.user.email}")
        print(f"   📱 {cliente.user.celular}")
        print()

if __name__ == '__main__':
    create_sample_data()
    print("✅ Datos de prueba creados exitosamente!")
    print("\nPara acceder al sistema:")
    print("- Usuario admin: admin")
    print("- Los clientes tienen usuarios con username=CI y password=temp123456")
    print("- Navega a http://127.0.0.1:8000/accounts/clientes/ para ver la lista")