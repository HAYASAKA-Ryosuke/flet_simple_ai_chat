import flet as ft
from ai_chat import AiChat


async def main(page: ft.Page):
    ai_chat = AiChat()
    page.title = "SIMPLE CHAT UI"
    page.vertical_alignment = ft.MainAxisAlignment.END
    messages = []

    async def send_message(e):
        messages.append(generate_chat_message_ui(input_text_field.value))
        messages.append(generate_chat_message_ui('waiting ...', 'AI'))
        message = input_text_field.value
        input_text_field.value = ''
        await send_message_to_ai(message, len(messages))

    input_text_field = ft.TextField(value="", hint_text="Write a message...", multiline=True, expand=True)

    def generate_chat_message_ui(message: str, user_name="YOU"):
        return ft.Row(
            [
                ft.CircleAvatar(
                    content=ft.Text(user_name),
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN if user_name == "YOU" else ft.colors.BLUE,
                ),
                ft.Column(
                    [
                        ft.Text(user_name, weight="bold"),
                        ft.Text(message, selectable=True)
                    ],
                    tight=True,
                    spacing=5,
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    async def send_message_to_ai(message: str, index: int):
        text = ''
        await columns.update_async()
        await page.update_async()
        async for response in ai_chat.send(message):
            text += response
            messages[index - 1] = generate_chat_message_ui(text, 'AI')
            columns.controls = update_column_items()
            await columns.update_async()
        await page.update_async()
 
    def update_column_items():
        items = []

        for message in messages:
            items.append(message)

        items.append(
            ft.Row(
                [
                    input_text_field,
                    ft.IconButton(
                      icon=ft.icons.SEND_ROUNDED,
                      tooltip="Send message",
                      on_click=send_message,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        return items

    columns = ft.Column(
        controls=update_column_items(),
        alignment=ft.MainAxisAlignment.CENTER,
    )

    await page.add_async(
        columns
    )

ft.app(target=main)
