from typing import Optional

from application.interfaces.workflow_engine.ProcessRunner import ProcessRunner
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class FakeProcessRunner(ProcessRunner):
    input: Optional[ProcessRunnerInput]
    result: ProcessRunnerResult

    def __init__(self, result: ProcessRunnerResult):
        self.input = None
        self.result = result

    def get_input(self) -> Optional[ProcessRunnerInput]:
        return self.input
    
    def run(
        self,
        payload: ProcessRunnerInput,
    ) -> ProcessRunnerResult:
        self.input = payload
        return self.result