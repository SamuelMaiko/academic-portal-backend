import random
from datetime import datetime, timedelta

from a_notifications.models import Notification
from a_work.models import Work


def run():
    try:
        # Define choices
        types = ["Essay", "Reflection Paper"]
        word_counts = [1500, 2000, 500, 2500]
        messages = [
            "Please follow the guidelines strictly.",
            "Ensure all sources are cited appropriately.",
            "The paper must adhere to the provided structure.",
            "Keep the content original and plagiarism-free.",
            "Focus on clarity and coherence throughout the paper.",
            "Provide a comprehensive analysis of the topic.",
            "Double-check grammar and formatting before submission.",
            "Make sure the paper aligns with the client's requirements.",
            "Include relevant and up-to-date references.",
            "The paper should be insightful and well-researched.",
        ]

        # Generate a random datetime within a range from 2 days to 2 months from today
        def random_deadline():
            start_date = datetime.now() + timedelta(days=2)
            end_date = datetime.now() + timedelta(days=60)  # Approx. 2 months
            return start_date + (end_date - start_date) * random.random()

        # Create 25 Work items
        for _ in range(25):
            work = Work(
                type=random.choice(types),
                words=random.choice(word_counts),
                comment=random.choice(messages),
                deadline=random_deadline(),
            )
            work.save()

        print("25 Work items created successfully.")

        Notification.objects.create(
            message="The work you bookmarked has been taken by another user",
            type="System Notification",
            triggered_by_id=1,
            work_id=2
            )
        Notification.objects.create(
            message="work has been has been reassigned",
            type="ReAssigned Work",
            triggered_by_id=1,
            work_id=2
            )
        
        Notification.objects.create(
            message="A new revision has been created for",
            type="New Revision",
            triggered_by_id=1,
            work_id=2
            )
        Notification.objects.create(
            message="is nearing deadline",
            type="Nearing Deadline",
            triggered_by_id=1,
            work_id=2
            )
        Notification.objects.create(
            message="work has been has been reassigned",
            type="Reassigned Work",
            triggered_by_id=1,
            work_id=2
            )
        
        print("5 Notifications created successfully")
        

        
    except Exception as e:
        print(f"Error: {e}")
