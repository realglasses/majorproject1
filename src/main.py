import os
import sys

# fix backend for linux
if sys.platform.startswith("linux"):
    os.environ["GDK_BACKEND"] = "x11"

import flet as ft
from functions import *


def main(page: ft.Page):
    page.controls.clear()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.auto_scroll = False

    QUIZ_QUESTIONS = [
    "I prefer planned dates over spontaneous adventures.",
    "Quality time matters more to me than gifts.",
    "I love mingling with new people at social events.",
    "Deep conversations beat casual small talk every time.",
    "Brutal honesty is better than sparing someone's feelings.",
    "Splitting bills evenly on early dates is important.",
    "I'm totally fine with my partner having close friends of their preferred gender.",
    "Work-life balance is a higher priority for me than career ambition.",
    "I'd rather stay in with a movie than go out to a loud party.",
    "A shared sense of humor is my top priority for chemistry."
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
            elif not username_input.value.strip():
                show_message(page, "invalid username")
            elif not password_input.value.strip():
                show_message(page, "invalid password")
            elif password_input.value != confirm_password_input.value:
                show_message(page, "passwords do not match")
            else:
                data[username_input.value] = {}
                data[username_input.value]["password"] = password_input.value
                write_info(data)
                info(username_input.value)

        title = ft.Text("New account", size=50, expand=1)
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

        page.add(title, input_fields)
        page.update()

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

        title = ft.Text("Sign in", size=50, expand=1)
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

        page.add(title, input_fields)
        page.update()

    def profile_page(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        if username not in data:
            show_message(page, "error: username not found")
            homepage_handler()
            return

        title = ft.Text(f"Hello, {username}", size=50)

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
            ):
                show_message(page, "please fill all fields")
                return

            if not(18 <= int(age_input.value) <= 120):
                show_message(page, "please input valid age")
                return

            data[username]["first name"] = first_name_input.value
            data[username]["last name"] = last_name_input.value
            data[username]["age"] = int(age_input.value)

            write_info(data)
            quiz(username=username)

        title = ft.Text("Input your details", size=50, expand=1)
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

        input_fields = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            first_name_input,
                            last_name_input,
                            age_input,
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

        page.add(title, input_fields)
        page.update()

    def quiz(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        title = ft.Text(value="Personality Quiz", size=50)
        page.add(title)
        page.update()

        gender_option = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="male", label="male"),
                    ft.Radio(value="female", label="female"),
                    ft.Radio(value="non binary", label="non binary"),
                    ft.Radio(value="other", label= "other"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
        
        gender_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("what is your gender"),
                    gender_option,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=20,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=12,
            width= 600
        )

        gender_prefer = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="male", label="male"),
                    ft.Radio(value="female", label="female"),
                    ft.Radio(value="non binary", label="non binary"),
                    ft.Radio(value="other", label= "other"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
        
        gender_prefer_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("what is your prefered gender"),
                    gender_prefer,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=20,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=12,
            width= 600
        )


        def update_border(radio_group, card):
            if radio_group.value is not None:
                card.border = ft.Border.all(1, ft.Colors.OUTLINE)
                card.update()

        gender_option.on_change = lambda e: update_border(gender_option, gender_card)
        gender_prefer.on_change = lambda e: update_border(gender_prefer, gender_prefer_card)
        page.add(gender_card, gender_prefer_card)

        answers = []
        question_cards = []

        def render_question(question: str) -> tuple:
            radio_group = ft.RadioGroup(
                content=ft.Row(
                    controls=[
                        ft.Radio(value=str(i), label=option)
                        for i, option in enumerate(OPTIONS, 1)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(question),
                        radio_group,
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                padding=20,
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                border_radius=12,
                width= 600
            )

            def update_border(e):
                if radio_group.value is not None:
                    card.border = ft.Border.all(1, ft.Colors.OUTLINE)
                    card.update()

            radio_group.on_change = update_border

            #row here is so that the border shrinks to fit
            row = ft.Row(
                controls=[card],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            page.add(row)
            return radio_group, card

        for question in QUIZ_QUESTIONS:
            radio_group, card = render_question(question=question)
            answers.append(radio_group)
            question_cards.append(card)

        def submit(e=None):
            unanswered = [
                *[i for i, group in enumerate(answers) if group.value == None ]
            ]

            if gender_option.value is None:
                gender_card.border = ft.Border.all(5, ft.Colors.RED_700)
                gender_card.update()

            if gender_prefer.value is None:
                gender_prefer_card.border = ft.Border.all(5, ft.Colors.RED_700)
                gender_prefer_card.update()

            for i, card in enumerate(question_cards):
                if i in unanswered:
                    card.border = ft.Border.all(5, ft.Colors.RED_700)
                card.update()

            if unanswered or gender_prefer.value is None or gender_option.value is None:
                show_message(page, "please answer all questions")
                return

            data[username]["gender"] = gender_option.value
            data[username]["target gender"] = gender_prefer.value

            values = [group.value for group in answers]

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

        #fields req to be full profile
        required_fields = [
            *QUIZ_QUESTIONS,
            "gender",
            "target gender",
        ]

        if not all(field in data[username] for field in required_fields):
                    show_message(page, "please complete your profile and quiz")
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

            if not all(field in data[person] for field in required_fields):
                continue

            #rejects if not favourable gender arrangement
            if data[person]["gender"] != data[username]["target gender"]:
                continue

            if data[username]["gender"] != data[person]["target gender"]:
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
        # the lambda function ensures that usernames do not affect
        # the order of matches when scores are tied 
        # (python sorts tuples by next term if collisions occur)
        matches = matches[:3]

        fields = []

        for match in matches:
            if match[1] == None:
                continue

            percent_match = round((match[0]-10) / 40 * 100, 2)
            user = match[1]
            fields.append((user, percent_match))

        if len(fields) < 1:
            show_message(page, "there are no people to match")
            return

        reset_page(page)

        page.add(ft.Text("Matches", size=50, expand=1))
        for i, match in enumerate(fields, 1):
            page.add(
                ft.Row(
                    controls= [ft.Container(
                        ft.Column(
                            controls= [
                                ft.Text(match[0], size=25, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{match[1]}% match", size=18), 

                                *[
                                    ft.Text(f"{question}: {data[match[0]][question]}")
                                    for question in data[match[0]] if (question != "password" and question not in QUIZ_QUESTIONS)
                                ]
                            ],
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            tight=True,
                        ),
                        padding=20,
                        border=ft.Border.all(1, ft.Colors.OUTLINE),
                        border_radius=12,
                        width= 500,
                    )],
                    alignment= ft.MainAxisAlignment.CENTER
                )
            )

        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=lambda e: profile_page(username=username),
        )

        page.update()

    def view_user(username=None) -> None:
        reset_page(page)
        data = read_info()

        if username == None or username not in data:
            show_message(page, "username error")
            return

        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=lambda e: profile_page(username=username),
        )

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
