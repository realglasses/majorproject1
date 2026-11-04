import os
import sys

# Linux-specific GTK backend configuration.
if sys.platform.startswith("linux"):
    os.environ["GDK_BACKEND"] = "x11"

import flet as ft
from functions import *


def main(page: ft.Page):
    page.controls.clear()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    QUIZ_QUESTIONS = [
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
    ]

    OPTIONS = [
        "Strongly disagree",
        "Disagree",
        "Neutral",
        "Agree",
        "Strongly agree",
    ]

    def homepage() -> None:
        reset_page(page)

        title = ft.Text("Epic Dating App", size=50, expand=1)
        page.add(title)

        sign_in_button = ft.Button(
            content="sign in",
            on_click=sign_in_handler,
        )
        new_user_button = ft.Button(
            content="add new user",
            on_click=new_user_handler,
        )
        quit_button = ft.Button(
            content="quit",
            on_click=quit_app,
        )

        options = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            sign_in_button,
                            new_user_button,
                            quit_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=1,
                ),
                ft.Container(expand=1),
            ],
        )

        page.add(options)
        page.update()

    def new_user() -> None:
        reset_page(page)
        data = read_info()

        def submit(e=None):
            if username_input.value in data:
                show_message(page, "username taken")
            elif username_input.value == "":
                show_message(page, "invalid username")
            elif password_input.value == "":
                show_message(page, "invalid password")
            elif password_input.value != confirm_password_input.value:
                show_message(page, "passwords do not match")
            else:
                data[username_input.value] = {}
                data[username_input.value]["password"] = password_input.value
                write_info(data)
                info(username_input.value)

        username_input = ft.TextField(label="username")
        password_input = ft.TextField(
            label="password",
            can_reveal_password=True,
        )
        confirm_password_input = ft.TextField(
            label="confirm password",
            can_reveal_password=True,
        )

        submit_button = ft.Button(
            content="submit",
            on_click=submit,
            expand=1,
        )
        page.floating_action_button = ft.FloatingActionButton(
            content="go back",
            on_click=homepage_handler,
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            username_input,
                            password_input,
                            confirm_password_input,
                            submit_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=1,
                ),
                ft.Container(expand=1),
            ],
        )

        page.add(input_fields)
        page.update()

    def render_question(question: str) -> ft.Slider:
        slider = ft.Slider(
            min=1,
            max=5,
            divisions=4,
            value=None,
            label="{value}",
        )

        answer = ft.Text("select and answer")

        def update_answer(e=None):
            answer.value = OPTIONS[int(e.control.value) - 1]
            answer.update()

        slider.on_change = update_answer

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(question),
                    slider,
                    answer,
                ],
                spacing=10,
            ),
            padding=20,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=12,
        )

        page.add(card)

        return slider

    def sign_in() -> None:
        reset_page(page)
        data = read_info()

        def submit(e=None):
            if username_input.value not in data:
                show_message(page, "username does not exist")
            elif data[username_input.value]["password"] != password_input.value:
                show_message(page, "incorrect password")
            else:
                profile_page_handler(username=username_input.value)

        username_input = ft.TextField(label="username")
        password_input = ft.TextField(
            label="password",
            can_reveal_password=True,
        )

        submit_button = ft.Button(
            content="submit",
            on_click=submit,
            expand=1,
        )

        page.floating_action_button = ft.FloatingActionButton(
            content="go back",
            on_click=homepage_handler,
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            username_input,
                            password_input,
                            submit_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=1,
                ),
                ft.Container(expand=1),
            ],
        )

        page.add(input_fields)
        page.update()

    def profile_page(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        if username not in data:
            show_message(page, "error: username not found")
            homepage_handler()
            return

        title = ft.Text(f"hello, {username}", size=50)

        redo_quiz_button = ft.Button(
            content="redo quiz",
            on_click=lambda e: quiz(username=username),
        )
        generate_matches_button = ft.Button(
            content="generate matches",
            on_click=lambda e: generate_matches_handler(username=username),
        )
        view_info_button = ft.Button(
            content="view info",
            on_click=lambda e: view_info_handler(username=username),
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            redo_quiz_button,
                            generate_matches_button,
                            view_info_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=1,
                ),
                ft.Container(expand=1),
            ],
        )

        page.floating_action_button = ft.FloatingActionButton(
            content="sign out",
            on_click=homepage_handler,
        )

        page.add(title, input_fields)
        page.update()

    def info(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        def submit(e=None):
            if not (
                first_name_input.value
                and last_name_input.value
                and age_input.value
                and gender_input.value
            ):
                show_message(page, "please fill all fields")
                return

            data[username]["first name"] = first_name_input.value
            data[username]["last name"] = last_name_input.value
            data[username]["age"] = age_input.value
            data[username]["gender"] = gender_input.value

            write_info(data)
            quiz(username=username)

        first_name_input = ft.TextField(
            label="first name",
            input_filter=ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$"),
        )
        last_name_input = ft.TextField(
            label="last name",
            input_filter=ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$"),
        )
        age_input = ft.TextField(
            label="age",
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        gender_input = ft.TextField(
            label="gender",
            input_filter=ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$"),
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            first_name_input,
                            last_name_input,
                            age_input,
                            gender_input,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=1,
                ),
                ft.Container(expand=1),
            ],
        )

        page.floating_action_button = ft.FloatingActionButton(
            content="submit",
            on_click=submit,
        )

        page.add(input_fields)
        page.update()

    def quiz(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        title = ft.Text(value="personality quiz", size=50)
        page.add(title)
        page.update()

        answers = []

        for question in QUIZ_QUESTIONS:
            selected = render_question(question=question)
            answers.append(selected)

        def submit(e=None):
            values = [slider.value for slider in answers]

            if not all(values):
                show_message(page, "please answer all questions")
                return

            for i, question in enumerate(QUIZ_QUESTIONS):
                data[username][question] = OPTIONS[int(values[i]) - 1]

            write_info(data)
            profile_page_handler(username=username)

        page.floating_action_button = ft.FloatingActionButton(
            content="go back",
            on_click=lambda e: profile_page_handler(username=username),
        )

        submit_button = ft.Button(
            "submit",
            on_click=submit,
        )

        page.add(submit_button)
        page.update()

    def generate_matches(username: str = None) -> None:
        data = read_info()

        if username == None or username not in data:
            show_message(page, "error")
            return

        if not all(question in data[username] for question in QUIZ_QUESTIONS):
            show_message(page, "please complete the quiz")
            return

        values = {
            key: value
            for value, key in enumerate(OPTIONS)
        }
        matches = []

        for person in data:
            score = 0

            if person == username:
                continue

            if not all(question in data[person] for question in QUIZ_QUESTIONS):
                continue

            for question in QUIZ_QUESTIONS:
                try:
                    score += 5 - abs(
                        values[data[person][question]]
                        - values[data[username][question]]
                    )
                except KeyError:
                    pass

            matches.append((score, person))
            matches.sort(key=lambda x: x[0], reverse=True)

            # The lambda function ensures that usernames do not affect
            # the order of matches when scores are tied.
            matches = matches[:3]

        fields = []

        for match in matches:
            if match[1] == None:
                continue

            percent_match = round(match[0] / 50 * 100, 2)
            user = match[1]
            fields.append((user, percent_match))

        if len(fields) < 1:
            show_message(page, "there are no people to match")
            return

        reset_page(page)

        for i, match in enumerate(fields, 1):
            page.add(
                ft.Text(f"match {i}: {match[0]}"),
                ft.Text(f"percentage match: {match[1]}%"),
            )

        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=homepage_handler,
        )

        page.update()

    def view_user(username=None) -> None:
        reset_page(page)

        if username == None or username not in data:
            show_message(page, "username error")
            return

        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=lambda e: profile_page(username=username),
        )

        data = read_info()

        if data == {}:
            show_message(page, "data error")
            return

        for question in data[username]:
            if question == "password": 
                continue

            page.add(
                ft.Text(
                    f"{question}: {data[username][question]}",
                )
            )

        page.update()

    def homepage_handler(e=None):
        homepage()

    def new_user_handler(e=None):
        new_user()

    def generate_matches_handler(e=None, username: str = None):
        generate_matches(username=username)

    def view_info_handler(e=None, username=None):
        view_user(username=username)

    def sign_in_handler(e=None):
        sign_in()

    def profile_page_handler(e=None, username: str = None):
        profile_page(username)

    async def quit_app(e=None):
        await page.window.close()

    homepage()


ft.run(main)
