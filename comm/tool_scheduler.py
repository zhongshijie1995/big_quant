from apscheduler.schedulers.background import BackgroundScheduler

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def get_scheduler(self):
        return self.scheduler
