def type_check(regime):
    def names_of_types(*types):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if regime == "in":
                    list_of_args_and_kwargs = list(args) + list(kwargs.values())

                    for item in list_of_args_and_kwargs:
                        if not isinstance(item, types):
                            expected_types = ", ".join(map(str, types))
                            print(f"Invalid input arguments, expected {expected_types}!")
                            return func(*args, **kwargs)

                result = func(*args, **kwargs)

                if regime == "out":
                    if not isinstance(result, types):
                        expected_types = ", ".join(map(str, types))
                        print(f"Invalid output value, expected {expected_types}!")
                return result
            return wrapper
        return decorator
    return names_of_types
