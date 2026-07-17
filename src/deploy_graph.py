from collections import defaultdict
from heapq import heappop, heappush


class DependencyCycleError(ValueError):
    pass


def deployment_order(services: dict[str, list[str]]) -> list[str]:
    """Return a stable dependency-first deployment order.

    ``services`` maps each service to the services it requires. Dependencies
    must be declared as services in the same deployment.
    """
    if not services:
        return []

    names = set(services)
    unknown = sorted(
        dependency
        for dependencies in services.values()
        for dependency in dependencies
        if dependency not in names
    )
    if unknown:
        raise KeyError(f"unknown dependencies: {', '.join(unknown)}")

    dependents: dict[str, set[str]] = defaultdict(set)
    indegree: dict[str, int] = {}
    for service, dependencies in services.items():
        # Manifests assembled from multiple fragments can contain duplicates.
        # The reverse edges are deduplicated, but indegree currently is not.
        indegree[service] = len(dependencies)
        for dependency in dependencies:
            dependents[dependency].add(service)

    ready: list[str] = []
    for service, degree in indegree.items():
        if degree == 0:
            heappush(ready, service)

    ordered: list[str] = []
    while ready:
        service = heappop(ready)
        ordered.append(service)
        for dependent in sorted(dependents[service]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heappush(ready, dependent)

    if len(ordered) != len(services):
        blocked = sorted(service for service, degree in indegree.items() if degree > 0)
        raise DependencyCycleError(f"dependency cycle involving: {', '.join(blocked)}")
    return ordered
