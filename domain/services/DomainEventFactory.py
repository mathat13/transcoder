from domain.value_objects.JobStatus import JobStatus
from domain.events.DomainEvents import *

class DOMAIN_EVENT_FACTORY:
    @staticmethod
    def create(job, old_status, new_status):
        # Map transitions → domain event classes
        match new_status:
            case JobStatus.pending:
                return JobCreated(
                    job_id=job.id,
                    source_file=job.source_file
                )
            case JobStatus.verifying:
                return JobMovedToVerifying(
                    job_id=job.id,
                    transcode_file=job.transcode_file
                )
            case JobStatus.processing:
                return JobMovedToProcessing(
                    job_id=job.id
                )
            case JobStatus.success:
                return JobCompleted(
                    job_id=job.id,
                    source_file=job.source_file,
                    transcode_file=job.transcode_file,
                    media_ids=job.external_media_ids,

                )
            case JobStatus.error:
                return JobFailed(
                    job_id=job.id
                )
            case _:
                # fallback generic event if needed
                return JobStatusChanged(
                    job_id=job.id,
                    old_status=old_status.value,
                    new_status=new_status.value
                )
