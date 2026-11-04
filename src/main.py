import flet as ft
import json
from pathlib import Path
from functions import *


def main(page: ft.Page):
    page.controls.clear()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
        
    def homepage() -> None:
        reset_page(page)

        title = ft.Text("epic dating app", size= 50, expand= 1)

        page.add(title)

        sign_in_button = ft.Button(
            content= "sign in",
            on_click= sign_in_handler
        )
        new_user_button = ft.Button(
            content= "add new user",
            on_click= new_user_handler,
        )
        view_users_button = ft.Button(
            content= "view users",
            on_click= view_user_handler,
        )
        quit_button = ft.Button(
            content= "quit",
            on_click= quit_app
        )

        options = ft.Row(
            controls= [
                ft.Container(expand= 1),
                ft.Container(
                    content= ft.Column(
                        controls= [
                            sign_in_button,
                            new_user_button,
                            view_users_button,
                            quit_button
                        ],
                        horizontal_alignment= ft.CrossAxisAlignment.STRETCH
                    ),
                    expand= 1
                ),
                ft.Container(expand= 1)
            ]
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
            elif password_input.value != confirm_password_input.value:
                show_message(page, "passwords do not match")
            else:
                data[username_input.value] = {}
                data[username_input.value]["password"] = password_input.value
                write_info(data)
                info(username_input.value)

        username_input = ft.TextField(label= "username")
        password_input = ft.TextField(label= "password", can_reveal_password= True)
        confirm_password_input = ft.TextField(label= "confirm password", can_reveal_password= True)

        submit_button = ft.Button(
            content="submit",
            on_click=submit,
            expand= 1
        )
        page.floating_action_button = ft.FloatingActionButton(
            content="go back",
            on_click=homepage_handler,
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand= 1),
                ft.Container(
                    content = ft.Column(
                        controls= [
                            username_input, 
                            password_input,
                            confirm_password_input,
                            submit_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ), 
                    expand= 1
                ),
                ft.Container(expand= 1)
            ]
        )

        page.add(input_fields)
        page.update()

    def render_question(question: str, options: list[str]) -> ft.Row:
        title = ft.Text(value=question)

        optionsradio = ft.Row(
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    content=ft.RadioGroup(
                        content=ft.Row(
                            controls=[
                                ft.Radio(
                                    value= opt, 
                                    label= opt, 
                                    expand= True
                                )
                                for opt in options
                            ],
                        )
                    ),
                    expand=3,
                    alignment=ft.Alignment.CENTER_LEFT,
                ),
                ft.Container(expand=1),
            ],
        )
        page.add(title, ft.Text(""), optionsradio, ft.Text(""), ft.Text(""))

        return optionsradio

    def sign_in() -> None:
        reset_page(page)
        data = read_info()

        def submit(e= None):
            if username_input.value not in data:
                show_message(page, "username does not exist")
            elif data[username_input.value]["password"] != password_input.value:
                show_message(page, "incorrect password")
            else:
                profile_page_handler(username= username_input.value)

        username_input = ft.TextField(label= "username")
        password_input = ft.TextField(label= "password", can_reveal_password= True)

        submit_button = ft.Button(
            content= "submit",
            on_click= submit,
            expand= 1
        )

        page.floating_action_button = ft.FloatingActionButton(
            content= "go back",
            on_click= homepage_handler
        )

        input_fields = ft.Row(
            controls=[
                ft.Container(expand= 1),
                ft.Container(
                    content = ft.Column(
                        controls= [
                            username_input, 
                            password_input,
                            submit_button
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ), 
                    expand= 1
                ),
                ft.Container(expand= 1)
            ]
        )
        
        page.add(input_fields)
        page.update()

    def profile_page(username: str = None) -> None:
        reset_page(page)
        data = read_info()
        if username not in data:
            show_message(page, "error: username not found")
            homepage_handler()

        title = ft.Text(f"hello, {username}", size= 50)
        redo_quiz_button = ft.Button(
            content= "redo quiz",
            on_click= lambda e: quiz(username= username)
        )
        generate_matches_button = ft.Button(
            content= "generate matches",
            on_click= lambda e: generate_matches_handler(username= username),
        )
        
        input_fields = ft.Row(
            controls=[
                ft.Container(expand= 1),
                ft.Container(
                    content = ft.Column(
                        controls= [
                            redo_quiz_button,
                            generate_matches_button
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ), 
                    expand= 1
                ),
                ft.Container(expand= 1)
            ]
        )

        page.floating_action_button = ft.FloatingActionButton(
            content= "sign out",
            on_click= homepage_handler
        )
        page.add(title, input_fields)

    def info(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        def submit(e = None):
            if not (first_name_input.value and last_name_input.value and age_input.value and gender_input.value):
                show_message(page, "please fill all fields")
                return
            data[username]["first_name"] = first_name_input.value
            data[username]["last_name"] = last_name_input.value
            data[username]["age"] = age_input.value
            data[username]["gender"] = gender_input.value
            write_info(data)
            quiz(username)

        first_name_input = ft.TextField(
            label= "first name",
            input_filter= ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$")
        )
        last_name_input = ft.TextField(
            label= "last name",
            input_filter= ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$")
        )
        age_input = ft.TextField(
            label= "age",
            input_filter= ft.NumbersOnlyInputFilter()
        )
        gender_input = ft.TextField(
            label= "gender",
            input_filter= ft.InputFilter(regex_string=r"^[a-zA-Z0-9]*$")
        )

        input_fields = ft.Row(
            controls= [
                ft.Container(expand= 1),
                ft.Container(
                    content= ft.Column(
                        controls= [
                            first_name_input,
                            last_name_input,
                            age_input,
                            gender_input
                        ],
                        horizontal_alignment= ft.CrossAxisAlignment.STRETCH
                    ),
                    expand= 1
                ),
                ft.Container(expand= 1)
            ]
        )

        page.floating_action_button = ft.FloatingActionButton(
            content= "submit",
            on_click= submit
        )
        page.add(input_fields)
        page.update()

    def quiz(username: str = None) -> None:
        reset_page(page)
        data = read_info()

        quizquestions = [
            {"question": "q1", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q2", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q3", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q4", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q5", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q6", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q7", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q8", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q9", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
            {"question": "q10", "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]},
        ]

        title = ft.Text(value= "personality quiz", size= 50)
        page.add(title)
        page.update()

        choices = []

        for question in quizquestions:
            choices.append(
                render_question(
                    question["question"],
                    question["options"],
                )
            )

        def submit(e=None):
            for row, question in zip(choices, quizquestions):
                if row.controls[1].content.value:
                    data[username][question["question"]] = row.controls[1].content.value
                    
                else:
                    show_message(page, "please answer all questions")
                    return

            write_info(data)
            profile_page_handler(username= username)

        page.floating_action_button = ft.FloatingActionButton(
            content="go back",
            on_click= lambda e: profile_page_handler(username= username),
        )

        submit_button = ft.Button(
            "submit", 
            on_click= submit
        )

        page.add(submit_button)
        page.update()

    def generate_matches(username: str = None) -> None:
        data = read_info()

        if username == None:
            show_message(page, "error")
            return

        if len(data) < 2:
            show_message(page, "there are no people to match")
            return
        
        reset_page(page)
        values = {
            "strongly disagree": 0,
            "disagree": 1, 
            "neutral": 2, 
            "agree": 3, 
            "strongly agree": 4
        }
        matches = [
            (
                0,      #score
                None    #username
            )
            for _ in range(3)
        ]
        for person in data:
            score = 0
            if person == username:
                continue
            for question in data[person]: 
                try:
                    score += (5 - abs(values[data[person][question]] - values[data[username][question]]))
                except KeyError:
                    pass
            matches.sort()
            for i, match in enumerate(matches):
                if score > match[0]:
                    matches[i] = (score, person)
                    break
            matches.sort(reverse= True)
            print(matches)
        fields = []
        for match in matches:
            percent_match = round(match[0]/50 * 100, 2)
            user = match[1]
            fields.append((user, percent_match))
        for match in fields: page.add(ft.Text(match[0]), ft.Text(f"{match[1]}%"))

            
            
            

        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=homepage_handler,
        )    
        page.update()

    def view_user() -> None:
        reset_page(page)
        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("go back"),
            on_click=homepage_handler,
        )

        data = read_info()

        if data == {}:
            page.add(ft.Text("there are no users"))
            page.update()
            return

        for user in data:
            page.add(ft.Text(f"user: {user}"))

            page.add(
                ft.Row(
                    controls=[
                        ft.Container(expand=1),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{question}: {data[user][question]}"
                                    )
                                    for question in data[user] if question != "password"
                                ]
                            ),
                            expand=2,
                            alignment=ft.Alignment.CENTER_LEFT,
                        ),
                        ft.Container(expand=1),
                    ]
                )
            )

        page.update()

    def homepage_handler(e= None):
        homepage()

    def new_user_handler(e= None):
        new_user()

    def generate_matches_handler(e= None, username: str = None):
        generate_matches(username= username)

    def view_user_handler(e= None):
        view_user()

    def sign_in_handler(e= None):
        sign_in()

    def profile_page_handler(e= None, username: str = None):
        profile_page(username)

    async def quit_app(e= None):
        await page.window.close()

    homepage()


ft.run(main)
