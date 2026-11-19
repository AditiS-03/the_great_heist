
GOAL_TREE = {
    "escape_with_artifact": {
        "description": "Escape the museum carrying the artifact",
        "subgoals": [
            "collect_artifact",
            "reach_exit"
        ]
    },

    "collect_artifact": {
        "description": "Obtain the museum artifact",
        "subgoals": [
            "unlock_vault",
            "reach_artifact"
        ]
    },

    "unlock_vault": {
        "description": "Unlock the museum vault",
        "subgoals": [
            "collect_key",
            "reach_vault"
        ]
    },

    "collect_key": {
        "description": "Find and collect the vault key",
        "subgoals": [
            "reach_key"
        ]
    }
}

def get_subgoals(goal):

    if goal not in GOAL_TREE:
        return []

    return GOAL_TREE[goal]["subgoals"]

def display_goal_tree():

    def display(goal, level=0):

        print("  " * level + goal)

        for subgoal in get_subgoals(goal):
            display(subgoal, level + 1)

    display("escape_with_artifact")

def get_objectives():

    return [
        "reach_key",
        "collect_key",
        "reach_vault",
        "unlock_vault",
        "reach_artifact",
        "collect_artifact",
        "reach_exit"
    ]