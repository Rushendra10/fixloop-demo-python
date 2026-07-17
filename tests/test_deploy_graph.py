import pytest

from deploy_graph import DependencyCycleError, deployment_order


def test_dependencies_are_deployed_before_consumers():
    services = {
        "api": ["database", "redis"],
        "worker": ["database", "redis"],
        "database": [],
        "redis": [],
    }
    order = deployment_order(services)
    assert order.index("database") < order.index("api")
    assert order.index("redis") < order.index("api")
    assert order.index("database") < order.index("worker")


def test_independent_services_use_stable_name_order():
    assert deployment_order({"worker": [], "api": [], "database": []}) == [
        "api",
        "database",
        "worker",
    ]


def test_real_cycles_are_rejected():
    with pytest.raises(DependencyCycleError, match="api"):
        deployment_order({"api": ["worker"], "worker": ["api"]})


def test_unknown_dependencies_are_rejected():
    with pytest.raises(KeyError, match="missing"):
        deployment_order({"api": ["missing"]})
