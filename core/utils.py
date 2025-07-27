def obtener_faena(user):
    username = user.username.lower()
    if "mantos_cobrizos" in username:
        return "mantos_cobrizos"
    elif "tigresa" in username:
        return "tigresa"  # ya no 'bodega_tigresa'
    elif "revoltosa" in username:
        return "revoltosa"
    return ""