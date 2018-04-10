def items():
    """Create some fake items. Useful to populate database tables.

    Returns
    -------
    list
    """
    return [
        {"name": "bread", "price": 0.5, "quantity": 20},
        {"name": "milk", "price": 1.0, "quantity": 10},
        {"name": "wine", "price": 10.0, "quantity": 5},
    ]
