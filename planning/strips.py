
ACTIONS = [

    {
        "name": "MoveToKey",

        "preconditions": {
            "key_reachable"
        },

        "add_effects": {
            "at_key"
        },

        "delete_effects": set()
    },

    {
        "name": "CollectKey",

        "preconditions": {
            "at_key"
        },

        "add_effects": {
            "has_key"
        },

        "delete_effects": {
            "at_key"
        }
    },

    {
        "name": "MoveToVault",

        "preconditions": {
            "has_key",
            "vault_reachable"
        },

        "add_effects": {
            "at_vault"
        },

        "delete_effects": {
            "at_key"
        }
    },

    {
        "name": "UnlockVault",

        "preconditions": {
            "at_vault",
            "has_key"
        },

        "add_effects": {
            "vault_unlocked"
        },

        "delete_effects": set()
    },

    {
        "name": "MoveToArtifact",

        "preconditions": {
            "vault_unlocked",
            "artifact_reachable"
        },

        "add_effects": {
            "at_artifact"
        },

        "delete_effects": {
            "at_vault"
        }
    },

    {
        "name": "CollectArtifact",

        "preconditions": {
            "at_artifact",
            "vault_unlocked"
        },

        "add_effects": {
            "has_artifact"
        },

        "delete_effects": {
            "at_artifact"
        }
    },

    {
        "name": "MoveToExit",

        "preconditions": {
            "has_artifact",
            "exit_reachable"
        },

        "add_effects": {
            "at_exit"
        },

        "delete_effects": set()
    },

    {
        "name": "Escape",

        "preconditions": {
            "at_exit",
            "has_artifact"
        },

        "add_effects": {
            "escaped"
        },

        "delete_effects": set()
    }

]

def applicable_actions(facts):

    available = []

    for action in ACTIONS:

        if action["preconditions"].issubset(facts):
            available.append(action)

    return available

def apply_action(facts, action):

    if not action["preconditions"].issubset(facts):
        raise ValueError(
            "Action preconditions are not satisfied"
        )

    new_facts = set(facts)

    new_facts.difference_update(
        action["delete_effects"]
    )

    new_facts.update(
        action["add_effects"]
    )

    return new_facts