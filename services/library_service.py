def valid_phone(phone):

    return (
        phone.isdigit()
        and len(phone) == 10
    )
