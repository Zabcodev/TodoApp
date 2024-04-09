import re

task_list = []
status_task = ['Completado', 'Pendiente']


'''--------------------------------------- FUNCIONES DE LA SECCION 1 -> LISTA DE TAREAS ---------------------------------------'''

def completed_task_list():
    completed_list = [task for task in task_list if task['estado'].lower() == status_task[0].lower()]
    print('---------- TAREAS COMPLETADAS ----------')
    print_list(completed_list)
    print('----------------------------------------')

def pending_task_list():
    pending_list = [task for task in task_list if task['estado'].lower() == status_task[1].lower()]
    print('---------- TAREAS PENDIENTES ----------')
    print_list(pending_list)
    print('----------------------------------------')

def print_list(list_task):
    for task in list_task:
        print('-' * 40)
        for key, value in task.items():
            print(f'{key}: {value}')

def list_task_status():
    ejecucion_menu = True
    while ejecucion_menu:
        print('''
---------- LISTA DE TAREAS ----------
1.- Completadas.
2.- Pendientes.
3.- Atras.''')
        opcion_seleccionada = input('Selecciona una opcion: ')
        match(opcion_seleccionada):
            case '1': completed_task_list()
            case '2': pending_task_list()
            case '3': ejecucion_menu = False
            case _: print('Opcion invalida, intente de nuevo.')

'''----------------------------------------------------------------------------------------------------------------------------'''


'''--------------------------------------- FUNCIONES DE LA SECCION 2 -> FILTRAR TAREAS ---------------------------------------'''

def filter_task_by_id():
    verify_id = False
    while not verify_id:
        filter_id = input('Introduce el ID de la tarea a buscar: ')
        verify_id = is_number(filter_id)
    
    tasks_by_id = list(filter(lambda task: task if task['id'] == filter_id else False, task_list))
    if tasks_by_id is not None:
        print_list(tasks_by_id)
    else:
        print('Tarea no econtrada.')

def filter_task_by_title():
    verify_title = False
    while not verify_title:
        filter_title = input('Introduce el titulo de las tareas a filtrar: ')
        verify_title = valid_title(filter_title)
    
    tasks_by_title = list(filter(lambda task: task if filter_title.lower() in task['titulo'].lower() else False, task_list))
    if tasks_by_title is not None:
        print_list(tasks_by_title)
    else:
        print('No se han encontrado tareas que coincidan con el titulo ingresado.')

def filter_task_by_date():
    verify_date = False
    while not verify_date:
        filter_date = input('Introduce la fecha de las tareas a filtrar: ')
        verify_date, mensaje = valid_date(filter_date)
        if mensaje is not None:
            print(mensaje)
    
    tasks_by_date = list(filter(lambda task: task if task['fecha'] == filter_date else False, task_list))
    if tasks_by_date is not None:
        print_list(tasks_by_date)
    else:
        print('No se han encontrado tareas que coincidan con la fecha ingresada.')

def filter_tasks():
    ejecucion_menu = True
    while ejecucion_menu:
        print('''
---------- FILTRAR TAREAS ----------
1.- Filtrar por codigo.
2.- Filtrar por titulo.
3.- Filtrar por fecha.
4.- Atras.''')
        opcion_seleccionada = input('Selecciona una opcion: ')
        match(opcion_seleccionada):
            case '1': filter_task_by_id()
            case '2': filter_task_by_title()
            case '3': filter_task_by_date()
            case '4': ejecucion_menu = False
            case _: print('Opcion invalida, intente de nuevo.')

'''----------------------------------------------------------------------------------------------------------------------------'''

'''---------------------------------------- FUNCIONES DE LA SECCION 3 -> AÑADIR TAREA -----------------------------------------'''

def is_number(check_id):
    return ' '.join(check_id.split()).isdigit()

def id_is_unique(check_id):
    for task in task_list:
        if task['id'] == check_id:
            return False
    return True
    
def valid_id(check_id):
    if not is_number(check_id):
        return False, 'El ID debe ser un digito numerico entero.'
    if not id_is_unique(check_id):
        return False, 'El ID ya esta en uso, ingrese otro diferente.'
    return True, None

