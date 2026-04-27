#------------ФАЙЛОВЫЙ МЕНЕДЖЕР--------------
#Что должен уметь:
#Создание и удаление директорий
#Навигация по файловой системе внутри рабочей директории
#Создание файлов
#Чтение файлов
#Запись в файлы
#Удаление файлов
#Копирование файлов
#Перемещение файлов
#Переименование файлов
#Пользовательский интерфейс - текстовый
#Должна быть кросплатформенность

#Программа будет иметь псевдоинтерфейс на textual
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid, Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Tree, TextArea, Input
from textual.reactive import reactive
from pathlib import Path
import shutil
import os

# --- ОКНО ВВОДА ИМЕНИ ---
class InputModal(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Введите название:", id="label"),
            Input(placeholder="имя..."),
            Horizontal(
                Button("Ок", variant="success", id="ok"),
                Button("Отмена", variant="error", id="cancel"),
            ),
            id="input-dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss("")

# --- ОСНОВНОЕ ПРИЛОЖЕНИЕ ---
class AdvancedFileManager(App):
    CSS = """
    #input-dialog {
        grid-size: 1;
        grid-rows: 1fr 3 3;
        padding: 1 2;
        width: 40;
        height: 15;
        border: thick $accent;
        background: $surface;
        align: center middle;
    }
    #main-view { display: none; }
    .visible { display: block !important; }
    #sidebar { width: 35; border-right: tall $primary; }
    .icon-button { min-width: 3; margin: 0; }
    """

    show_main = reactive(False)
    current_path = Path.cwd()

    def compose(self) -> ComposeResult:
        yield Header()

        # Начальный экран (как вы просили)
        with Vertical(id="welcome-view", classes="visible" if not self.show_main else ""):
            yield Static("Добро пожаловать, здесь пока пусто.\nСоздайте директорию или ваш первый файл")
            with Horizontal():
                yield Button("[*] Папка", id="init-dir")
                yield Button("[+] Файл", id="init-file")

        # Основной интерфейс
        with Horizontal(id="main-view", classes="visible" if self.show_main else ""):
            with Vertical(id="sidebar"):
                with Horizontal():
                    yield Button("*", id="add-dir", classes="icon-button")
                    yield Button("+", id="add-file", classes="icon-button")
                    yield Button("✖", id="delete", classes="icon-button", variant="error")
                yield Tree(str(self.current_path.name), id="file-tree")

            yield TextArea(id="editor", show_line_numbers=True)

        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        # Переход к основному виду
        if event.button.id in ["init-dir", "init-file"]:
            self.show_main = True
            self.query_one("#welcome-view").remove_class("visible")
            self.query_one("#main-view").add_class("visible")
            await self.action_create_node("dir" if "dir" in event.button.id else "file")

        # Кнопки в сайдбаре
        if event.button.id == "add-dir": await self.action_create_node("dir")
        if event.button.id == "add-file": await self.action_create_node("file")
        if event.button.id == "delete": self.action_delete_node()

    async def action_create_node(self, node_type: str):
        def check_name(name: str):
            if name:
                path = self.current_path / name
                if node_type == "dir":
                    path.mkdir(exist_ok=True)
                else:
                    path.touch()
                self.refresh_tree()

        self.push_screen(InputModal(), check_name)

    def refresh_tree(self):
        tree = self.query_one("#file-tree")
        tree.root.clear()
        for path in self.current_path.iterdir():
            if path.is_dir():
                tree.root.add(path.name, expand_allow_leaf=True)
            else:
                tree.root.add_leaf(path.name)

    def action_delete_node(self):
        tree = self.query_one("#file-tree")
        if tree.cursor_node:
            name = str(tree.cursor_node.label)
            path = self.current_path / name
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            self.refresh_tree()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        path = self.current_path / str(event.node.label)
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
                self.query_one("#editor").text = content
            except Exception as e:
                self.notify(f"Ошибка чтения: {e}", severity="error")

if __name__ == "__main__":
    AdvancedFileManager().run()
