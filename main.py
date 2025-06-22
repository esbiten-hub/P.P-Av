import random, gi, re, io
from PIL import Image
from simulador import Simulador
from gi.repository import Gtk, Gdk, GLib, Gio

gi.require_version('Gtk', '4.0')

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)

        self.especie_entry = None
        self.cantidad_entry = None
        self.simular_button = None
        self.pasos_entry = None
        self.factores_ambientales = None
        self.siguiente_button = None
        self.scroll_list = []
        self.scroll_en_pantalla = None
        self.simulador = None

        self.left_panel = None
        self.right_panel = None

        self.create_header_bar()
        self.create_boxes()

        self.simular_button.connect("clicked", self.on_simular_button_clicked)
        self.siguiente_button.connect("clicked", self.on_siguiente_button_clicked)

    def create_boxes(self):
        #Creacion del panel izquierdo
        self.left_panel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.left_panel.set_hexpand(True)
        self.left_panel.set_vexpand(True)

        #Creacion y configuracion del panel derecho
        self.right_panel  = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        especie_label = Gtk.Label(label = "Especie:")
        self.especie_entry = Gtk.Entry()
        cantidad_label = Gtk.Label(label = "Cantidad de bacterias (máx 5):")
        self.cantidad_entry = Gtk.Entry()
        pasos_label = Gtk.Label(label = "Pasos a simular (máx 20):")
        self.pasos_entry = Gtk.Entry()
        factor_ambiental = Gtk.Label(label = "Factor ambiental:")
        self.factores_ambientales = Gtk.DropDown.new_from_strings(["Nada", "Antibiótico"])
        self.simular_button = Gtk.Button(label = "Simular")
        self.siguiente_button  = Gtk.Button(label = "Siguiente paso")

        box_espaciador = Gtk.Box()
        box_espaciador.set_vexpand(True)

        self.right_panel.append(especie_label)
        self.right_panel.append(self.especie_entry)
        self.right_panel.append(cantidad_label)
        self.right_panel.append(self.cantidad_entry)
        self.right_panel.append(pasos_label)
        self.right_panel.append(self.pasos_entry)
        self.right_panel.append(factor_ambiental)
        self.right_panel.append(self.factores_ambientales)
        self.right_panel.append(self.simular_button)
        self.right_panel.append(box_espaciador)
        self.right_panel.append(self.siguiente_button)

        #Disposicion de los paneles
        main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        main_box.append(self.left_panel)
        main_box.append(self.right_panel)
        self.set_child(main_box)

    def create_header_bar(self):

        #Encabezado
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(titlebar = header_bar)
        self.set_title("Simulador: colonia bacteriana")
        
        ################################################
        #Crear menu -> "Acerca de", "Salir"
        about_menu = Gio.Menu.new()
        self.popover_about_menu = Gtk.PopoverMenu.new_from_model(about_menu)
        self.about_menu_button = Gtk.MenuButton.new()
        self.about_menu_button.set_popover(self.popover_about_menu)
        self.about_menu_button.set_icon_name("help-about-symbolic")
        
        header_bar.pack_end(self.about_menu_button)

        #AboutDialog -> "Acerca de"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action_activate)
        self.add_action(about_action)
        about_menu.append("Acerca de", "win.about")

        #Boton -> Salir
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action_activate)
        self.add_action(quit_action)
        about_menu.append("Salir", "win.quit")
        ################################################

        ################################################
        #Crear menu -> graficas
        graficas_menu = Gio.Menu.new()
        self.popover_graficas_menu = Gtk.PopoverMenu.new_from_model(graficas_menu)
        self.graficas_menu_button = Gtk.MenuButton.new()
        self.graficas_menu_button.set_popover(self.popover_graficas_menu)
        self.graficas_menu_button.set_icon_name("open-menu-symbolic")
        
        header_bar.pack_start(self.graficas_menu_button)

        #Graficas de crecimiento Dialog -> "Grafica de crecimiento"
        graficas_crecimiento_action = Gio.SimpleAction.new("graficas_crecimiento", None)
        graficas_crecimiento_action.connect("activate", self.on_graficas_crecimiento_activate)
        self.add_action(graficas_crecimiento_action)
        graficas_menu.append("Grafica de crecimiento", "win.graficas_crecimiento")

        #Graficas de resistencia Dialog -> "Grafica de resistencia"
        graficas_resistencia_action = Gio.SimpleAction.new("graficas_resistencia", None)
        graficas_resistencia_action.connect("activate", self.on_graficas_resistencia_activate)
        self.add_action(graficas_resistencia_action)
        graficas_menu.append("Grafica de resistencia", "win.graficas_resistencia")
        ################################################
    
    def on_simular_button_clicked(self, widget):
        check_1 = False
        check_2 = False
        #Valida que los campos esten llenos
        if self.especie_entry.get_text() == "" or self.cantidad_entry.get_text() == "" or self.pasos_entry.get_text() == "":
            error_dialog = Gtk.MessageDialog(
                transient_for = self,
                modal = True,
                message_type = Gtk.MessageType.ERROR,
                buttons = Gtk.ButtonsType.OK,
                text = "Error al ingresar los datos",
                secondary_text = "Complete todos los campos",
            )
            error_dialog.connect("response", self.on_error_dialog_response)
            error_dialog.show()
        else:
            check_1 = True
        #Valida que se ingrese el tipo de dato adecuado
        if (not re.fullmatch("[A-Za-z]+", self.especie_entry.get_text()) or self.cantidad_entry.get_text().isalpha() or int(self.cantidad_entry.get_text()) > 5 or self.pasos_entry.get_text().isalpha() or int(self.pasos_entry.get_text()) > 20) and check_1 == True:
            error_dialog = Gtk.MessageDialog(
                transient_for = self,
                modal = True,
                message_type = Gtk.MessageType.ERROR,
                buttons = Gtk.ButtonsType.OK,
                text = "Error al ingresar los datos",
                secondary_text = "Ingrese el tipo/cantidad de dato adecuado",
            )
            error_dialog.connect("response", self.on_error_dialog_response)
            error_dialog.show()
        else:
            check_2 = True

        #Si se ingresaron los datos correctamente, se inicia el simulador
        if check_1 == True and check_2 == True:
            #Limpia simulaciones anteriores
            if self.scroll_en_pantalla != None:
                self.left_panel.remove(self.scroll_en_pantalla)
                self.scroll_en_pantalla = None

            self.scroll_list = []
            self.simulador = Simulador(self.especie_entry.get_text(), int(self.cantidad_entry.get_text()), self.factores_ambientales.get_selected_item().get_string(), int(self.pasos_entry.get_text()))
            self.simulador.inicia_simulacion()
            bytes_por_simulacion = self.simulador.run()
            
            for i in bytes_por_simulacion:
                #Cargar imagen con PIL
                image = Image.open(i)
                width, height = image.size

                #Convertir a bytes
                data = image.tobytes()
                gbytes = GLib.Bytes.new(data)
            
                texture = Gdk.MemoryTexture.new(
                    width,
                    height,
                    5,
                    gbytes,
                    width * 4
                )

                #Crea el Gtk.Picture()
                picture = Gtk.Picture()
                picture.set_paintable(texture)
                picture.set_hexpand(True)
                picture.set_vexpand(True)

                #Poner imagen en scroll
                scroll = Gtk.ScrolledWindow()
                scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
                scroll.set_child(picture)

                self.scroll_list.append(scroll)

            self.left_panel.append(self.scroll_list[0])
            self.scroll_en_pantalla = self.scroll_list[0]

    def on_siguiente_button_clicked(self, widget):
        contador = 0
        for i in self.scroll_list:
            if i == self.scroll_en_pantalla:
                if contador + 1 > len(self.scroll_list) - 1:
                    break
                else:
                    self.left_panel.remove(i)
                    self.scroll_en_pantalla = self.scroll_list[contador + 1]
                    self.left_panel.append(self.scroll_en_pantalla)
                    break
            else:
                contador += 1

    def on_graficas_crecimiento_activate(self, action, param):
        open_grafico_dialog = Gtk.FileDialog.new()
        open_grafico_dialog.open(self, None, self.open_grafico_crecimiento_response)

    def open_grafico_crecimiento_response(self, widget, response):
        archivo = widget.open_finish(response)

        #Recibe imagen de la grafica
        image, width, height = self.simulador.graficar_crecimiento(archivo)

        #Convertir a bytes
        data = image.tobytes()
        gbytes = GLib.Bytes.new(data)
    
        texture = Gdk.MemoryTexture.new(
            width,
            height,
            5,
            gbytes,
            width * 4
        )

        #Crea el Gtk.Picture()
        picture = Gtk.Picture()
        picture.set_paintable(texture)
        picture.set_hexpand(True)
        picture.set_vexpand(True)

        #Poner imagen en scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(picture)

        self.left_panel.remove(self.scroll_en_pantalla)
        self.left_panel.append(scroll)
        self.scroll_en_pantalla = scroll

    def on_graficas_resistencia_activate(self, action, param):
        open_grafico_dialog = Gtk.FileDialog.new()
        open_grafico_dialog.open(self, None, self.open_grafico_resistencia_response)

    def open_grafico_resistencia_response(self, widget, response):
        archivo = widget.open_finish(response)

        #Recibe imagen de la grafica
        image, width, height = self.simulador.graficar_resistencia(archivo)

        #Convertir a bytes
        data = image.tobytes()
        gbytes = GLib.Bytes.new(data)
    
        texture = Gdk.MemoryTexture.new(
            width,
            height,
            5,
            gbytes,
            width * 4
        )

        #Crea el Gtk.Picture()
        picture = Gtk.Picture()
        picture.set_paintable(texture)
        picture.set_hexpand(True)
        picture.set_vexpand(True)

        #Poner imagen en scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(picture)

        self.left_panel.remove(self.scroll_en_pantalla)
        self.left_panel.append(scroll)
        self.scroll_en_pantalla = scroll

    def on_about_action_activate(self, action, param):
        about_dialog = Gtk.AboutDialog(
            transient_for = self,
            modal = True,
            authors = ["Esteban Bustamante V"],
            copyright = "Copyright 2025",
            license_type = Gtk.License.GPL_3_0,
            website = "https://example.com",
            website_label = "Colonia bacteriana",
            version = "1.0",
            logo_icon_name = "help-about-symbolic",
            comments = "Simulador de una colonia de bacterias",
            visible = True,
        )
    
    def on_error_dialog_response(self, widget, action):
        widget.destroy()

    def on_quit_action_activate(self, _action, param):
        quit()

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id = "org.proyecto.simulador")

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application = self)
            self.win.present()

app = Application()
app.run()    