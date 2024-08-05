import os
import flet as ft
# import boto3

# Initialize S3 client
# s3_client = boto3.client('s3')

# Function to upload file to S3
def upload_file_to_s3(file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        return True
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")
        return False

# Function to get file details
def get_file_details(path):
    return {
        'name': os.path.basename(path),
        'size': os.path.getsize(path),
        'extension': os.path.splitext(path)[1]
    }

# Function to list files in directory
def list_files_in_directory(directory, file_extension_filter=None):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if not file_extension_filter or filename.endswith(file_extension_filter):
                file_path = os.path.join(root, filename)
                file_details = get_file_details(file_path)
                files.append(file_details)
    return files

# Initialize Flet app
def main(page: ft.Page):
    page.title = "File Manager App"

    # Define UI elements
    directory_list = ft.ListView()
    file_details_container = ft.Column()

    # Populate directory list
    def populate_directory_list():
        root_dir = "."  # Change this to the desired root directory
        for root, dirs, files in os.walk(root_dir):
            for name in dirs:
                print(name)
                directory_list.controls.append(ft.TextButton(text=name, on_click=lambda e: on_directory_selected(e, os.path.join(root, name))))
            break  # Only show the first level for simplicity

    # Populate file details
    def populate_file_details(directory, file_extension_filter=None):
        files = list_files_in_directory(directory, file_extension_filter)
        file_details_container.controls.clear()
        for file in files:
            file_details_container.controls.append(ft.ListTile(
                leading=ft.Icon(ft.icons.FILE_PRESENT),
                title=ft.Text(file['name']),
                subtitle=ft.Text(f"{file['size']} bytes, {file['extension']}"),
                trailing=ft.Icon(ft.icons.CHECK_CIRCLE if file.get('uploaded') else ft.icons.CHECK_CIRCLE_OUTLINE)
            ))
        page.update()

    # Event handlers
    def on_directory_selected(e, directory):
        populate_file_details(directory)

    def on_file_filter_changed(e):
        selected_filter = e.control.value
        populate_file_details(selected_directory, selected_filter)

    def on_upload_button_click(e):
        selected_files = []  # Implement logic to get selected files
        for file in selected_files:
            upload_file_to_s3(file['path'], 'your-s3-bucket', file['name'])
            file['uploaded'] = True  # Update the file status
        populate_file_details(selected_directory)
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
           e.path if e.path else "Cancelled!"
        )
        selected_files.update()
        populate_file_details(e.path)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)
    # Layout
    page.add(
        ft.AppBar(
            title=ft.Text("File manager app"),
            bgcolor="blue"
        ),
        ft.Row(
            width=300,
            height=300,
            controls=
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.get_directory_path(
                        dialog_title="select folder"
                    ),
                ),
                selected_files,
            
            # ft.Column(controls=[directory_list]),
            # ft.Column(controls=[file_details_container])
        ])
    )

    # Populate initial data
    populate_directory_list()

# Run Flet app
ft.app(target=main)
