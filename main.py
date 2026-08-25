import math
import time

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

from jnius import autoclass, PythonJavaClass, java_method

from plyer import vibrator


PythonActivity = autoclass(
    "org.kivy.android.PythonActivity"
)

Context = autoclass(
    "android.content.Context"
)

Sensor = autoclass(
    "android.hardware.Sensor"
)

SensorManager = autoclass(
    "android.hardware.SensorManager"
)


class SensorListener(PythonJavaClass):

    __javainterfaces__ = [
        "android/hardware/SensorEventListener"
    ]

    def __init__(self, app):
        super().__init__()
        self.app = app

    @java_method("(Landroid/hardware/SensorEvent;)V")
    def onSensorChanged(self, event):

        valores = event.values

        x = float(valores[0])
        y = float(valores[1])
        z = float(valores[2])

        intensidad = math.sqrt(
            x*x + y*y + z*z
        )

        Clock.schedule_once(
            lambda dt: self.app.actualizar(
                x,
                y,
                z,
                intensidad
            )
        )

    @java_method("(Landroid/hardware/Sensor;I)V")
    def onAccuracyChanged(
        self,
        sensor,
        accuracy
    ):
        pass


class DetectorApp(App):

    def build(self):

        Window.clearcolor = (
            0.015,
            0.015,
            0.02,
            1
        )

        self.maximo = 0
        self.ultimo_vibrado = 0

        self.root = FloatLayout()

        # =========================
        # TITULO
        # =========================

        titulo = Label(
            text="DETECTOR MAGNÉTICO",
            font_size="24sp",
            bold=True,
            color=(
                0.9,
                0.9,
                0.95,
                1
            ),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.94
            }
        )

        self.root.add_widget(titulo)

        # =========================
        # VALOR
        # =========================

        self.valor = Label(
            text="--",
            font_size="64sp",
            bold=True,
            color=(
                1,
                1,
                1,
                1
            ),
            size_hint=(1, 0.22),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.70
            }
        )

        self.root.add_widget(self.valor)

        # =========================
        # UNIDAD
        # =========================

        unidad = Label(
            text="MICROTESLAS (µT)",
            font_size="16sp",
            color=(
                0.5,
                0.5,
                0.55,
                1
            ),
            size_hint=(1, 0.07),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.58
            }
        )

        self.root.add_widget(unidad)

        # =========================
        # ESTADO
        # =========================

        self.estado = Label(
            text="INICIANDO...",
            font_size="21sp",
            bold=True,
            color=(
                0.3,
                1,
                0.4,
                1
            ),
            size_hint=(1, 0.08),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.50
            }
        )

        self.root.add_widget(self.estado)

        # =========================
        # BARRA
        # =========================

        self.barra = ProgressBar(
            max=300,
            value=0,
            size_hint=(0.80, None),
            height="20dp",
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.42
            }
        )

        self.root.add_widget(self.barra)

        # =========================
        # MAXIMO
        # =========================

        self.max_label = Label(
            text="MÁXIMO: -- µT",
            font_size="18sp",
            color=(
                0.65,
                0.65,
                0.7,
                1
            ),
            size_hint=(1, 0.08),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.34
            }
        )

        self.root.add_widget(self.max_label)

        # =========================
        # EJES
        # =========================

        self.x_label = Label(
            text="X: --",
            font_size="17sp",
            color=(
                0.6,
                0.6,
                0.65,
                1
            ),
            size_hint=(0.33, 0.08),
            pos_hint={
                "x": 0,
                "center_y": 0.24
            }
        )

        self.root.add_widget(self.x_label)

        self.y_label = Label(
            text="Y: --",
            font_size="17sp",
            color=(
                0.6,
                0.6,
                0.65,
                1
            ),
            size_hint=(0.33, 0.08),
            pos_hint={
                "x": 0.33,
                "center_y": 0.24
            }
        )

        self.root.add_widget(self.y_label)

        self.z_label = Label(
            text="Z: --",
            font_size="17sp",
            color=(
                0.6,
                0.6,
                0.65,
                1
            ),
            size_hint=(0.33, 0.08),
            pos_hint={
                "x": 0.66,
                "center_y": 0.24
            }
        )

        self.root.add_widget(self.z_label)

        # =========================
        # RESET
        # =========================

        reset = Button(
            text="REINICIAR MÁXIMO",
            font_size="17sp",
            background_normal="",
            background_color=(
                0.12,
                0.12,
                0.15,
                1
            ),
            color=(
                0.9,
                0.9,
                0.95,
                1
            ),
            size_hint=(0.65, 0.10),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.10
            }
        )

        reset.bind(
            on_release=self.reset_maximo
        )

        self.root.add_widget(reset)

        Clock.schedule_once(
            self.iniciar_sensor,
            0.5
        )

        return self.root

    # ==================================
    # SENSOR
    # ==================================

    def iniciar_sensor(self, dt):

        try:

            actividad = (
                PythonActivity.mActivity
            )

            manager = (
                actividad.getSystemService(
                    Context.SENSOR_SERVICE
                )
            )

            sensor = (
                manager.getDefaultSensor(
                    Sensor.TYPE_MAGNETIC_FIELD
                )
            )

            if sensor is None:

                self.valor.text = "N/A"

                self.estado.text = (
                    "SIN MAGNETÓMETRO"
                )

                self.estado.color = (
                    1,
                    0.25,
                    0.25,
                    1
                )

                return

            self.manager = manager
            self.sensor = sensor

            self.listener = SensorListener(
                self
            )

            manager.registerListener(
                self.listener,
                sensor,
                SensorManager.SENSOR_DELAY_GAME
            )

            self.estado.text = (
                "SENSOR ACTIVO"
            )

        except Exception as e:

            self.estado.text = (
                "ERROR"
            )

            print(e)

    # ==================================
    # ACTUALIZAR
    # ==================================

    def actualizar(
        self,
        x,
        y,
        z,
        intensidad
    ):

        self.valor.text = (
            f"{intensidad:.1f}"
        )

        self.x_label.text = (
            f"X: {x:.1f}"
        )

        self.y_label.text = (
            f"Y: {y:.1f}"
        )

        self.z_label.text = (
            f"Z: {z:.1f}"
        )

        # Máximo
        if intensidad > self.maximo:

            self.maximo = intensidad

            self.max_label.text = (
                f"MÁXIMO: {self.maximo:.1f} µT"
            )

        # Barra
        self.barra.value = min(
            intensidad,
            300
        )

        # Estados
        if intensidad < 60:

            self.estado.text = (
                "🟢 CAMPO NORMAL"
            )

            self.estado.color = (
                0.3,
                1,
                0.4,
                1
            )

        elif intensidad < 120:

            self.estado.text = (
                "🟡 CAMPO ELEVADO"
            )

            self.estado.color = (
                1,
                0.8,
                0.2,
                1
            )

        else:

            self.estado.text = (
                "🔴 CAMPO MAGNÉTICO FUERTE"
            )

            self.estado.color = (
                1,
                0.25,
                0.25,
                1
            )

            # Vibrar como máximo cada 1 segundo
            ahora = time.time()

            if ahora - self.ultimo_vibrado > 1:

                try:

                    vibrator.vibrate(
                        0.2
                    )

                except:

                    pass

                self.ultimo_vibrado = ahora

    # ==================================
    # RESET
    # ==================================

    def reset_maximo(self, instance):

        self.maximo = 0

        self.max_label.text = (
            "MÁXIMO: -- µT"
        )

    # ==================================
    # CERRAR
    # ==================================

    def on_stop(self):

        try:

            self.manager.unregisterListener(
                self.listener
            )

        except:

            pass


if __name__ == "__main__":
    DetectorApp().run()
