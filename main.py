from simulador import Simulador
import random, gi, re
from gi.repository import Gtk, Gio

gi.require_version('Gtk', '4.0')

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)

        self.especie_entry = None
        self.cantidad_entry = None
        self.simular_button = None

        self.create_header_bar()
        self.create_boxes()

        self.simular_button.connect("clicked", self.on_simular_button_clicked)

    def on_simular_button_clicked(self, widget):
        check_1 = False
        check_2 = False
        #Valida que los campos esten llenos
        if self.especie_entry.get_text() == "" or self.cantidad_entry.get_text() == "":
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
        if (not re.fullmatch("[A-Za-z]+", self.especie_entry.get_text()) or self.cantidad_entry.get_text().isalpha()) and check_1 == True:
            error_dialog = Gtk.MessageDialog(
                transient_for = self,
                modal = True,
                message_type = Gtk.MessageType.ERROR,
                buttons = Gtk.ButtonsType.OK,
                text = "Error al ingresar los datos",
                secondary_text = "Ingrese el tipo de dato adecuado",
            )
            error_dialog.connect("response", self.on_error_dialog_response)
            error_dialog.show()
        else:
            check_2 = True

        #Si se ingresaron los datos correctamente, se inicia el simulador
        if check_1 == True and check_2 == True:
            pass

    def create_boxes(self):
        #Creacion del panel izquierdo
        left_panel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        left_panel.append(Gtk.Label(label = "Panel izquierdo"))

        #Creacion y configuracion del panel derecho
        right_panel  = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        right_panel.set_size_request(100, -1)
        especie_label = Gtk.Label(label = "Especie:")
        self.especie_entry = Gtk.Entry()
        cantidad_label = Gtk.Label(label = "Cantidad de bacterias:")
        self.cantidad_entry = Gtk.Entry()
        factor_ambiental = Gtk.Label(label = "Factor ambiental:")
        factores_ambientales = Gtk.DropDown.new_from_strings(["Nada", "Antibiótico"])
        self.simular_button = Gtk.Button(label = "Simular")

        right_panel.append(especie_label)
        right_panel.append(self.especie_entry)
        right_panel.append(cantidad_label)
        right_panel.append(self.cantidad_entry)
        right_panel.append(factor_ambiental)
        right_panel.append(factores_ambientales)
        right_panel.append(self.simular_button)

        right_panel.set_halign(Gtk.Align.START)
        left_panel.set_halign(Gtk.Align.END)
        self.set_child(left_panel)
        self.set_child(right_panel)

    def create_header_bar(self):

        #Encabezado
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(titlebar = header_bar)
        self.set_title("Simulador: colonia bacterian")
        
        ################################################
        #Crear menu -> "Accerca de", "Salir"
        menu = Gio.Menu.new()
        self.popover_about_menu = Gtk.PopoverMenu.new_from_model(menu)
        self.about_menu_button = Gtk.MenuButton.new()
        self.about_menu_button.set_popover(self.popover_about_menu)
        self.about_menu_button.set_icon_name("open-menu-symbolic")
        
        header_bar.pack_end(self.about_menu_button)

        #AboutDialog -> "Acerca de"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action_activate)
        self.add_action(about_action)
        menu.append("Acerca de", "win.about")

        #Salir
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action_activate)
        self.add_action(quit_action)
        menu.append("Salir", "win.quit")
        ################################################
    
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