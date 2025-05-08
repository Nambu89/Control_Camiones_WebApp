# Guía de Usuario

## Introducción

Bienvenido a la Guía de Usuario del Sistema de Control Logístico de Camiones. Este documento está diseñado para proporcionar instrucciones claras sobre cómo utilizar todas las funcionalidades del sistema, desde el registro de entradas y salidas hasta la generación de reportes y exportación de datos.

## Acceso al Sistema

El sistema es una aplicación web que puede accederse a través de cualquier navegador moderno (Chrome, Firefox, Edge, Safari). Para acceder al sistema:

1. Abra su navegador web
2. Introduzca la dirección URL proporcionada por su administrador
3. La página principal del sistema se cargará automáticamente

## Navegación Principal

La barra de navegación en la parte superior de la aplicación permite acceder a todas las funcionalidades principales:

- **Inicio**: Página principal para registrar entradas y salidas
- **Buscar**: Permite buscar registros históricos
- **Lista**: Muestra todos los camiones actualmente dentro de las instalaciones
- **Reporte**: Genera informes por rango de fechas

## Registro de Entradas y Salidas

### Registrar la Entrada de un Camión

1. Acceda a la página principal (Inicio)
2. Complete el formulario con la siguiente información:
   - **Matrícula de la tractora**: Obligatorio
   - **Matrícula del remolque**: Opcional
   - **Empresa del transportista**: Obligatorio
   - **Número de envío**: Opcional
   - **Almacén**: Seleccione S1 o S6 (Obligatorio)
   - **Tipo**: Seleccione Carga o Descarga (Obligatorio)
3. Haga clic en el botón "Registrar entrada"
4. El sistema registrará la entrada con la fecha y hora actuales
5. Se mostrará la información del registro creado en la parte inferior

### Registrar la Salida de un Camión

#### Desde la Página Principal

1. Acceda a la página principal (Inicio)
2. Introduzca la matrícula de la tractora del camión que está saliendo
3. Si el camión está registrado como "dentro", el sistema mostrará su información y cambiará el botón a "Registrar salida"
4. Haga clic en "Registrar salida"
5. El sistema registrará la salida con la fecha y hora actuales

#### Desde la Lista de Camiones

1. Acceda a la página "Lista" desde la barra de navegación
2. Localice el camión que está saliendo
3. Haga clic en el botón "Registrar salida" correspondiente a ese camión
4. El sistema registrará la salida y actualizará la lista

## Gestión de Camiones Activos

### Ver Camiones Dentro de las Instalaciones

1. Acceda a la página "Lista" desde la barra de navegación
2. Se mostrará una tabla con todos los camiones que están actualmente dentro (sin fecha de salida)
3. Puede filtrar la lista por almacén (S1 o S6) utilizando el selector y el botón "Filtrar"

### Editar Información de un Camión

1. En la página "Lista", localice el camión que desea editar
2. Haga clic en el botón "Editar" correspondiente a ese camión
3. Se abrirá un formulario con la información actual del camión
4. Modifique los campos según sea necesario
5. Haga clic en "Guardar" para aplicar los cambios

### Eliminar un Registro

1. En la página "Lista", localice el camión cuyo registro desea eliminar
2. Haga clic en el botón "Borrar" correspondiente a ese camión
3. El registro se eliminará permanentemente (no hay confirmación adicional)

### Duplicar un Registro

1. En la página "Lista", localice el camión cuyo registro desea duplicar
2. Haga clic en el botón "+" correspondiente a ese camión
3. Se creará un nuevo registro con la misma información

## Búsqueda de Registros

### Buscar Camiones por Criterios

1. Acceda a la página "Buscar" desde la barra de navegación
2. Introduzca un término de búsqueda en el campo (puede ser matrícula, empresa o número de envío)
3. Haga clic en "Buscar"
4. Se mostrarán todos los registros que coincidan con el criterio de búsqueda

## Generación de Reportes

### Crear un Reporte por Rango de Fechas

1. Acceda a la página "Reporte" desde la barra de navegación
2. Seleccione la fecha de inicio utilizando el selector de fechas (formato DD-MM-YYYY)
3. Seleccione la fecha de fin utilizando el selector de fechas (formato DD-MM-YYYY)
4. Haga clic en "Filtrar"
5. Se mostrarán todos los registros cuya fecha de entrada esté dentro del rango seleccionado

### Exportar Datos a CSV

1. Genere un reporte como se describe en el punto anterior
2. Una vez que se muestren los resultados, haga clic en el botón "Exportar a CSV"
3. El navegador descargará un archivo CSV con los datos del reporte
4. Este archivo puede abrirse con Excel u otras aplicaciones de hoja de cálculo

## Consejos y Trucos

### Búsqueda Rápida

- Para encontrar rápidamente un camión específico, introduzca su matrícula en la página principal
- Si el camión está dentro, se mostrará su información y podrá registrar su salida
- Si no está dentro o ya ha salido, podrá registrar una nueva entrada

### Filtrado Eficiente

- Utilice el filtro por almacén en la página "Lista" para ver solo los camiones en un almacén específico
- Esto es especialmente útil cuando hay muchos camiones dentro de las instalaciones

### Duplicación para Operaciones Repetitivas

- Utilice el botón "+" para duplicar registros de camiones que realizan operaciones similares
- Esto ahorra tiempo al no tener que introducir toda la información nuevamente

## Solución de Problemas Comunes

### No Puedo Registrar la Salida de un Camión

- Verifique que ha introducido correctamente la matrícula de la tractora
- Compruebe en la página "Lista" si el camión aparece como dentro de las instalaciones
- Si no aparece, es posible que ya se haya registrado su salida o que no se haya registrado su entrada

### Los Datos No Aparecen en el Reporte

- Asegúrese de que ha seleccionado correctamente el rango de fechas
- Verifique que el formato de fecha sea DD-MM-YYYY
- Compruebe que existen registros en el rango de fechas seleccionado

### No Puedo Encontrar un Registro en la Búsqueda

- Intente con términos de búsqueda más cortos o parciales
- Pruebe a buscar por diferentes criterios (matrícula, empresa, número de envío)
- Verifique que el registro existe y no ha sido eliminado
