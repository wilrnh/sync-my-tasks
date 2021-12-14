"""
    AsanaProvider interfaces with Asana API
"""
import asana
from sync_my_tasks.tasklist import TaskList
from sync_my_tasks.task import Task
from datetime import datetime


class AsanaProvider:

    def __init__(self, api_token: str, workspace_name: str) -> None:
        # Set up the Asana client
        self.client = asana.Client.access_token(api_token)
        # Get the current user, mostly for the user ID and workspace list
        self.user = self.client.users.me()

        # Set the workspace
        for workspace in self.user['workspaces']:
            if workspace['name'] == workspace_name:
                self.workspace = workspace

        # Initialize the projects list that will be exported
        self.projects = []

        # Get the My Tasks project
        my_tasks = self.client.user_task_lists.get_user_task_list_for_user(
            self.user['gid'], {'workspace': self.workspace['gid']})
        my_tasks_project = self.client.projects.get_project(my_tasks['gid'])

        # Add My Tasks to the projects list
        self.projects.append(my_tasks_project)

        # Get all projects
        for workspace_project in self.client.projects.get_projects_for_workspace(self.workspace.get('gid')):
            self.projects.append(
                self.client.projects.get_project(workspace_project.get('gid'))
            )

        # Let the user know which account and workspace they connected
        print('Connected to Asana as ' +
              self.user['name'] + ' in workspace ' + self.workspace['name'])

    # Export a list of TaskLists
    def export_tasks(self) -> list[TaskList]:
        # The fields that should be returned when getting tasks/subtasks
        TASK_FIELDS = 'name,assignee,created_at,completed_at,due_on,html_notes,projects,num_subtasks'
        # Initialize the return list
        task_lists = []

        # Get all the projects that should be exported
        for project in self.projects:
            # Get all sections in project
            for section in self.client.sections.get_sections_for_project(project['gid']):
                # Create TaskList for each section
                task_list = TaskList(project['name'] + ' - ' + section['name'])
                # Get tasks for each section
                for task in self.client.tasks.get_tasks_for_section(section['gid'], {'opt_fields': TASK_FIELDS}):
                    # Skip empty tasks
                    if task.get('name').strip() == '':
                        continue

                    # Get task created date
                    task_created_at = datetime.fromisoformat(
                        task.get('created_at').replace('Z', '+00:00'))
                    # Get task completed date
                    if task.get('completed_at') != None:
                        task_completed_at = datetime.fromisoformat(
                            task.get('completed_at').replace('Z', '+00:00'))
                    else:
                        task_completed_at = None

                    # Get task due date
                    if task.get('due_on') != None:
                        task_due_on = datetime.fromisoformat(
                            task.get('due_on'))
                    else:
                        task_due_on = None

                    # Handle subtasks if they exist
                    if task['num_subtasks'] > 0:
                        # Create a TaskList for each subtask
                        subtasks_list = TaskList('Subtasks')
                        # Get all the subtasks
                        for subtask in self.client.tasks.get_subtasks_for_task(task['gid'], {'opt_fields': TASK_FIELDS}):
                            # Skip empty subtasks
                            if subtask.get('name').strip() == '':
                                continue

                            # Get subtask created date
                            subtask_created_at = datetime.fromisoformat(
                                subtask.get('created_at').replace('Z', '+00:00'))
                            # Get subtask completed date
                            if subtask.get('completed_at') != None:
                                subtask_completed_at = datetime.fromisoformat(
                                    subtask.get('completed_at').replace('Z', '+00:00'))
                            else:
                                subtask_completed_at = None
                            # Create a Task for the subtask
                            subtask_task = Task(
                                id=subtask['gid'],
                                title=subtask['name'],
                                description=subtask['html_notes'],
                                created=subtask_created_at,
                                completed=subtask_completed_at,
                                subtasks=None
                            )
                            # Append the subtask to the subtask TaskList
                            subtasks_list.add(subtask_task)
                    else:
                        subtasks_list = None

                    # Collect all comments into the description
                    task_comments = []
                    for story in self.client.stories.get_stories_for_task(task['gid']):
                        if story.get('type') != 'comment':
                            continue

                        task_comments.append(
                            '<li>' + story.get('text') + '</li>')
                    if len(task_comments) > 0:
                        task['html_notes'] += 'Comments: <ul>' + \
                            ''.join(task_comments) + '</ul>'

                    # Create the Task
                    tasklist_task = Task(
                        id=task['gid'],
                        title=task['name'],
                        description=task['html_notes'],
                        created=task_created_at,
                        completed=task_completed_at,
                        due=task_due_on,
                        subtasks=subtasks_list
                    )
                    # Append the Task to the TaskList
                    task_list.add(tasklist_task)
                # Let the user know the progress
                print('Imported ' + str(len(task_list.task_list)) +
                      ' tasks into ' + task_list.name)
                # Append the TaskList to the return list
                task_lists.append(task_list)
        # Return the TaskLists
        return task_lists
