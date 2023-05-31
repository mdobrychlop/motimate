from todoist_api_python.api import TodoistAPI
import datetime

# Probably a Project class is needed. This class should store all info regarding tasks and comments.
# The class should also contain methods for figuring out the info of what is completed, past, future etc.

class TodoistProject():
    def __init__(self, project_object, tasks, comments):
        po = project_object
        self.project_id = po.id
        self.project_name = po.name
        self.tasks = tasks
        self.comments = comments     
        self.uncompleted_tasks_with_no_due_date = []
        self.tasks_for_today = []
        self.completed_tasks_yesterday = []
        self.failed_tasks_yesterday = []
        self.task_count = len(self.tasks)
        self.categorize_tasks()
        self.prompt_input = self.create_prompt_input() 
        
    def categorize_tasks(self):
        todays_date = datetime.datetime.now()
        yesterdays_date = todays_date - datetime.timedelta(days=1)

        today = str(todays_date.date())
        yesterday = str(yesterdays_date.date())

        for task in self.tasks:
            if task.is_completed:
                if task.due is not None:
                    if str(task.due.date) == yesterday:
                        self.completed_tasks_yesterday.append(task)
            else:
                if task.due is not None:
                    if str(task.due.date) == yesterday:
                        self.failed_tasks_yesterday.append(task)
                    if str(task.due.date) == today:
                        self.tasks_for_today.append(task)
                else:
                    self.uncompleted_tasks_with_no_due_date.append(task)

    def create_prompt_input(self):
        prompt_input = "Project: {}\n".format(self.project_name)
        prompt_input += "Comments (project context):\n"
        for comment in self.comments:
            prompt_input += comment.content + "\n"
        prompt_input += "Tasks completed yesterday: " + str(len(self.completed_tasks_yesterday)) + "\n"
        for task in self.completed_tasks_yesterday:
            prompt_input += "- " + task.content + "\n"
        prompt_input += "Tasks due yesterday but not completed: " + str(len(self.failed_tasks_yesterday)) + "\n"
        for task in self.failed_tasks_yesterday:
            prompt_input += "- " + task.content + "\n"
        prompt_input += "Tasks due today: " + str(len(self.tasks_for_today)) + "\n"
        for task in self.tasks_for_today:
            prompt_input += "- " + task.content + "\n"
        prompt_input += "Uncompleted tasks with no due date: " + str(len(self.uncompleted_tasks_with_no_due_date)) + "\n"
        for task in self.uncompleted_tasks_with_no_due_date:
            prompt_input += "- " + task.content + "\n"

        return prompt_input


class Todoist_Content():
    def __init__(self):
        self.apikey = self.parse_config()
        self.api = TodoistAPI(self.apikey)
        self.projects = self.get_project_information()
        self.prompt = self.create_tasklist_prompt()
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
        tasks = self.api.get_tasks()
        return tasks
    
    def get_projects_sync(self):
        projects = self.api.get_projects()
        return projects
    
    def get_comments_for_project(self, project_id):
        comments = self.api.get_comments(project_id=project_id)
        return comments
    
    def get_project_information(self):
        out_projectlist = []
        if self.apikey is None:
            print("No api key found")
        else:
            tasklist = self.get_tasks_sync()
            projectlist = self.get_projects_sync()
            for p in projectlist:
                pid = p.id
                project_tasks = []
                project_comments = self.get_comments_for_project(pid)
                for task in tasklist:
                    if task.project_id == pid:
                        project_tasks.append(task)
                project = TodoistProject(p, project_tasks, project_comments)
                out_projectlist.append(project)
        return out_projectlist
    
    def create_tasklist_prompt(self):
        prompt = ""
        for project in self.projects:
            if project.task_count > 0:
                prompt += project.prompt_input
                prompt += "\n"
        return prompt





if __name__ == '__main__':
    todoist_content = Todoist_Content()
    if todoist_content.apikey is None:
        print("No api key found")
        exit()
    else:
        tasklist = todoist_content.get_tasks_sync()
        projectlist = todoist_content.get_projects_sync()
        commentlist = todoist_content.get_comments_for_project(2313142145)
        for p in projectlist:
            pid = p.id
            project_tasks = []
            project_comments = []
            for task in tasklist:
                if task.project_id == pid:
                    project_tasks.append(task)
            for comment in commentlist:
                if comment.project_id == pid:
                    project_comments.append(comment)
            project = TodoistProject(p, project_tasks, project_comments)
            print(project.prompt_input)

        


"""
# task data:
[Task(assignee_id=None, assigner_id=None, comment_count=0, is_completed=False, content='Placeholders for unit tests', created_at='2023-05-29T13:46:50.018688Z', creator_id='15578057', description='Create placeholder unit tests in the 
repository.', due=None, id='6919257518', labels=[], order=1, parent_id=None, priority=1, project_id='2313142145', section_id=None, url='https://todoist.com/showTask?id=6919257518', sync_id=None)]

"""