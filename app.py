import flet as ft
from groq import Groq
import os

# Groq API Client setup
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
except Exception as e:
    client = None

def main(page: ft.Page):
    page.title = "Gemini AI Assistant"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # চ্যাট হিস্ট্রি এবং সিস্টেম প্রম্পট
    messages_list = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

    chat_history = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True,
        padding=10
    )

    # ভয়েস সিলেক্ট ড্রপডাউন (Female/Male)
    voice_dropdown = ft.Dropdown(
        label="ভয়েস",
        value="Female",
        options=[
            ft.dropdown.Option("Female"),
            ft.dropdown.Option("Male"),
        ],
        width=100,
        text_size=12,
        content_padding=5
    )

    def send_message(e):
        user_text = user_input.value.strip()
        if not user_text:
            return

        # ইউজারের মেসেজ স্ক্রিনে যোগ করা
        chat_history.controls.append(
            ft.Row(
                [ft.Container(ft.Text(user_text, color=ft.colors.WHITE), bgcolor=ft.colors.BLUE_700, padding=12, border_radius=12)],
                alignment=ft.MainAxisAlignment.END
            )
        )
        user_input.value = ""
        page.update()

        messages_list.append({"role": "user", "content": user_text})

        # AI থেকে রেসপন্স আনা
        try:
            if not client:
                reply = "দুঃখিত, এপিআই কি (API Key) পাওয়া যায়নি।"
            else:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in messages_list],
                    temperature=0.5
                )
                reply = res.choices[0].message.content
        except Exception as err:
            reply = f"একটি ত্রুটি হয়েছে: {err}"

        messages_list.append({"role": "assistant", "content": reply})

        # বটের উত্তর স্ক্রিনে যোগ করা
        chat_history.controls.append(
            ft.Row(
                [ft.Container(ft.Text(reply, color=ft.colors.BLACK87), bgcolor=ft.colors.GREY_200, padding=12, border_radius=12)],
                alignment=ft.MainAxisAlignment.START
            )
        )
        page.update()

    user_input = ft.TextField(
        hint_text="Gemini-কে কিছু জিজ্ঞাসা করুন...",
        expand=True,
        border_radius=25,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_700,
        on_submit=send_message
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_750,
        on_click=send_message
    )

    # নিচের ইনপুট বার (একদম জেমিনির মতো বড় ও চওড়া)
    input_bar = ft.Container(
        content=ft.Row([user_input, send_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=10,
        bgcolor=ft.colors.WHITE,
        border_radius=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.BLACK12)
    )

    page.add(
        ft.Row([ft.Text("✨ Gemini AI", weight=ft.FontWeight.BOLD, size=18), voice_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        chat_history,
        input_bar
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
