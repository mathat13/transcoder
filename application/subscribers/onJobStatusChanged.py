from domain import JobStatus

def on_job_status_changed(event):
    if event.new_status == JobStatus.success:
        return True
        # email_service.send(f"Job {event.job_id} completed!")
