import flet as ft

class LeftContainer(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.page = kwargs.get("page")
        self.selected_index = None
        self.col = {
            "xs": 0,
            "sm": 3,
            "md": 3,
            "xl": 3,
        }
        self.border_radius = 0
        self.bgcolor = ft.colors.RED

        # Initialize the FilePicker
        self.file_picker = ft.FilePicker(on_result=self.pick_files_result)

        self.content = ft.NavigationRail(
            bgcolor=ft.colors.RED,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True,
            height=800,

            destinations=[
                ft.NavigationRailDestination(
                    padding=5,
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label="File",
                ),
                
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.LOGOUT_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.LOGOUT),
                    label="LOGOUT",
                ),
            ],
            on_change=self.on_nav_change,
        )
        
        self.controls = [self.content]

    def on_nav_change(self, e):
        self.selected_index = e.control.selected_index
        if self.selected_index == 0:
            # Trigger the file picker to select a directory when the "File" destination is selected
            self.file_picker.get_directory_path()

    def pick_files_result(self, e):
        if e.files:
            directory_path = e.files[0].path
            print(f"Selected directory: {directory_path}")

# Example usage
def main(page: ft.Page):
    left_container = LeftContainer(page=page)
    page.add(left_container)
    
    # Add the FilePicker to the page
    page.overlay.append(left_container.file_picker)
    page.update()

ft.app(target=main)

