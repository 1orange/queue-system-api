import simpy
from simpy.core import BoundClass

class PriorityGet(simpy.resources.base.Get):

    def __init__(self, resource, priority=10, preempt=True):
        self.priority = priority
        """The priority of this request. A smaller number means higher
        priority."""

        self.preempt = preempt
        """Indicates whether the request should preempt a resource user or not
        (:class:`PriorityResource` ignores this flag)."""

        self.time = resource._env.now
        """The time at which the request was made."""

        self.usage_since = None
        """The time at which the request succeeded."""

        self.key = (self.priority, self.time, not self.preempt)
        """Key for sorting events. Consists of the priority (lower value is
        more important), the time at which the request was made (earlier
        requests are more important) and finally the preemption flag (preempt
        requests are more important)."""

        super().__init__(resource)


class PriorityBaseStore(simpy.resources.store.Store):

    GetQueue = simpy.resources.resource.SortedQueue

    get = BoundClass(PriorityGet)