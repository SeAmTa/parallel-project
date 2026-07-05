from app.services.thread.defining_thread import (
    scenario_1 as defining_thread_scenario_1,
    scenario_2 as defining_thread_scenario_2,
    scenario_3 as defining_thread_scenario_3,
)

from app.services.thread.current_thread import (
    scenario_1 as current_thread_scenario_1,
    scenario_2 as current_thread_scenario_2,
    scenario_3 as current_thread_scenario_3,
)

from app.services.thread.thread_subclass import (
    scenario_1 as thread_subclass_scenario_1,
    scenario_2 as thread_subclass_scenario_2,
    scenario_3 as thread_subclass_scenario_3,
)

from app.services.thread.lock_sync import (
    scenario_1 as lock_sync_scenario_1,
    scenario_2 as lock_sync_scenario_2,
    scenario_3 as lock_sync_scenario_3,
)

from app.services.thread.rlock_sync import (
    scenario_1 as rlock_sync_scenario_1,
    scenario_2 as rlock_sync_scenario_2,
    scenario_3 as rlock_sync_scenario_3,
)

from app.services.thread.semaphore_sync import (
    scenario_1 as semaphore_sync_scenario_1,
    scenario_2 as semaphore_sync_scenario_2,
    scenario_3 as semaphore_sync_scenario_3,
)

from app.services.thread.barrier_sync import (
    scenario_1 as barrier_sync_scenario_1,
    scenario_2 as barrier_sync_scenario_2,
    scenario_3 as barrier_sync_scenario_3,
)

from app.services.thread.event_sync import (
    scenario_1 as event_sync_scenario_1,
    scenario_2 as event_sync_scenario_2,
    scenario_3 as event_sync_scenario_3,
)

from app.services.thread.condition_sync import (
    scenario_1 as condition_sync_scenario_1,
    scenario_2 as condition_sync_scenario_2,
    scenario_3 as condition_sync_scenario_3,
)

from app.services.thread.queue_sync import (
    scenario_1 as queue_sync_scenario_1,
    scenario_2 as queue_sync_scenario_2,
    scenario_3 as queue_sync_scenario_3,
)

THREAD_SECTIONS = {
    1: {
        1: defining_thread_scenario_1,
        2: defining_thread_scenario_2,
        3: defining_thread_scenario_3,
    },
    
    2: {
        1: current_thread_scenario_1,
        2: current_thread_scenario_2,
        3: current_thread_scenario_3,
    },

    3: {
        1: thread_subclass_scenario_1,
        2: thread_subclass_scenario_2,
        3: thread_subclass_scenario_3,
    },

    4: {
        1: lock_sync_scenario_1,
        2: lock_sync_scenario_2,
        3: lock_sync_scenario_3,
    },

    5: {
        1: rlock_sync_scenario_1,
        2: rlock_sync_scenario_2,
        3: rlock_sync_scenario_3,
    },
    
    6: {
        1: semaphore_sync_scenario_1,
        2: semaphore_sync_scenario_2,
        3: semaphore_sync_scenario_3,
    },

    7: {
        1: barrier_sync_scenario_1,
        2: barrier_sync_scenario_2,
        3: barrier_sync_scenario_3,
    },

    8: {
        1: event_sync_scenario_1,
        2: event_sync_scenario_2,
        3: event_sync_scenario_3,
    },
    
    9: {
        1: condition_sync_scenario_1,
        2: condition_sync_scenario_2,
        3: condition_sync_scenario_3,
    },
    
    10: {
        1: queue_sync_scenario_1,
        2: queue_sync_scenario_2,
        3: queue_sync_scenario_3,
    },
}


def run_thread_scenario(section: int, scenario: int):
    try:
        return THREAD_SECTIONS[section][scenario]()
    except KeyError:
        return {
            "error": "Section or Scenario not implemented"
        }