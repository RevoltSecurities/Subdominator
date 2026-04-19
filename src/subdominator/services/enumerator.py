from __future__ import annotations

import asyncio
from collections import deque
from datetime import UTC, datetime
from time import perf_counter

from revoltlogger import Logger

from subdominator.core.models import EnumerationSummary, Finding, ResourceExecution, ResourceResult
from subdominator.resources.base import BaseResource


class EnumerationService:
    def __init__(self, logger: Logger, concurrency: int = 8, cancel_event: asyncio.Event | None = None) -> None:
        self.logger = logger
        self.semaphore = asyncio.Semaphore(concurrency)
        self.cancel_event = cancel_event

    async def enumerate(
        self,
        domain: str,
        resources: list[BaseResource],
        recursive_depth: int = 0,
    ) -> EnumerationSummary:
        started_at = datetime.now(UTC)
        queue = deque([(domain, 0)])
        seen_targets = {domain}
        unique_findings: dict[str, Finding] = {}
        resource_executions: list[ResourceExecution] = []

        while queue:
            current_target, depth = queue.popleft()
            self.logger.info(f"Enumerating {current_target} at recursion depth {depth}")
            tasks = {asyncio.create_task(self._run_resource(resource, current_target, depth)) for resource in resources}
            cancel_task = asyncio.create_task(self.cancel_event.wait()) if self.cancel_event else None
            
            while tasks:
                wait_list = list(tasks)
                if cancel_task and not cancel_task.done():
                    wait_list.append(cancel_task)

                done, pending = await asyncio.wait(wait_list, return_when=asyncio.FIRST_COMPLETED)

                if cancel_task and cancel_task in done:
                    self.logger.warn("Scan interrupted by user! Gracefully finalizing partial results...")
                    for task in tasks:
                        if not task.done():
                            task.cancel()
                    break

                tasks = set(task for task in done if task != cancel_task) | {task for task in pending if task != cancel_task}
                
                for task in [t for t in done if t != cancel_task]:
                    tasks.remove(task)
                    try:
                        result = task.result()
                    except asyncio.CancelledError:
                        continue

                    if isinstance(result, Exception):
                        self.logger.warn(f"Resource failed: {result}")
                        resource_executions.append(
                            ResourceExecution(
                                resource="unknown",
                                target=current_target,
                                recursion_depth=depth,
                                findings_count=0,
                                duration_ms=0,
                                error=str(result),
                            )
                        )
                        continue

                    self.logger.debug(
                        f"{result.resource} returned {len(result.findings)} findings for {current_target}"
                    )
                    resource_executions.append(
                        ResourceExecution(
                            resource=result.resource,
                            target=result.target,
                            recursion_depth=result.recursion_depth,
                            findings_count=len(result.findings),
                            duration_ms=result.duration_ms,
                            error=result.error,
                        )
                    )

                    for subdomain in result.findings:
                        existing = unique_findings.get(subdomain)
                        if existing is None:
                            unique_findings[subdomain] = Finding(
                                domain=domain,
                                subdomain=subdomain,
                                resource=result.resource,
                                query_target=result.target,
                                recursion_depth=result.recursion_depth,
                            )

                        if depth < recursive_depth and subdomain not in seen_targets:
                            seen_targets.add(subdomain)
                            queue.append((subdomain, depth + 1))
                            
            if cancel_task and cancel_task.done():
                break



        completed_at = datetime.now(UTC)
        return EnumerationSummary(
            root_domain=domain,
            recursive_depth=recursive_depth,
            started_at=started_at,
            completed_at=completed_at,
            targets_scanned=sorted(seen_targets),
            findings=sorted(unique_findings.values(), key=lambda item: item.subdomain),
            resource_executions=resource_executions,
            fresh_findings_count=len(unique_findings),
            new_findings_count=len(unique_findings),
        )

    async def _run_resource(self, resource: BaseResource, target: str, depth: int) -> ResourceResult:
        async with self.semaphore:
            started = perf_counter()
            try:
                result = await resource.enumerate(target, depth)
                result.duration_ms = int((perf_counter() - started) * 1000)
                return result
            except Exception as exc:
                self.logger.debug(
                    f"Exception occurred in {resource.name} API module due to: {exc}, {type(exc)}"
                )
                return ResourceResult(
                    resource=resource.name,
                    target=target,
                    recursion_depth=depth,
                    findings=[],
                    error=str(exc),
                    duration_ms=int((perf_counter() - started) * 1000),
                )
