import argparse
import json
import os
from datetime import datetime

document_path = os.path.join(os.path.expanduser('~'), 'Documents')
file_name = os.path.join(document_path, 'task_file.json')
status_selection = ['todo', 'in-progress', 'done']


def load_contacts():
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    return {}


def save_task(task):
    if not os.path.exists(document_path):
        os.makedirs(file_name)
    with open(file_name, 'w') as file:
        json.dump(task, file, indent=4)


def add_new_task(description):
    task = load_contacts()
    task_key = list(task.keys())
    task_key = [int(key) for key in task_key]
    index_key = max(task_key) + 1 if task_key else 1
    new_task = TaskManager(index_key, description)
    task[index_key] = {'description': new_task.description, 'status': new_task.status, 'createdAt': new_task.createdAt,
                       'updatedAt': new_task.updatedAt}
    save_task(task)


def update_task(the_id, the_description=False):
    try:
        the_id = int(the_id)
    except ValueError:
        print("Veuillez s'il vous plait saisir un nombre entier supérieur à zéro")
    task = load_contacts()
    the_id = str(the_id)
    if the_id not in task:
        print(f"Aucune tâche avec cet ID.")
    else:
        if the_description:
            task[the_id]['description'] = the_description
            task[the_id]['updatedAt'] = datetime.now().strftime("%d%m%Y")
            save_task(task)


def delete_task(the_id):
    try:
        the_id = int(the_id)
    except ValueError:
        print("Veuillez s'il vous plait saisir un nombre entier supérieur à zéro")
    task = load_contacts()
    the_id = str(the_id)
    if the_id not in task:
        print(f"Aucune tâche avec cet ID.")
    else:
        del task[the_id]
        save_task(task)


def mark_in_progress(the_id):
    try:
        the_id = int(the_id)
    except ValueError:
        print("Veuillez s'il vous plait saisir un nombre entier supérieur à zéro")
    task = load_contacts()
    the_id = str(the_id)
    if str(the_id) not in task:
        print(f"Aucune tâche avec cet ID.")
    else:
        task[the_id]['status'] = 'in-progress'
        task[the_id]['updatedAt'] = datetime.now().strftime("%d%m%Y")
        save_task(task)


def mark_done(the_id):
    try:
        the_id = int(the_id)
    except ValueError:
        print("Veuillez s'il vous plait saisir un nombre entier supérieur à zéro")
    task = load_contacts()
    the_id = str(the_id)
    if str(the_id) not in task:
        print(f"Aucune tâche avec cet ID.")
    else:
        task[the_id]['status'] = 'done'
        task[the_id]['updatedAt'] = datetime.now().strftime("%d%m%Y")
        save_task(task)


def task_list(status=None):
    task = load_contacts()
    if not status:
        for key, value in task.items():
            if value['status'] == 'done':
                status = 'Done'
            elif value['status'] == 'todo':
                status = 'To Do'
            else:
                status = "In Progress"
            print(
                f"Tâche {key}: \n\t\t Description: {value['description']} \n\t\t Status: {status} \n\t\t "
                f"Créé le: {value['createdAt']} \n\t\t Mise à jour le: {value['updatedAt']}")
    elif status == 'done':
        for key, value in task.items():
            if value['status'] == 'done':
                print(
                    f"Tâche {key}: \n\t\t Description: {value['description']} \n\t\t Status: Done \n\t\t "
                    f"Créé le: {value['createdAt']} \n\t\t Mise à jour le: {value['updatedAt']}")
    elif status == 'in-progress':
        for key, value in task.items():
            if value['status'] == 'in-progress':
                print(
                    f"Tâche {key}: \n\t\t Description: {value['description']} \n\t\t Status: In progress \n\t\t "
                    f"Créé le: {value['createdAt']} \n\t\t Mise à jour le: {value['updatedAt']}")
    elif status == 'todo':
        for key, value in task.items():
            if value['status'] == 'todo':
                print(
                    f"Tâche {key}: \n\t\t Description: {value['description']} \n\t\t Status: To Do \n\t\t "
                    f"Créé le: {value['createdAt']} \n\t\t Mise à jour le: {value['updatedAt']}")


class TaskManager:
    def __init__(self, the_id, description):
        self.id = the_id
        self.description = description
        self.status = 'todo'
        self.createdAt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.updatedAt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâche CLI.")
    subparsers = parser.add_subparsers(dest='command')

    # Sous-commande pour ajouter un tâche
    add_parser = subparsers.add_parser('add', help='Ajouter un tâche.')
    add_parser.add_argument('description', type=str, help='Description de la tâche.')

    # Sous-commande pour modifier la description une tâche
    update_parser = subparsers.add_parser('update', help='Lister tous les contacts.')
    update_parser.add_argument('id', help="ID de la tâche")
    update_parser.add_argument('description', type=str, help='Description de la tâche.')

    # Sous-commande pour supprimer une tâche
    delete_parser = subparsers.add_parser('delete', help='Supprimer une tâche')
    delete_parser.add_argument('id', help="ID de la tâche")

    # Sous-commande pour modifier le status d'une tâche à in-progress
    mark_in_progress_parser = subparsers.add_parser('mark-in-progress',
                                                    help='Changer le status de la tâche à \'in-progress\'')
    mark_in_progress_parser.add_argument('id', help="ID de la tâche")

    # Sous-commande pour modifier le status d'une tâche à done
    mark_done_parser = subparsers.add_parser('mark-done',
                                             help='Changer le status de la tâche à \'done\'')
    mark_done_parser.add_argument('id', help="ID de la tâche")

    # Sous-commande pour afficher toutes les tâches ou celles en status done ou in-progress ou todo
    list_parser = subparsers.add_parser('list',
                                        help='Lister toutes les tâches ou celles en status \'done ou in-progress ou '
                                             'todo\'.')
    list_parser.add_argument('status', nargs="?", default=None, help="Status de la tâche")

    args = parser.parse_args()

    if args.command == 'add':
        add_new_task(args.description)
    elif args.command == 'update':
        update_task(args.id, args.description)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'mark-in-progress':
        mark_in_progress(args.id)
    elif args.command == 'mark-done':
        mark_done(args.id)
    elif args.command == 'list':
        task_list(args.status)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
