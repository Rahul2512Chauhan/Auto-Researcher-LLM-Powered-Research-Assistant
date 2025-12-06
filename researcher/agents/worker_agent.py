# researcher/agents/worker_agent.py

from typing import Dict, Any, List
from researcher.agents.task_registry import TASK_MAP
from researcher.memory.memory_store import memory


class WorkerAgent:

    def __init__(self):
        pass

    def execute_task(self, task: Dict[str, Any], state: Dict[str, Any]):
        """
        Executes a single task using TASK_MAP and updates state.
        """

        name = task["name"]
        func = TASK_MAP.get(name)

        if func is None:
            print(f"[Worker] Unknown task: {name}")
            return state

        print(f"\n[Worker] Running task: {name}")

        # Gather inputs
        inputs = {k: state.get(k) for k in task.get("required_inputs", [])}

        # Execute function
        output = func(**inputs)

        # Save outputs into state
        if isinstance(task.get("expected_outputs"), list):
            # When function returns multiple values (dict)
            if isinstance(output, dict):
                for k, v in output.items():
                    state[k] = v
            else:
                # Single output → store under task name
                state[name] = output

        return state

    def run_plan(self, tasks: List[Dict[str, Any]], initial_state: Dict[str, Any]):
        """
        Runs tasks in dependency order.
        """
        state = initial_state.copy()

        for task in tasks:
            state = self.execute_task(task, state)

        return state
