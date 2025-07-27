def ruta_inicio_context(request):
    ruta_inicio = "/"

    if request.user.is_authenticated:
        username = request.user.username
        if username.startswith("bodega_"):
            faena = username.replace("bodega_", "").lower()
            ruta_inicio = f"/core/bodega/{faena}/"
        elif username == "prevencion":
            ruta_inicio = "/prevencion/"
        elif username == "admin":
            ruta_inicio = "/admin/"

    return {
        'ruta_inicio': ruta_inicio
    }