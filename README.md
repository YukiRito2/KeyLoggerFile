# Keylogger con Webhook de Discord

Este proyecto es un keylogger escrito en Python que registra las pulsaciones de teclas y las envía a un webhook de Discord en intervalos definidos. El keylogger utiliza las librerías `dhooks` para enviar los logs a Discord y `pynput` para escuchar las pulsaciones de teclas.

## Características

- Captura de pulsaciones de teclas, incluidas teclas especiales como espacio, enter, tab, y combinaciones de teclas.
- Los registros se envían automáticamente a un webhook de Discord cada cierto intervalo de tiempo.
- Sistema de logging para guardar las pulsaciones de teclas en un archivo `keylog.txt`.
- Validación automática de la URL del webhook antes de iniciar el envío de datos.
- Mecanismo para omitir ciertas teclas (por ejemplo, Shift).
- Posibilidad de modificar el intervalo de tiempo entre reportes.

## Configuración de la URL del Webhook

La URL del webhook de Discord se puede establecer mediante una variable de entorno llamada `DISCORD_WEBHOOK_URL`. Si no configuras esta variable de entorno, el script usará una URL predeterminada que está en el código.

### Pasos para configurar la URL del Webhook:

1. Abre tu terminal y ejecuta el siguiente comando para configurar la URL del webhook como una variable de entorno:

   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/tu_webhook"
