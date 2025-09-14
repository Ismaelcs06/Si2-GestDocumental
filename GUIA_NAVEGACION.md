# 🧭 **GUÍA COMPLETA DE NAVEGACIÓN - Sistema de Gestión de Clientes**

## 🚀 **Cómo Acceder y Navegar por el Sistema**

### **1. Iniciar el Servidor**
```bash
cd /c/dev/Si2-GestDocumental
python manage.py runserver
```

### **2. URLs Principales para Testing**

#### **🏠 Página Principal**
- **URL:** `http://127.0.0.1:8000/`
- **Descripción:** Página de inicio del sistema

#### **🔐 Login de Administrador**
- **URL:** `http://127.0.0.1:8000/accounts/login/`
- **Credenciales:** 
  - Usuario: `admin`
  - Contraseña: `admin` (o la que configuraste)

#### **📊 Dashboard Principal**
- **URL:** `http://127.0.0.1:8000/dashboard/`
- **Descripción:** Panel de control con accesos directos
- **Requisito:** Estar logueado

---

## 👥 **SISTEMA DE CLIENTES - URLs Principales**

### **📋 Lista de Clientes**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/`
- **Funcionalidades:**
  - ✅ Ver todos los clientes registrados
  - ✅ Búsqueda por nombre, CI, email, NIT
  - ✅ Filtros por tipo (Persona/Empresa)
  - ✅ Filtros por clasificación procesal
  - ✅ Paginación (10 clientes por página)
  - ✅ Enlaces de acciones (Ver, Editar, Eliminar)

### **➕ Registrar Cliente - Persona Natural**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=PERSONA`
- **Campos a probar:**
  - Nombres (obligatorio)
  - Apellidos (paterno obligatorio, materno opcional)
  - CI (formato boliviano: 1234567 o 1234567-1A)
  - Email (único en el sistema)
  - Celular (formato boliviano: 71234567)
  - Dirección (opcional)
  - Fecha de nacimiento (optional)
  - Clasificación procesal (Demandante/Demandado/Otro)
  - Historial (opcional)

### **🏢 Registrar Cliente - Empresa**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=EMPRESA`
- **Campos adicionales de empresa:**
  - Nombre de empresa (obligatorio)
  - NIT (formato boliviano: 1234567890)
  - Todos los campos de persona (para representante legal)

### **👁️ Ver Detalle de Cliente**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/1/`
- **Funcionalidades:**
  - ✅ Ver toda la información del cliente
  - ✅ Diferente vista para personas vs empresas
  - ✅ Enlaces de acciones (Editar, Eliminar)
  - ✅ Panel lateral con opciones

### **✏️ Editar Cliente**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/1/editar/`
- **Funcionalidades:**
  - ✅ Formularios separados (datos personales + datos de cliente)
  - ✅ Campos dinámicos según tipo de cliente
  - ✅ Validaciones en tiempo real

### **🗑️ Eliminar Cliente**
- **URL:** `http://127.0.0.1:8000/accounts/clientes/1/eliminar/`
- **Funcionalidades:**
  - ✅ Confirmación de eliminación
  - ✅ Vista previa de datos a eliminar
  - ✅ Advertencia sobre eliminación en cascada

---

## 🔧 **Panel de Administración Django**

### **Admin Principal**
- **URL:** `http://127.0.0.1:8000/admin/`
- **Credenciales:** Usuario admin

### **Gestión de Clientes en Admin**
- **URL:** `http://127.0.0.1:8000/admin/accounts/cliente/`
- **Funcionalidades:**
  - ✅ Lista con filtros avanzados
  - ✅ Búsqueda por múltiples campos
  - ✅ Formulario organizado en secciones

### **Gestión de Usuarios en Admin**
- **URL:** `http://127.0.0.1:8000/admin/accounts/user/`
- **Funcionalidades:**
  - ✅ Gestión completa de usuarios
  - ✅ Filtros por tipo de usuario
  - ✅ Campos personalizados del modelo User

---

## 🧪 **CASOS DE PRUEBA - STEP BY STEP**

### **✅ TEST 1: Registro de Persona Natural**
1. Ir a: `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=PERSONA`
2. Llenar campos:
   - Nombres: `Juan Carlos`
   - Apellido Paterno: `Pérez`
   - Apellido Materno: `Mamani`
   - CI: `12345678` (probar validación)
   - Email: `juan.perez@test.com`
   - Celular: `71234567`
   - Clasificación: `DEMANDANTE`
3. **Resultado esperado:** Cliente creado, redirección a detalle

### **✅ TEST 2: Registro de Empresa**
1. Ir a: `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=EMPRESA`
2. Llenar datos de empresa:
   - Nombre Empresa: `Consultora Legal S.R.L.`
   - NIT: `1029384756`
