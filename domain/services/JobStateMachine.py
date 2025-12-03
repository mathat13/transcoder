from domain.value_objects.JobStatus import JobStatus

JOB_STATE_MACHINE = {
    JobStatus.pending: [JobStatus.processing],
    JobStatus.processing: [JobStatus.verifying, JobStatus.error],
    JobStatus.verifying: [JobStatus.success, JobStatus.error],
    JobStatus.success: [],
    JobStatus.error: [],
}