def valid_title(title):
    check_title = title.replace(' ', '')
    if len(check_title) <= 0:
        return False, 'El titulo no puede ser vacio.'
    elif len(check_title) > 20:
        return False, 'El titulo de la tarea no debe contener mas de 20 palabras.'
    return True, None

def valid_description(description):
    check_description = description.replace(' ', '')
    if len(check_description) <= 0:
        return False, 'La descripcion no puede estar vacia.'
    return True, None

def valid_status(check_status):
    for status in status_task:
        if status.lower() == check_status.lower():
            return True, None
    return False, 'Estado ingresado no permitido.'


def valid_date(date):
    pattern = r'^(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-\d{4}$'

    if not re.match(pattern, date):
        return False, 'El formato de fecha ingresado es invalido.'
    
    day, month, year = map(int, date.split('-'))

    if day > 31:
        return False, 'Dia invalido.'
    if month > 12:
        return False, 'Mes invalido.'
    if year < 0 or year > 9999:
        return False, 'Año invalido.'
    return True, None

def add_task():
    verify_id = False
    while not verify_id:
        id = input('ID Tarea: ')
        verify_id, mensaje = valid_id(id)
        if mensaje is not None:
            print(mensaje)

    verify_title = False
    while not verify_title:
        title = input('Titulo de la tarea: ')
        verify_title, mensaje = valid_title(title)
        if mensaje is not None:
            print(mensaje)

    verify_description = False
    while not verify_description:
        description = input('Descripcion de la tarea: ')
        verify_description, mensaje = valid_description(description)
        if mensaje is not None:
            print(mensaje)

    verify_status = False
    while not verify_status:
        status = input('Estado de la tarea: ')
        verify_status, mensaje = valid_status(status)
        if mensaje is not None:
            print(mensaje)

    verify_date = False
    while not verify_date:
        date_creation = input('Fecha de creacion (DD-MM-YYYY): ')
        verify_date, mensaje = valid_date(date_creation)
        if mensaje is not None:
            print(mensaje)

    task = {
        'id': id,
        'titulo': title,
        'descripcion': description,
        'estado': status,
        'fecha': date_creation
    }

    task_list.append(task)
    print('Tarea añadida exitosamente.')

'''----------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------- FUNCIONES DE LA SECCION 4 -> ACTUALIZAR TAREA --------------------------------------'''

def task_to_update(task_id, task_key_update, new_value):
    for task in task_list:
        if task['id'] == task_id:
            task[task_key_update] = new_value
            break

def verify_task_exist(id_task_to_update):
    if len(task_list) > 0:
        for task in task_list:
            if task['id'] == id_task_to_update:
                return True, 'Tarea encontrada'
        return False, 'Tarea no encontrada, introduce nuevamente el id de la tarea.'
    return False

def update_task_id(task_id):
    print('---------- ACTUALIZAR CODIGO TAREA ----------')
    verify_new_id = False
    while not verify_new_id:
        new_id = input('Introduce el nuevo codigo de la tarea: ')
        verify_new_id, mensaje = valid_id(new_id)
        if mensaje is not None:
            print(mensaje)
    map(task_to_update(task_id, 'id', new_id), task_list)
    print('El codigo (ID) de la tarea ha sido actualizado exitosamente.')

def update_task_title(task_id):
    print('---------- ACTUALIZAR TITULO TAREA ----------')
    verify_new_title = False
    while not verify_new_title:
        new_title = input('Introduce el nuevo titulo de la tarea: ')
        verify_new_title, mensaje = valid_title(new_title)
        if mensaje is not None:
            print(mensaje)
    map(task_to_update(task_id, 'titulo', new_title), task_list)
    print('El titulo de la tarea ha sido actualizado exitosamente')

def update_task_description(task_id):
    print('---------- ACTUALIZAR DESCRIPCION TAREA ----------')
    verify_new_description = False
    while not verify_new_description:
        new_description = input('Introduce la nueva descripcion de la tarea: ')
        verify_new_description, mensaje = valid_description(new_description)
        if mensaje is not None:
            print(mensaje)
    map(task_to_update(task_id, 'descripcion', new_description), task_list)
    print('La descripcion de la tarea ha sido actualizado exitosamente')

