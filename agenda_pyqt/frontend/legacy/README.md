# Código Legacy - No en Uso

Este directorio contiene código antiguo que ya no está en uso en la aplicación. Se mantiene temporalmente como referencia durante la migración a la nueva estructura.

## Estructura

- `layouts/`: Antiguos formularios y layouts de la interfaz (reemplazados por `frontend/views/components/dialogs/`)
- `ui/`: Código UI antiguo (reemplazado por la nueva estructura en `frontend/views/components/`)
- `ventanas/`: Ventanas antiguas (reemplazadas por los nuevos componentes)

## Nueva Estructura (En Uso)

El código actual en uso se encuentra en:
```
frontend/
└── views/
    └── components/
        ├── dialogs/    (diálogos modales: clientes, corredores, movimientos)
        └── tabs/       (pestañas de la interfaz principal)
```

## Nota Importante

Este código se mantiene temporalmente solo como referencia y será eliminado en el futuro. 
NO usar este código para nuevos desarrollos. Usar siempre los componentes de la nueva estructura.
