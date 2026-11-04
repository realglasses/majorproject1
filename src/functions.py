import flet as ft
import json
from pathlib import Path

def read_info() -> dict:
        try:
            with open("profiles.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
            Path("profiles.json").touch()

        return data

def write_info(data) -> None:
    try:
        with open("profiles.json", "w") as f:
            json.dump(data, f)
    except(FileNotFoundError, json.JSONDecodeError):
        Path("profiles.json").touch()

def show_message(page: ft.Page, message: str) -> None:
    page.show_dialog(
        ft.SnackBar(
            content=ft.Text(message, color="#FFFFFF"),
            duration=3000,
            action=ft.SnackBarAction(
                label="ok",
                text_color="#FFFFFF",
            ),
            bgcolor="#2C3E50",
        )
    )

def reset_page(page) -> None:
    page.controls.clear()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.floating_action_button = None
    page.pop_dialog()