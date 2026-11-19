def can_unlock_vault(state):

    return (
        state.has_key
        and state.thief.position == state.board.vault_pos
    )


def thief_has_won(state):

    return (
        state.has_artifact
        and state.thief.position == state.board.exit_pos
    )


def guard_has_won(state):

    return (
        state.thief.position == state.guard.position
        or state.round > 25
    )