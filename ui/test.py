# from database.repository import insert_item,select_item,delete_item
from nicegui import ui
def root():
    ui.dark_mode().enable()

    # ui.label("📦").classes("text-4xl font-bold")

    ui.page_title("CRM-склад")
    ui.label("CRM").classes("text-4xl font-bold w-full text-center")
    ui.label("Управление карточками товара").classes("w-full text-center")
    
    ui.separator()
    
    ###Создание 3 кнопок 
    content = ui.column()
    with ui.row().classes("w-full justify-center"):
        ui.button("Save", on_click=lambda:button_insert(content)).classes("flex-1 justify-center")
        ui.button("Delete", on_click=lambda:button_delete(content)).classes("flex-1 justify-center")
        ui.button("Select", on_click=lambda:button_select(content)).classes("flex-1 justify-center")


def button_insert(content):
    content.clear()

    with content:
        ui.label("New card for item").classes("text-2xl")
        name = ui.input("Название товара").value
        category = ui.input("Категория").value
        unit = ui.number("Количество")
        critical_balance = ui.number("Критичный баланс")
        # if  ui.button("Save"):
            # insert_item(name,category,unit,critical_balance)
            # print("Вызвана функция insert с параметрами",name,category,unit,critical_balance)


def button_delete(content):
    content.clear()

    with content:
        ui.label("Delete item").classes("text-2xl")
        id = ui.input("Id товара").value
        # if ui.button("Delete"):
            # delete_item(id)
            # print("Вызвана функция delete_item c параметром",id)

def button_select(content):
    content.clear()

    with content:
        ui.label("Select item").classes("text-2xl")
        form = ui.input("Form").value
        data = ui.input("Data").value
        # if ui.button("Select"):
            # select_item(form,data)
            # print("Вызвана функция select с параметрами", form,data)

ui.run(root)          
