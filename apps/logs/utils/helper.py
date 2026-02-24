from ..models import ActivityLog

class Logger:
    @staticmethod
    def write(user, title, description, module):
        """
        A static method to create a log entry from anywhere in the project.
        """
        ActivityLog.objects.create(
            username=user.username,
            title=title,
            description=description,
            module=module
        )