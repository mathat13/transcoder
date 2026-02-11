from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessRunner:
    def run(
        self,
        payload: ProcessRunnerInput,
    ) -> ProcessRunnerResult:
        context = payload.process_context
        process_definition = payload.process_definition

        try:
            for step in process_definition.steps:
                step.execute(context)
            return ProcessRunnerResult.success()
            
        except Exception as exc:
            return ProcessRunnerResult.failure(exc=exc)