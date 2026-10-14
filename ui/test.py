from database import insert_item
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
        ui.button("Insert", on_click=lambda:show_insert(content)).classes("flex-1 justify-center")
        ui.button("Delete", on_click=lambda:show_delete(content)).classes("flex-1 justify-center")
        ui.button("Select", on_click=lambda:show_select(content)).classes("flex-1 justify-center")
    # ui.separator()



def show_insert(content):
    content.clear()

    with content:
        ui.label("New card for item").classes("text-2xl")
        name = ui.input("Название товара").value
        category = ui.input("Категория").value
        unit = ui.number("Количество")
        critical_balance = ui.number("Критичный баланс")
        if  ui.button("Сохранить"):
            insert_item(name,category,unit,critical_balance)
            print("Вызвана функция insert с параметрами",name,category,unit,critical_balance)


def show_delete(content):
    content.clear()

    with content:
        ui.label("Delete item").classes("text-2xl")


def show_select(content):
    content.clear()

    with content:
        ui.label("Select item").classes("text-2xl")

ui.run(root)          
