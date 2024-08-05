from typing import Any, List, Optional, Callable
import flet as ft
import os

class Header(ft.Container):
    def __init__(self,*args,**kwargs):
        super().__init__()
        # create a dt attribute
        self.height=200
        self.width=200
        self.name = ft.Text("Files")
        self.avatar = ft.IconButton("person")

        # compile the attributes inside the header contianer
        self.content = ft.Row(
            alignment="spaceBetween", controls=[self.name,self.avatar]
        )

class folderCol(ft.Column):
    def __init__(self,*args,**kwargs):
        super().__init__() 
class FolderButton(ft.IconButton):
    def __init__(self,*args,**kwargs):
        super().__init__()    
        self.icon=ft.icons.ARROW_RIGHT
        


class LeftContianer(ft.Container):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.page=kwargs.get("page")
        self.selected_index=None
        self.col={
            "xs":0,
            "sm": 3,
            "md": 3,
            "xl": 3,
        }
        self.border_radius=0
        self.bgcolor=ft.colors.RED
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        folder_col=folderCol()
        button=FolderButton()
        button.on_click=self.add_folder
        button.data="aymen"
        folder_col.controls.append(button)
        if self.page.path:
            self.content=ft.ExpansionTile(
                title=ft.Text("hello"),
                controls=[
                    ft.ExpansionTile(
                        title=ft.Text("hi"),
                        controls=[
                            ft.ExpansionTile(
                                title=ft.Text("hi"),
                                controls=[
                                    
                                ]
                            )
                        ]
                    )
                ]
            )
        else:
            self.content=button

    def add_folder(self,e):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.pick_files_dialog.get_directory_path()
    def pick_files_result(self,e: ft.FilePickerResultEvent):
        path=e.path
        self.page.path=path

        expansion_tiles = self.create_expansion_tile(path)
        self.content = ft.ExpansionTile(

            title=ft.Text(e.path),
            controls=expansion_tiles
        )
        self.list_folders_recursively(e.path)
        self.page.update()
    def create_expansion_tile(self,path):
        items = os.listdir(path)
        tiles = []

        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tiles.append(
                    ft.ExpansionTile(
                        title=ft.Text(item),
                        controls=self.create_expansion_tile(item_path)
                        
                    )
                )
            else:
                tiles.append(ft.Text(item))
        
        return tiles
    def list_folders_recursively(self,path, level=0):
        try:
            items = os.listdir(path)
        except PermissionError:
            print(f"{' ' * level * 2}Permission denied: {path}")
            return

        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                
                print(f"{' ' * level * 2}Folder: {item}")
                self.list_folders_recursively(item_path, level + 1)
            else:
                print(f"{' ' * level * 2}File: {item}")
                
    def on_nav_change(self, e):
        self.selected_index = e.control.selected_index
        if self.selected_index == 0: 
            print("0")
        elif self.selected_index == 1:
            pass
        elif self.selected_index == 2:
            pass
        self.page.update()

        


class RightContianer(ft.Column):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.scroll="auto"
        self.col={
            "xs":12,
            "sm": 9,
            "md": 9,
            "xl": 9,
        }
        self.controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                            scroll="auto",
                            controls=[
                                    ft.Container(
                                    height=800,
                                    border_radius=10,
                                    padding=ft.padding.only(top=50,bottom=50,),
                                    bgcolor=ft.colors.WHITE,
                                ),
            
                            ]
                    ),
            
                ]
            ),
            
        ]
                


class MainResponsiveContainer(ft.ResponsiveRow):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.page=kwargs.get("page")
        left_c=LeftContianer(page=self.page)
        right_c=RightContianer()
        self.controls=[
            left_c,
            right_c
                       ]
        self.page.update()

class HomePage(ft.Container):

    def __init__(self,*args,**kwargs):
        super().__init__()
        self.expand=True
        self.content=MainResponsiveContainer(page=kwargs.get("page"))

