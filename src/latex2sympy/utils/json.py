def get_token(node, type):
    tokens = node.get('tokens') if 'tokens' in node else None
    token = next((t for t in node.get('tokens') if t.get('type') == type), None) if tokens is not None else None
    return token


def has_type_or_token(node, type):
    if 'type' in node and node.get('type') == type:
        return True
    token = get_token(node, type)
    return token is not None
