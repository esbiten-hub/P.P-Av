from simulador import Simulador
import random, gi
from gi.repository import Gtk, Gio

gi.require_version('Gtk', '4.0')

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(800, 600)
        
        self.header_bar = self.create_header_bar()
    
    def create_header_bar(self):

        #Encabezado
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(titlebar = header_bar)
        self.set_title("Simulador: colonia bacterian")

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

        return header_bar
    
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