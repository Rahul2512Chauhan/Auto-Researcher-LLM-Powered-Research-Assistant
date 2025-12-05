# researcher/agents/orchestrator.py
from typing import List, Dict, Any, Tuple, Optional
from collections import deque, defaultdict

from researcher.agents.planner_agent import plan_research
from researcher.agents.worker_agent import WorkerAgent
from researcher.agents.reviewer_agent import ReviewerAgent


class Orchestrator:
    def __init__(self, reviewer_enabled: bool = True):
        self.worker = WorkerAgent()
        self.reviewer = ReviewerAgent() if reviewer_enabled else None

    def _build_task_map(self, tasks: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return {t["name"]: t for t in tasks}

    def _toposort(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Kahn's algorithm for topological sorting of tasks by 'dependencies'.
        Tasks with missing dependency fields or empty lists are treated as no-deps.
        If cycles or unknown deps exist, they will be ignored and order best-effort.
        """
        # Build graph
        deps = {t["name"]: set(t.get("dependencies", [])) for t in tasks}
        dependents = defaultdict(set)
        for t in tasks:
            for d in t.get("dependencies", []):
                dependents[d].add(t["name"])

        # Start with nodes that have no incoming edges
        q = deque([name for name, ds in deps.items() if not ds])
        ordered = []
        deps = {k: set(v) for k, v in deps.items()}

        while q:
            node = q.popleft()
            # append full task object
            ordered.append(node)
            for child in list(dependents.get(node, [])):
                deps[child].discard(node)
                if not deps[child]:
                    q.append(child)

            dependents.pop(node, None)

        # If some nodes still have dependencies (cycle or missing), append them at the end
        remaining = [name for name, ds in deps.items() if ds]
        ordered.extend(remaining)
        # Convert ordered names back to task objects
        name_to_task = self._build_task_map(tasks)
        return [name_to_task[n] for n in ordered if n in name_to_task]

    def run(self, query: str, initial_state: Optional[Dict[str, Any]] = None, review_each_task: bool = True) -> Dict[str, Any]:
        """
        Run the full pipeline:
        1) Planner -> tasks
        2) Toposort tasks by dependencies
        3) Execute each task via WorkerAgent
        4) Optionally review each task's outputs via ReviewerAgent
        Returns final state with metadata.
        """
        initial_state = initial_state.copy() if initial_state else {}
        initial_state.setdefault("query", query)

        # 1) Plan
        tasks = plan_research(query)
        if not tasks:
            return {"error": "planner_failed", "state": initial_state}

        # 2) Sort
        ordered_tasks = self._toposort(tasks)

        # 3) Execute
        state = initial_state
        run_log: List[Dict[str, Any]] = []

        for task in ordered_tasks:
            # execute
            before_state_keys = set(state.keys())
            state = self.worker.execute_task(task, state)
            after_state_keys = set(state.keys())

            produced_keys = list(after_state_keys - before_state_keys)
            log_entry = {
                "task": task["name"],
                "produced": produced_keys,
            }

            # 4) Review if enabled and review_each_task
            if self.reviewer and review_each_task:
                # pick something to review: if expected_outputs declared, prefer that
                expected_outputs = task.get("expected_outputs", [])
                to_review_text = ""
                if expected_outputs:
                    # combine outputs into a single text chunk
                    parts = []
                    for k in expected_outputs:
                        if k in state:
                            parts.append(str(state[k]))
                    to_review_text = "\n\n".join(parts)
                else:
                    # fallback: review the content stored under task name (if any)
                    to_review_text = str(state.get(task["name"], ""))

                if to_review_text.strip():
                    review_result = self.reviewer.review(task["name"], to_review_text)
                    # Attach review results to state under a reserved key
                    review_key = f"{task['name']}_review"
                    state[review_key] = review_result
                    log_entry["review"] = {"key": review_key, "issues": review_result.get("issues_found", [])}

            run_log.append(log_entry)

        return {"state": state, "run_log": run_log, "tasks": [t["name"] for t in ordered_tasks]}
