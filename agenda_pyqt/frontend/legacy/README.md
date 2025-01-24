# Legacy Code Directory

Este directorio contiene código legacy que ha sido reemplazado por versiones más modernas y mantenibles.

## Archivos

### Ventana Principal
- `main_window.py.legacy`: Versión anterior de la ventana principal que contenía toda la lógica en un solo archivo. 
  - Reemplazado por: `frontend/main_window.py` y los componentes modulares en `frontend/views/components/`
  - Fecha de deprecación: 19/01/2025
  - Razón: Mejora de la arquitectura para hacerla más modular y mantenible

### Ventanas de Backup
- `ventana_inicio_sesion.py`: Versión anterior de la ventana de inicio de sesión
- `ventana_primera_ejecucion.py`: Versión anterior de la ventana de primera ejecución
- `ventana_principal.py`: Versión anterior de la ventana principal
- `__init__.py`: Archivo de inicialización del módulo de ventanas
  - Reemplazados por: Las nuevas implementaciones en `frontend/views/`
  - Fecha de deprecación: 20/01/2025
  - Razón: Reorganización de la arquitectura para mejor modularidad y mantenibilidad

Este código se mantiene como referencia histórica y para consultar funcionalidades que puedan no haber sido migradas completamente.
