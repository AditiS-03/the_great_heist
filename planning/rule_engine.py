
from collections import deque

from planning.planners import forward_plan
from planning.strips import ACTIONS

def is_reachable(board, start, goal):

    queue = deque([start])

    visited = {start}

    while queue:

        current = queue.popleft()

        if current == goal:
            return True

        for neighbor in board.neighbors(
            current,
            vault_unlocked=True
        ):

            if neighbor not in visited:

                visited.add(neighbor)

                queue.append(neighbor)

    return False

def build_facts(state):

    board = state.board

    thief_position = state.thief.position

    facts = set()

    # Inventory facts
    if state.has_key:
        facts.add("has_key")

    if state.vault_unlocked:
        facts.add("vault_unlocked")

    if state.has_artifact:
        facts.add("has_artifact")

    # Position facts
    positions = {
        "at_key": board.key_pos,
        "at_vault": board.vault_pos,
        "at_artifact": board.artifact_pos,
        "at_exit": board.exit_pos
    }

    for fact, position in positions.items():

        if thief_position == position:
            facts.add(fact)

    # Reachability facts
    targets = {
        "key_reachable": board.key_pos,
        "vault_reachable": board.vault_pos,
        "artifact_reachable": board.artifact_pos,
        "exit_reachable": board.exit_pos
    }

    for fact, position in targets.items():

        if is_reachable(
            board,
            thief_position,
            position
        ):

            facts.add(fact)

    return facts

def get_next_objective(state):

    if not state.has_key:
        return state.board.key_pos

    if not state.vault_unlocked:
        return state.board.vault_pos

    if not state.has_artifact:
        return state.board.artifact_pos

    return state.board.exit_pos

def get_heist_plan(state):

    facts = build_facts(state)

    return forward_plan(
        facts,
        {"escaped"}
    )

def get_current_action(state):

    plan = get_heist_plan(state)

    if plan:
        return plan[0]

    return None