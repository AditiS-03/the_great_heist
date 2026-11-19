
from collections import deque

from planning.strips import (
    ACTIONS,
    applicable_actions,
    apply_action
)

def forward_plan(initial_facts, goal_facts):

    initial_facts = set(initial_facts)
    goal_facts = set(goal_facts)

    queue = deque([
        (initial_facts, [])
    ])

    visited = {
        frozenset(initial_facts)
    }

    while queue:

        facts, plan = queue.popleft()

        # Check whether the goal is achieved
        if goal_facts.issubset(facts):
            return plan

        # Find applicable actions
        for action in applicable_actions(facts):

            new_facts = apply_action(
                facts,
                action
            )

            state_key = frozenset(new_facts)

            if state_key not in visited:

                visited.add(state_key)

                new_plan = plan + [
                    action["name"]
                ]

                queue.append(
                    (new_facts, new_plan)
                )

    return []

def backward_plan(initial_facts, goal_facts):

    initial_facts = set(initial_facts)
    goal_facts = set(goal_facts)

    queue = deque([
        (goal_facts, [])
    ])

    visited = {
        frozenset(goal_facts)
    }

    while queue:

        goals, reverse_plan = queue.popleft()

        # All required goals are already true
        if goals.issubset(initial_facts):
            return list(reversed(reverse_plan))

        for action in ACTIONS:

            # The action must achieve at least one goal
            if not (
                action["add_effects"] & goals
            ):
                continue

            # It must not destroy an existing goal
            if (
                action["delete_effects"] & goals
            ):
                continue

            # Regress the goal through the action
            new_goals = (
                goals - action["add_effects"]
            ) | action["preconditions"]

            state_key = frozenset(new_goals)

            if state_key not in visited:

                visited.add(state_key)

                new_plan = reverse_plan + [
                    action["name"]
                ]

                queue.append(
                    (new_goals, new_plan)
                )

    return []