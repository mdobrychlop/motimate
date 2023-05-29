from todoist_api_python.api import TodoistAPI

# Probably a Project class is needed. This class should store all info regarding tasks and comments.
# The class should also contain methods for figuring out the info of what is completed, past, future etc.

class Todoist_Content():
    def __init__(self):
        self.apikey = self.parse_config()
        self.api = TodoistAPI(self.apikey)
    def parse_config(self):
        try:
            with open('apikeys.txt', 'r') as f:
                for line in f.readlines():
                    if line.startswith('todoist'):
                        return line.split(':')[1].strip()
        except Exception as e:
            print(e)
            return None
    def get_tasks_sync(self):
        try:
            tasks = self.api.get_tasks()
            return tasks
        except Exception as error:
            print(error) 
            return None
    def get_projects_sync(self):
        try:
            projects = self.api.get_projects()
            return projects
        except Exception as error:
            print(error) 
            return None
    def get_comments_for_project(self, project_id):
        try:
            comments = self.api.get_comments(project_id=project_id)
            return comments
        except Exception as error:
            print(error)
            return None





if __name__ == '__main__':
    todoist_content = Todoist_Content()
    tasklist = todoist_content.get_tasks_sync()
    for t in tasklist:
        # create a separate list of tasks for each project
        print(t)
    projectlist = todoist_content.get_projects_sync()
    for p in projectlist:  
        if p.comment_count > 0:
            pid = p.id
            print(pid)
            commentlist = todoist_content.get_comments_for_project(pid)
            print(commentlist)

    


"""
# task data:
[Task(assignee_id=None, assigner_id=None, comment_count=0, is_completed=False, content='Placeholders for unit tests', created_at='2023-05-29T13:46:50.018688Z', creator_id='15578057', description='Create placeholder unit tests in the 
repository.', due=None, id='6919257518', labels=[], order=1, parent_id=None, priority=1, project_id='2313142145', section_id=None, url='https://todoist.com/showTask?id=6919257518', sync_id=None)]

"""