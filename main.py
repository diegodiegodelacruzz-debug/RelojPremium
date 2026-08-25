from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime

try:
    from plyer import battery
    BATTERY_OK = True
except Exception:
    BATTERY_OK = False

class Panel(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.04, 0.04, 0.05, 1)
            self.fondo = RoundedRectangle(pos=self.pos, size=self.size, radius=[25])
        self.bind(pos=self._update_bg, size=self._update_bg)
    def _update_bg(self, *args):
        self.fondo.pos = self.pos
        self.fondo.size = self.size

class RelojApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0.01, 0.015, 1)
        try: Window.fullscreen = True
        except Exception: pass
        self.formato_24 = True
        self.mostrar_fecha = True
        self.mostrar_bateria = True
        self.menu = None
        self.root = FloatLayout()
        self.hora = Label(text='00:00:00', font_size='82sp', bold=True,
                          color=(0.95,0.95,0.98,1), size_hint=(1,.25),
                          pos_hint={'center_x':.5,'center_y':.59})
        self.fecha = Label(text='', font_size='20sp', color=(.55,.57,.62,1),
                           size_hint=(1,.10), pos_hint={'center_x':.5,'center_y':.42})
        self.bateria = Label(text='', font_size='17sp', color=(.45,.47,.52,1),
                             size_hint=(1,.08), pos_hint={'center_x':.5,'center_y':.28})
        self.config = Button(text='⚙', font_size='28sp', background_normal='',
                             background_color=(0,0,0,0), color=(.55,.57,.62,1),
                             size_hint=(None,None), size=('65dp','65dp'),
                             pos_hint={'right':.97,'top':.96})
        self.config.bind(on_release=self.mostrar_menu)
        for w in (self.hora,self.fecha,self.bateria,self.config): self.root.add_widget(w)
        Clock.schedule_interval(self.actualizar, 1)
        self.actualizar(0)
        return self.root
    def actualizar(self, dt):
        ahora = datetime.now()
        self.hora.text = ahora.strftime('%H:%M:%S') if self.formato_24 else ahora.strftime('%I:%M:%S %p')
        dias=['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO']
        meses=['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
        self.fecha.text=f'{dias[ahora.weekday()]}  •  {ahora.day} DE {meses[ahora.month-1]}'
        if BATTERY_OK:
            try:
                p=battery.status.get('percentage')
                self.bateria.text=f'●  {p}%' if p is not None else ''
            except Exception: self.bateria.text=''
    def mostrar_menu(self, instance):
        if self.menu: return
        self.menu=Panel(size_hint=(.88,.78),pos_hint={'center_x':.5,'center_y':.5})
        title=Label(text='CONFIGURACIÓN',font_size='25sp',bold=True,color=(.95,.95,.98,1),size_hint=(1,.15),pos_hint={'center_x':.5,'top':.96})
        self.menu.add_widget(title)
        self.boton_formato=Button(text=self.texto_formato(),font_size='18sp',background_normal='',background_color=(.10,.10,.12,1),color=(.9,.9,.93,1),size_hint=(.82,.16),pos_hint={'center_x':.5,'center_y':.67})
        self.boton_formato.bind(on_release=self.cambiar_formato)
        self.menu.add_widget(self.boton_formato)
        self.boton_fecha=Button(text=self.texto_fecha(),font_size='18sp',background_normal='',background_color=(.10,.10,.12,1),color=(.9,.9,.93,1),size_hint=(.82,.16),pos_hint={'center_x':.5,'center_y':.47})
        self.boton_fecha.bind(on_release=self.cambiar_fecha)
        self.menu.add_widget(self.boton_fecha)
        self.boton_bateria=Button(text=self.texto_bateria(),font_size='18sp',background_normal='',background_color=(.10,.10,.12,1),color=(.9,.9,.93,1),size_hint=(.82,.16),pos_hint={'center_x':.5,'center_y':.27})
        self.boton_bateria.bind(on_release=self.cambiar_bateria)
        self.menu.add_widget(self.boton_bateria)
        cerrar=Button(text='CERRAR',font_size='18sp',background_normal='',background_color=(.15,.15,.17,1),color=(.75,.75,.8,1),size_hint=(.60,.11),pos_hint={'center_x':.5,'y':.06})
        cerrar.bind(on_release=self.cerrar_menu)
        self.menu.add_widget(cerrar)
        self.root.add_widget(self.menu)
    def texto_formato(self): return 'Formato de hora\n24 HORAS' if self.formato_24 else 'Formato de hora\n12 HORAS'
    def texto_fecha(self): return 'Mostrar fecha\nACTIVADO' if self.mostrar_fecha else 'Mostrar fecha\nDESACTIVADO'
    def texto_bateria(self): return 'Mostrar batería\nACTIVADO' if self.mostrar_bateria else 'Mostrar batería\nDESACTIVADO'
    def cambiar_formato(self, instance):
        self.formato_24=not self.formato_24; instance.text=self.texto_formato(); self.actualizar(0)
    def cambiar_fecha(self, instance):
        self.mostrar_fecha=not self.mostrar_fecha; self.fecha.opacity=1 if self.mostrar_fecha else 0; instance.text=self.texto_fecha()
    def cambiar_bateria(self, instance):
        self.mostrar_bateria=not self.mostrar_bateria; self.bateria.opacity=1 if self.mostrar_bateria else 0; instance.text=self.texto_bateria()
    def cerrar_menu(self, instance):
        if self.menu: self.root.remove_widget(self.menu); self.menu=None

if __name__ == '__main__': RelojApp().run()
