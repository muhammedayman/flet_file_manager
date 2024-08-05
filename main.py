import flet as ft

from home import HomePage




DIRECTORIES={
    "IMAGES":[".jpg",".png",".jpeg",".webp",".svg"],
    "VIDEOS":[".avi",".mp4",".mkv",".mpg","webm"]
}

def main(page:ft.Page):
    page.path=None
    home_page=HomePage(page=page)
    page.add(
        ft.AppBar(
            title=ft.Text("File manager app"),
            bgcolor="blue"
        ),
        home_page
    )

ft.app(target=main)