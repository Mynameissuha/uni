from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,Static
from textual.containers import Horizontal
from textual.binding import Binding

TEXT = "Здесь будет ваш текст"
footer_text = "[h]-help"
class Lout(App):
    BINDINGS = [
        Binding(key = "q",action = "quit",description = "Quit the app"),
        Binding(key = "h",action= "help",description = "Show help screen",key_display = "h"),
        ]
    CSS = """
    #sidebar {
    width: 15;
    height: 100%;
    background: black;}"""
    def compose(self) -> ComposeResult:
        yield Header(id = "header")
        yield Footer()
        with Horizontal():
            yield Static("Sidebar1",id = "sidebar")
            yield Static(TEXT,id = "body")

if __name__ == "__main__":
    app = Lout()
    app.run()
