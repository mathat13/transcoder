from domain import Job

from presentation.api.jobs.internal.queries.dtos.job_summary.dto import JobSummaryDTO

class JobSummaryMapper:
    @staticmethod
    def to_job_summary(job: Job) -> JobSummaryDTO:
        return JobSummaryDTO(
            id = str(job.id),
            source_file = str(job.source_file.path),
            transcode_output_file = str(job.transcode_output_file.path),
            delivery_file = str(job.delivery_file.path),
            status = job.status.value
        )