"""
    MsTodoProvider interfaces with Microsoft To-Do API
"""

from msal import PublicClientApplication
import requests
from sync_my_tasks.task import Task
from sync_my_tasks.tasklist import TaskList


class MsTodoProvider():

    def __init__(self) -> None:
        # Set up an MSAL app; anyone can register and use an Azure app and use it's client ID here
        msal_app = PublicClientApplication(
            '6783665b-4d9b-485d-85df-a3478f6959f5')
        # Get an MSAL token with read/write permissions for Tasks
        self.msal_token = msal_app.acquire_token_interactive(
            scopes=['User.read,Tasks.ReadWrite'])

        if 'access_token' in self.msal_token:
            # Let the user know which account they connected
            print('Connected to Microsoft To-Do as ' +
                  self.msal_token.get('id_token_claims').get('preferred_username'))
        else:
            print('Got an error connecting to Microsoft To-Do: ' +
                  self.msal_token.get('error_description'))

    # Import a list of TaskLists
    def import_tasks(self, task_lists: list[TaskList]):
        # Get each TaskList
        for task_list in task_lists:
            # Create a MS To-Do List to import tasks into
            mstodo_tasklist_body = {'displayName': task_list.name}
            mstodo_tasklist_resp = requests.post('https://graph.microsoft.com/v1.0/me/todo/lists', json=mstodo_tasklist_body, headers={
                                                 'Authorization': 'Bearer ' + self.msal_token.get('access_token')})
            mstodo_tasklist_resp.raise_for_status()
            mstodo_tasklist = mstodo_tasklist_resp.json()
            
            # Import all Tasks in the TaskList into the MS To-Do List
            for task in task_list.task_list:
                # Initialize the task that will be added to MS To-Do
                mstodo_task_body = {}
                
                # Add the task title
                mstodo_task_body.update({
                    'title': task.task_title
                })

                # Set the status if completed
                if task.task_completed != None:
                    mstodo_task_body.update({
                        'status': 'completed'
                    })
                
                # Add the task due date
                if task.task_due != None:
                    mstodo_task_body.update({'dueDateTime': {
                        'dateTime': task.task_due.isoformat(),
                        'timeZone': 'Etc/GMT'
                    }})
                
                # MS To-Do does not support subtasks in the API so collect all the subtasks into the description
                if task.task_subtasks != None:
                    subtasks_html = 'Subtasks: <ul>'
                    for subtask in task.task_subtasks.task_list:
                        subtasks_html += f'<li>{subtask.task_title}: {subtask.task_description}</li>'
                    subtasks_html += '</ul>'

                    task.task_description += subtasks_html

                # MS To-Do does not expose created/completed dates in UI, so add to description
                task.task_description += f'History: <ul><li>Created: {task.task_created.isoformat()}</li>'
                if task.task_completed != None:
                    task.task_description += f'<li>Completed: {task.task_completed.isoformat()}</li>'
                task.task_description += '</ul>'

                # Add the task description
                mstodo_task_body.update({'body': {
                    'content': task.task_description,
                    'contentType': 'html'
                }})
                
                # Add the task to MS To-Do
                mstodo_task_resp = requests.post('https://graph.microsoft.com/v1.0/me/todo/lists/' + mstodo_tasklist.get(
                    'id') + '/tasks', json=mstodo_task_body, headers={'Authorization': 'Bearer ' + self.msal_token.get('access_token')})
                mstodo_task_resp.raise_for_status()