3. Llenar datos del representante:
   - Nombres: `Patricia`
   - Apellido Paterno: `Vásquez`
   - CI: `87654321`
   - Email: `patricia.vasquez@consultora.bo`
   - Clasificación: `OTRO`
4. **Resultado esperado:** Empresa creada con representante

### **✅ TEST 3: Búsqueda y Filtros**
1. Ir a: `http://127.0.0.1:8000/accounts/clientes/`
2. Probar búsquedas:
   - Buscar: `María` (debería encontrar María Elena González)
   - Buscar: `TechSolutions` (empresa)
   - Buscar: `1234567` (por CI)
   - Buscar: `constructora` (por nombre empresa)
3. Probar filtros:
   - Filtro Tipo: `EMPRESA`
   - Filtro Clasificación: `DEMANDANTE`
4. **Resultado esperado:** Resultados filtrados correctamente

### **✅ TEST 4: Edición de Cliente**
1. Ir a detalle de cualquier cliente
2. Clic en "Editar"
3. Modificar datos:
   - Cambiar teléfono
   - Agregar historial
   - Cambiar clasificación procesal
4. Guardar cambios
5. **Resultado esperado:** Datos actualizados correctamente

### **✅ TEST 5: Validaciones**
1. Intentar crear cliente con CI duplicado
2. Intentar crear empresa sin NIT
3. Probar formato incorrecto de CI
4. Probar NIT con formato incorrecto
5. **Resultado esperado:** Errores de validación mostrados

### **✅ TEST 6: Eliminación**
1. Crear un cliente de prueba
2. Ir a su detalle
3. Clic en "Eliminar"
4. Confirmar eliminación
5. **Resultado esperado:** Cliente eliminado, redirección a lista

---

## 📊 **Datos de Prueba Disponibles**

Ya tienes **5 clientes de prueba** creados:

### **👤 Personas Naturales:**
1. **María Elena González López**
   - CI: 1234567
   - Clasificación: Demandante
   - Email: maria.gonzalez@email.com

2. **Carlos Mendoza Ríos**
   - CI: 7654321-1A
   - Clasificación: Demandado
   - Email: carlos.mendoza@email.com

3. **Laura Jiménez Morales**
   - CI: 9999999
   - Clasificación: Otro
   - Email: laura.jimenez@email.com

### **🏢 Empresas:**
1. **TechSolutions Ltda.**
   - NIT: 1234567890123
   - Representante: Ana Vargas Sánchez (CI: 5555555)
   - Clasificación: Demandante

2. **Constructora Andina S.R.L.**
   - NIT: 9876543210987
   - Representante: Roberto Flores Castro (CI: 8888888)
   - Clasificación: Demandado

---

## 🎯 **Funcionalidades Implementadas para Probar**

### **✅ CRUD Completo**
- [x] Crear clientes (naturales y jurídicos)
- [x] Leer/Ver clientes (lista y detalle)
- [x] Actualizar clientes
- [x] Eliminar clientes

### **✅ Validaciones**
- [x] CI boliviano (formato correcto)
- [x] NIT boliviano (7-15 dígitos)
- [x] Email único
- [x] Campos obligatorios
- [x] Validaciones de negocio (empresa debe tener NIT)

### **✅ Búsqueda y Filtros**
- [x] Búsqueda por texto libre
- [x] Filtro por tipo de cliente
- [x] Filtro por clasificación procesal
- [x] Paginación

### **✅ Interfaz de Usuario**
- [x] Templates responsivos con Bootstrap
- [x] Formularios dinámicos
- [x] Mensajes de confirmación
- [x] Navegación intuitiva

### **✅ Clasificación Procesal**
- [x] Demandante
- [x] Demandado
- [x] Otro

---

## 🚨 **Troubleshooting**

### **Problema: Error 404**
- **Solución:** Verificar que el servidor esté corriendo en `http://127.0.0.1:8000/`

### **Problema: No puedo acceder**
- **Solución:** Iniciar sesión en `/accounts/login/` con usuario `admin`

### **Problema: Datos no se muestran**
- **Solución:** Ejecutar `python create_sample_data.py` para crear datos de prueba

### **Problema: Error en formularios**
- **Solución:** Verificar que todos los campos obligatorios estén llenos y con formato correcto

---

## 🎉 **¡Listo para Probar!**

Tu sistema de gestión de clientes está **100% funcional** y listo para testing. 

**🔗 Enlaces Directos de Acceso Rápido:**
- 📋 Lista: `http://127.0.0.1:8000/accounts/clientes/`
- ➕ Nueva Persona: `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=PERSONA`
- 🏢 Nueva Empresa: `http://127.0.0.1:8000/accounts/clientes/nuevo/?tipo=EMPRESA`
- 🔧 Admin: `http://127.0.0.1:8000/admin/accounts/cliente/`

¡Disfruta probando todas las funcionalidades! 🎯