def update_task_status(task_id):
    print('---------- ACTUALIZAR STATUS TAREA ----------')
    verify_new_status = False
    while not verify_new_status:
        new_status = input('Introduce el nuevo status de la tarea: ')
        verify_new_status, mensaje = valid_status(new_status)
        if mensaje is not None:
            print(mensaje)
    map(task_to_update(task_id, 'estado', new_status), task_list)
    print('El estado de la tarea ha sido actualizado exitosamente')

def update_task_date(task_id):
    print('---------- ACTUALIZAR FECHA TAREA ----------')
    verify_new_date = False
    while not verify_new_date:
        new_date = input('Introduce la nueva fecha de la tarea: ')
        verify_new_date, mensaje = valid_date(new_date)
        if mensaje is not None:
            print(mensaje)
    map(task_to_update(task_id, 'fecha', new_date), task_list)
    print('La fecha de la tarea ha sido actualizado exitosamente')

def menu_update_task(task_id, message):
    print(message)
    ejecucion_menu = True
    while ejecucion_menu:
        print('-' * 50)
        print('1.- Actualizar codigo.')
        print('2.- Actualizar titulo.')
        print('3.- Actualizar descripcion.')
        print('4.- Actualizar status.')
        print('5.- Actualizar fecha.')
        print('6.- Atras.')
        opcion_seleccionada = input('Seleccione una opcion: ')
        match(opcion_seleccionada):
            case '1': update_task_id(task_id)
            case '2': update_task_title(task_id)
            case '3': update_task_description(task_id)
            case '4': update_task_status(task_id)
            case '5': update_task_date(task_id)
            case '6': 
                ejecucion_menu = False
            case _: print('Opcion invalida, intente de nuevo.')

def update_task():
    print('-' * 10, 'ACTUALIZAR TAREA', '-' * 10)
    verify_id = False
    verify_task = False
    message_exist = ''
    while not verify_id and not verify_task:
        id_task_to_update = input("Introduce el codigo (ID) de la tarea a actualizar: ")
        verify_id = is_number(id_task_to_update)
        verify_task, message_exist = verify_task_exist(id_task_to_update)
        if not verify_task:
            verify_id = False
            print(message_exist)
    print('-' * 50)
    menu_update_task(id_task_to_update, message_exist)
    print('-' * 50)
'''----------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------- FUNCIONES DE LA SECCION 5 -> ELIMINAR TAREA ----------------------------------------'''

def delete_task():
    verify_id = False
    while not verify_id:
        id_task_delete = input('Introduce el ID de la tarea a eliminar: ')
        verify_id = is_number(id_task_delete)

    deleted_task = False
    for task in task_list:
        if task['id'] == id_task_delete:
            task_list.pop(task_list.index(task))
            deleted_task = True
            break

    if deleted_task:
        print('Tarea eliminada exitosamente')
    else:
        print('Tarea no encontrada, intentelo de nuevo')

'''-----------------------------------------------------------------------------------------------------------------------------'''

'''------------------------------------- FUNCION DE LA SECCION 6 -> SALIR DE LA APLICACION -------------------------------------'''

def close_app():
    exit(1)

'''----------------------------------------------------------------------------------------------------------------------------'''

'''---------------------------------------- MENU PRINCIPAL DE LA APLICACION DE TAREAS -----------------------------------------'''
def task_app():
    while True:
        print('''
---------- APLICACION DE TAREAS ----------
1.- Lista de tareas.
2.- Filtrar tareas.
3.- Añadir tarea.
4.- Actualizar tarea.
5.- Eliminar tarea.
6.- Salir.''')
        opcion_seleccionada = input('Selecciona una opcion: ')
        match(opcion_seleccionada):
            case '1': list_task_status()
            case '2': filter_tasks()
            case '3': add_task()
            case '4': update_task()
            case '5': delete_task()
            case '6': close_app()
            case _: print('Opcion invalida, intente de nuevo.')

'''----------------------------------------------------------------------------------------------------------------------------'''

# Inicio de la ejecucion del programa
task_app()