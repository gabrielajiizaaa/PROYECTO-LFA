from datetime import datetime
import os

#CLASES
class Usuario:
    def __init__(objeto, id_usuario, nombre_usuario):
        objeto.id_usuario = id_usuario
        objeto.nombre_usuario = nombre_usuario
    
    def __str__(objeto):
        return f"ID: {objeto.id_usuario}, Nombre: {objeto.nombre_usuario}"

class Libro:
    def __init__(objeto, id_libro, titulo_libro):
        objeto.id_libro = id_libro
        objeto.titulo_libro = titulo_libro
    
    def __str__(objeto):
        return f"ID: {objeto.id_libro}, Título: {objeto.titulo_libro}"

class Prestamo:
    def __init__(objeto, id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion=""):
        objeto.id_usuario = id_usuario
        objeto.nombre_usuario = nombre_usuario
        objeto.id_libro = id_libro
        objeto.titulo_libro = titulo_libro
        objeto.fecha_prestamo = fecha_prestamo
        objeto.fecha_devolucion = fecha_devolucion
    
    def __str__(objeto):
        return f"Usuario: {objeto.nombre_usuario}, Libro: {objeto.titulo_libro}, Prestado: {objeto.fecha_prestamo}, Devolución: {objeto.fecha_devolucion if objeto.fecha_devolucion else 'Pendiente'}"

class BibliotecaDigital:
    def __init__(objeto):
        objeto.usuarios = []
        objeto.libros = []
        objeto.prestamos = []
    
    def validar_fecha(objeto, fecha_str):
        
        if not fecha_str:
            return True  # Fecha vacía es válida para devolución
        
        if len(fecha_str) != 10: 
            return False
        
        #Formato YYYY-MM-DD
        partes = fecha_str.split('-')
        if len(partes) != 3:
            return False
        
        try:
            year, month, day = partes
            if len(year) != 4 or len(month) != 2 or len(day) != 2:
                return False
            
            # Verificar que sean números
            int(year)
            int(month)
            int(day)
            
            # Verificar que sea una fecha válida
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except:
            return False

    def validar_caracteres_validos(objeto, texto):
        caracteres_validos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 áéíóúÁÉÍÓÚñÑüÜ-.,()")
        for i, char in enumerate(texto):
            if char not in caracteres_validos:
                return False, f"Caracter no válido '{char}' en posición {i+1}"
        return True, ""

    def analizar_linea_usuario(objeto, linea, numero_linea):
        linea = linea.strip()
        if not linea:
            return None
        
        separador = ','
        if ';' in linea and linea.count(';') >= linea.count(','):
            separador = ';'
        
        partes = linea.split(separador)
        
        if len(partes) != 2:
            print(f"ERROR - Línea {numero_linea}: Formato incorrecto, se esperan 2 campos separados por '{separador}' (ID y Nombre)")
            return None
        
        try:
            id_usuario = partes[0].strip()
            if not id_usuario.isdigit():
                print(f"ERROR - Línea {numero_linea}, Posición 1: ID de usuario debe ser numérico, encontrado '{id_usuario}'")
                return None
            id_usuario = int(id_usuario)
            
            nombre_usuario = partes[1].strip()
            if not nombre_usuario:
                print(f"ERROR - Línea {numero_linea}, Posición 2: Nombre de usuario no puede estar vacío")
                return None
            
            # Validar caracteres válidos en nombre de usuario
            es_valido, mensaje = objeto.validar_caracteres_validos(nombre_usuario)
            if not es_valido:
                print(f"ERROR - Línea {numero_linea}, Posición 2: {mensaje}")
                return None
            
            return Usuario(id_usuario, nombre_usuario)
        
        except Exception as e:
            print(f"ERROR - Línea {numero_linea}: Error procesando datos de usuario - {str(e)}")
            return None

    def analizar_linea_libro(objeto, linea, numero_linea):
        linea = linea.strip()
        if not linea:
            return None
        
        separador = ','
        if ';' in linea and linea.count(';') >= linea.count(','):
            separador = ';'
        
        partes = linea.split(separador)
        
        if len(partes) != 2:
            print(f"ERROR - Línea {numero_linea}: Formato incorrecto, se esperan 2 campos separados por '{separador}' (ID, Título)")
            return None
        
        try:
            id_libro = partes[0].strip()
            if not id_libro:
                print(f"ERROR - Línea {numero_linea}, Posición 1: ID de libro no puede estar vacío")
                return None
            
            titulo_libro = partes[1].strip()
            if not titulo_libro:
                print(f"ERROR - Línea {numero_linea}, Posición 2: Título de libro no puede estar vacío")
                return None
            
            # Validar caracteres válidos en título de libro
            es_valido, mensaje = objeto.validar_caracteres_validos(titulo_libro)
            if not es_valido:
                print(f"ERROR - Línea {numero_linea}, Posición 2: {mensaje}")
                return None
            
            return Libro(id_libro, titulo_libro)
        
        except Exception as e:
            print(f"ERROR - Línea {numero_linea}: Error procesando datos de libro - {str(e)}")
            return None

    def analizar_linea_prestamo(objeto, linea, numero_linea):
        linea = linea.strip()
        if not linea:
            return None
               
        separador = ','
        if ';' in linea and linea.count(';') >= linea.count(','):
            separador = ';'
        
        partes = linea.split(separador)
        
        if len(partes) < 5:
            print(f"ERROR - Línea {numero_linea}: Formato incorrecto, se esperan al menos 5 campos separados por '{separador}'")
            return None
        
        try:
            id_usuario_str = partes[0].strip()
            if not id_usuario_str.isdigit():
                print(f"ERROR - Línea {numero_linea}, Posición 1: ID de usuario debe ser numérico, encontrado '{id_usuario_str}'")
                return None
            id_usuario = int(id_usuario_str)
            
            nombre_usuario = partes[1].strip()
            if not nombre_usuario:
                print(f"ERROR - Línea {numero_linea}, Posición 2: Nombre de usuario no puede estar vacío")
                return None
            
            es_valido, mensaje = objeto.validar_caracteres_validos(nombre_usuario)
            if not es_valido:
                print(f"ERROR - Línea {numero_linea}, Posición 2: {mensaje}")
                return None
            
            id_libro = partes[2].strip()
            if not id_libro:
                print(f"ERROR - Línea {numero_linea}, Posición 3: ID de libro no puede estar vacío")
                return None
            
            titulo_libro = partes[3].strip()
            if not titulo_libro:
                print(f"ERROR - Línea {numero_linea}, Posición 4: Título de libro no puede estar vacío")
                return None
            
            es_valido, mensaje = objeto.validar_caracteres_validos(titulo_libro)
            if not es_valido:
                print(f"ERROR - Línea {numero_linea}, Posición 4: {mensaje}")
                return None
            
            fecha_prestamo = partes[4].strip()
            if not objeto.validar_fecha(fecha_prestamo):
                print(f"ERROR - Línea {numero_linea}, Posición 5: Fecha de préstamo inválida '{fecha_prestamo}', formato esperado YYYY-MM-DD")
                return None
            
            fecha_devolucion = ""
            if len(partes) > 5:
                fecha_devolucion = partes[5].strip()
                if fecha_devolucion and not objeto.validar_fecha(fecha_devolucion):
                    print(f"ERROR - Línea {numero_linea}, Posición 6: Fecha de devolución inválida '{fecha_devolucion}', formato esperado YYYY-MM-DD")
                    return None
            
            return Prestamo(id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion)
        
        except Exception as e:
            print(f"ERROR - Línea {numero_linea}: Error procesando datos - {str(e)}")
            return None
    
    def cargar_usuarios_desde_archivo(objeto):
        print("-"*30)
        print("CARGAR USUARIOS")
        nombre_archivo = input("Ingrese el nombre del archivo de usuarios: ").strip()
        
        if not nombre_archivo.endswith('.txt'):
            nombre_archivo += '.txt'

        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            usuarios_cargados = 0
            usuarios_duplicados = 0

            print("Formato: ID_Usuario, Nombre_Usuario")
            print("-" * 50)
            
            for numero_linea, linea in enumerate(lineas, 1):
                usuario = objeto.analizar_linea_usuario(linea, numero_linea)
                if usuario:
                    # Verificar que no exista un usuario con el mismo ID
                    usuario_existe = False
                    for u in objeto.usuarios:
                        if u.id_usuario == usuario.id_usuario:
                            print(f"ADVERTENCIA - Línea {numero_linea}: Usuario con ID {usuario.id_usuario} ya existe ('{u.nombre_usuario}'), se omite")
                            usuario_existe = True
                            usuarios_duplicados += 1
                            break
                    
                    if not usuario_existe:
                        objeto.usuarios.append(usuario)
                        usuarios_cargados += 1
                        print(f"Usuario registrado: {usuario.nombre_usuario} (ID: {usuario.id_usuario})")
            
            print("-" * 50)
            print(f"Usuarios cargados exitosamente: {usuarios_cargados}")
            if usuarios_duplicados > 0:
                print(f"Usuarios duplicados omitidos: {usuarios_duplicados}")
            print(f"Total usuarios en sistema: {len(objeto.usuarios)}")
            
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
    
    def cargar_libros_desde_archivo(objeto):
        print("CARGAR LIBROS")
        nombre_archivo = input("Ingrese el nombre del archivo de libros: ").strip()
        
        if not nombre_archivo.endswith('.txt'):
            nombre_archivo += '.txt'
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            libros_cargados = 0
            libros_duplicados = 0
            
            print("Formato: ID_Libro, Título_Libro")
            print("-" * 50)
            
            for numero_linea, linea in enumerate(lineas, 1):
                libro = objeto.analizar_linea_libro(linea, numero_linea)
                if libro:
                    # Verificar que no exista un libro con el mismo ID
                    libro_existe = False
                    for l in objeto.libros:
                        if l.id_libro == libro.id_libro:
                            print(f"ADVERTENCIA - Línea {numero_linea}: Libro con ID '{libro.id_libro}' ya existe ('{l.titulo_libro}'), se omite")
                            libro_existe = True
                            libros_duplicados += 1
                            break
                    
                    if not libro_existe:
                        objeto.libros.append(libro)
                        libros_cargados += 1
                        print(f"Libro cargado: {libro.titulo_libro} (ID: {libro.id_libro})")
            
            print("-" * 50)
            print(f"Libros cargados exitosamente: {libros_cargados}")
            if libros_duplicados > 0:
                print(f"Libros duplicados omitidos: {libros_duplicados}")
            print(f"Total libros en sistema: {len(objeto.libros)}")
            
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
            print("Asegúrese de que el archivo exista en el directorio actual.")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
    
    def cargar_prestamos_desde_archivo(objeto):
        print("CARGAR PRÉSTAMOS")
        nombre_archivo = input("Ingrese el nombre del archivo (.lfa): ").strip()
        
        if not nombre_archivo.endswith('.lfa'):
            nombre_archivo += '.lfa'
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            prestamos_cargados = 0
            
            for numero_linea, linea in enumerate(lineas, 1):
                prestamo = objeto.analizar_linea_prestamo(linea, numero_linea)
                if prestamo:
                    # Verificar que el usuario exista
                    usuario_existe = False
                    for usuario in objeto.usuarios:
                        if usuario.id_usuario == prestamo.id_usuario:
                            usuario_existe = True
                            break
                    
                    # Si no existe usuario
                    if not usuario_existe:
                        print(f"ADVERTENCIA - Línea {numero_linea}: Usuario con ID {prestamo.id_usuario} no existe en el catálogo")
                        continue
                    
                    # Verificar que el libro exista
                    libro_existe = False
                    for libro in objeto.libros:
                        if libro.id_libro == prestamo.id_libro:
                            libro_existe = True
                            break

                    # Si no existe libro
                    if not libro_existe:
                        print(f"ADVERTENCIA - Línea {numero_linea}: Libro con ID {prestamo.id_libro} no existe en el catálogo")
                        continue
                    
                    objeto.prestamos.append(prestamo)
                    prestamos_cargados += 1
            
            print(f"Préstamos cargados exitosamente: {prestamos_cargados}")
            print(f"Total préstamos en sistema: {len(objeto.prestamos)}")
            
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
    
    def mostrar_historial_prestamos(objeto):
        print("HISTORIAL DE PRÉSTAMOS")
        if not objeto.prestamos:
            print("No hay préstamos registrados.")
            return
        
        print(f"{'ID Usuario':^10} {'Nombre Usuario':^20} {'ID Libro':^10} {'Título Libro':^30} {'Fecha Préstamo':^15} {'Fecha Devolución':^15}")
        print("-" * 120)

        for prestamo in objeto.prestamos:
            devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "Pendiente"
            print(f"{prestamo.id_usuario:^10} {prestamo.nombre_usuario:^20} {prestamo.id_libro:^10} {prestamo.titulo_libro:^30} {prestamo.fecha_prestamo:^15} {devolucion:^15}")
    
    def mostrar_usuarios_unicos(objeto):
        print("LISTADO DE USUARIOS")
        if not objeto.prestamos:
            print("No hay préstamos registrados.")
            return
        
        usuarios_unicos = {}
        for prestamo in objeto.prestamos:
            usuarios_unicos[prestamo.id_usuario] = prestamo.nombre_usuario
        
        print(f"{'ID Usuario':^10} {'Nombre Usuario':^25}")
        print("-" * 45)

        for id_usuario, nombre in usuarios_unicos.items():
            print(f"{id_usuario:^10} {nombre:^25}")
        print(f"Total usuarios únicos: {len(usuarios_unicos)}")
    
    def mostrar_libros_prestados(objeto):
        print("LISTADO DE LIBROS PRESTADOS")
        if not objeto.prestamos:
            print("No hay préstamos registrados.")
            return
        
        libros_unicos = {}
        for prestamo in objeto.prestamos:
            libros_unicos[prestamo.id_libro] = prestamo.titulo_libro
        
        print(f"{'ID Libro':^10} {'Título Libro':^30}")
        print("-" * 50)

        for id_libro, titulo in libros_unicos.items():
            print(f"{id_libro:^10} {titulo:^30}")
        print(f"Total libros diferentes prestados: {len(libros_unicos)}")
    
    def mostrar_estadisticas_prestamos(objeto):
        print("ESTADÍSTICAS DE PRÉSTAMOS")
        if not objeto.prestamos:
            print("No hay préstamos registrados.")
            return
        
        # Total de préstamos
        total_prestamos = len(objeto.prestamos)
        
        # Libro más prestado
        libros_contador = {}
        for prestamo in objeto.prestamos:
            if prestamo.id_libro in libros_contador:
                libros_contador[prestamo.id_libro] += 1
            else:
                libros_contador[prestamo.id_libro] = 1
        
        libro_mas_prestado = ""
        max_prestamos = 0
        for id_libro, count in libros_contador.items():
            if count > max_prestamos:
                max_prestamos = count
                # Buscar título del libro
                for prestamo in objeto.prestamos:
                    if prestamo.id_libro == id_libro:
                        libro_mas_prestado = prestamo.titulo_libro
                        break
        
        # Usuario más activo
        usuarios_contador = {}
        for prestamo in objeto.prestamos:
            if prestamo.id_usuario in usuarios_contador:
                usuarios_contador[prestamo.id_usuario] += 1
            else:
                usuarios_contador[prestamo.id_usuario] = 1
        
        usuario_mas_activo = ""
        max_prestamos_usuario = 0
        for id_usuario, count in usuarios_contador.items():
            if count > max_prestamos_usuario:
                max_prestamos_usuario = count
                # Buscar nombre del usuario
                for prestamo in objeto.prestamos:
                    if prestamo.id_usuario == id_usuario:
                        usuario_mas_activo = prestamo.nombre_usuario
                        break
        
        # Total usuarios únicos
        usuarios_unicos = len(set(prestamo.id_usuario for prestamo in objeto.prestamos))
        
        print(f"{'Estadística':^25} {'Valor':^25}")
        print("-" * 50)
        print(f"{'Total de préstamos:':<25} {total_prestamos:>25}")
        print(f"{'Libro más prestado:':<25} {libro_mas_prestado} ({max_prestamos} veces)")
        print(f"{'Usuario más activo:':<25} {usuario_mas_activo} ({max_prestamos_usuario} préstamos)")
        print(f"{'Total usuarios únicos:':<25} {usuarios_unicos:>25}")
    
    def mostrar_prestamos_vencidos(objeto):
        print("PRÉSTAMOS VENCIDOS")
        if not objeto.prestamos:
            print("No hay préstamos registrados.")
            return
        
        fecha_actual = datetime.now().date()
        prestamos_vencidos = []
        
        for prestamo in objeto.prestamos:
            # Si no tiene fecha de devolución, está pendiente
            if not prestamo.fecha_devolucion:
                try:
                    fecha_prestamo = datetime.strptime(prestamo.fecha_prestamo, '%Y-%m-%d').date()
                    from datetime import timedelta
                    fecha_limite = fecha_prestamo + timedelta(days=30)
                    if fecha_actual > fecha_limite:
                        prestamos_vencidos.append(prestamo)
                except:
                    continue
            else:
                try:
                    fecha_devolucion = datetime.strptime(prestamo.fecha_devolucion, '%Y-%m-%d').date()
                    if fecha_actual > fecha_devolucion:
                        prestamos_vencidos.append(prestamo)
                except:
                    continue
        
        if not prestamos_vencidos:
            print("No hay préstamos vencidos.")
            return
        
        print(f"{'ID Usuario':^10} {'Nombre Usuario':^20} {'ID Libro':^10} {'Título Libro':^30} {'Fecha Préstamo':^15} {'Fecha Límite':^20}")
        print("-" * 120)

        for prestamo in prestamos_vencidos:
            if prestamo.fecha_devolucion:
                fecha_limite = prestamo.fecha_devolucion
            else:
                # Calcular fecha límite para préstamos pendientes
                fecha_prestamo = datetime.strptime(prestamo.fecha_prestamo, '%Y-%m-%d').date()
                fecha_limite = (fecha_prestamo + timedelta(days=30)).strftime('%Y-%m-%d')
            
            print(f"{prestamo.id_usuario:^10} {prestamo.nombre_usuario:^20} {prestamo.id_libro:^10} {prestamo.titulo_libro:^30} {prestamo.fecha_prestamo:^15} {fecha_limite:^20}")
        print(f"\nTotal préstamos vencidos: {len(prestamos_vencidos)}")
   
    def exportar_reportes_html(objeto):
        print("REPORTES A HTML")
        
        try:
            # Crear directorio de reportes si no existe
            if not os.path.exists("reportes"):
                os.makedirs("reportes")
            
            # HTML base
            html_header = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .estadistica {{ margin: 10px 0; padding: 10px; background-color: #e8f4f8; }}
    </style>
</head>
<body>
    <h1>{titulo}</h1>
"""
            
            html_footer = """
</body>
</html>"""
            
            # 1. Historial de Préstamos
            with open("reportes/historial_prestamos.html", "w", encoding="utf-8") as f:
                f.write(html_header.format(titulo="Historial de Préstamos"))
                f.write("<table>\n")
                f.write("<tr><th>ID Usuario</th><th>Nombre Usuario</th><th>ID Libro</th><th>Título Libro</th><th>Fecha Préstamo</th><th>Fecha Devolución</th></tr>\n")
                
                for prestamo in objeto.prestamos:
                    devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "Pendiente"
                    f.write(f"<tr><td>{prestamo.id_usuario}</td><td>{prestamo.nombre_usuario}</td><td>{prestamo.id_libro}</td><td>{prestamo.titulo_libro}</td><td>{prestamo.fecha_prestamo}</td><td>{devolucion}</td></tr>\n")
                
                f.write("</table>\n")
                f.write(html_footer)
            
            # 2. Usuarios
            usuarios_unicos = {}
            for prestamo in objeto.prestamos:
                usuarios_unicos[prestamo.id_usuario] = prestamo.nombre_usuario
            
            with open("reportes/usuarios_unicos.html", "w", encoding="utf-8") as f:
                f.write(html_header.format(titulo="Listado de Usuarios Únicos"))
                f.write("<table>\n")
                f.write("<tr><th>ID Usuario</th><th>Nombre Usuario</th></tr>\n")
                
                for id_usuario, nombre in usuarios_unicos.items():
                    f.write(f"<tr><td>{id_usuario}</td><td>{nombre}</td></tr>\n")
                
                f.write("</table>\n")
                f.write(f"<p><strong>Total usuarios únicos: {len(usuarios_unicos)}</strong></p>\n")
                f.write(html_footer)
            
            # 3. Libros Prestados
            libros_unicos = {}
            for prestamo in objeto.prestamos:
                libros_unicos[prestamo.id_libro] = prestamo.titulo_libro
            
            with open("reportes/libros_prestados.html", "w", encoding="utf-8") as f:
                f.write(html_header.format(titulo="Listado de Libros Prestados"))
                f.write("<table>\n")
                f.write("<tr><th>ID Libro</th><th>Título Libro</th></tr>\n")
                
                for id_libro, titulo in libros_unicos.items():
                    f.write(f"<tr><td>{id_libro}</td><td>{titulo}</td></tr>\n")
                
                f.write("</table>\n")
                f.write(f"<p><strong>Total libros diferentes prestados: {len(libros_unicos)}</strong></p>\n")
                f.write(html_footer)
            
            # 4. Estadísticas
            total_prestamos = len(objeto.prestamos)
            
            libros_contador = {}
            for prestamo in objeto.prestamos:
                if prestamo.id_libro in libros_contador:
                    libros_contador[prestamo.id_libro] += 1
                else:
                    libros_contador[prestamo.id_libro] = 1
            
            libro_mas_prestado = ""
            max_prestamos = 0
            for id_libro, count in libros_contador.items():
                if count > max_prestamos:
                    max_prestamos = count
                    for prestamo in objeto.prestamos:
                        if prestamo.id_libro == id_libro:
                            libro_mas_prestado = prestamo.titulo_libro
                            break
            
            usuarios_contador = {}
            for prestamo in objeto.prestamos:
                if prestamo.id_usuario in usuarios_contador:
                    usuarios_contador[prestamo.id_usuario] += 1
                else:
                    usuarios_contador[prestamo.id_usuario] = 1
            
            usuario_mas_activo = ""
            max_prestamos_usuario = 0
            for id_usuario, count in usuarios_contador.items():
                if count > max_prestamos_usuario:
                    max_prestamos_usuario = count
                    for prestamo in objeto.prestamos:
                        if prestamo.id_usuario == id_usuario:
                            usuario_mas_activo = prestamo.nombre_usuario
                            break
            
            usuarios_unicos_count = len(set(prestamo.id_usuario for prestamo in objeto.prestamos))
            
            with open("reportes/estadisticas_prestamos.html", "w", encoding="utf-8") as f:
                f.write(html_header.format(titulo="Estadísticas de Préstamos"))
                f.write(f"<div class='estadistica'><strong>Total de préstamos:</strong> {total_prestamos}</div>\n")
                f.write(f"<div class='estadistica'><strong>Libro más prestado:</strong> {libro_mas_prestado} ({max_prestamos} veces)</div>\n")
                f.write(f"<div class='estadistica'><strong>Usuario más activo:</strong> {usuario_mas_activo} ({max_prestamos_usuario} préstamos)</div>\n")
                f.write(f"<div class='estadistica'><strong>Total usuarios únicos:</strong> {usuarios_unicos_count}</div>\n")
                f.write(html_footer)
            
            # 5. Préstamos Vencidos
            fecha_actual = datetime.now().date()
            prestamos_vencidos = []
            
            for prestamo in objeto.prestamos:
                if not prestamo.fecha_devolucion:
                    try:
                        fecha_prestamo = datetime.strptime(prestamo.fecha_prestamo, '%Y-%m-%d').date()
                        from datetime import timedelta
                        fecha_limite = fecha_prestamo + timedelta(days=30)
                        if fecha_actual > fecha_limite:
                            prestamos_vencidos.append(prestamo)
                    except:
                        continue
                else:
                    try:
                        fecha_devolucion = datetime.strptime(prestamo.fecha_devolucion, '%Y-%m-%d').date()
                        if fecha_actual > fecha_devolucion:
                            prestamos_vencidos.append(prestamo)
                    except:
                        continue
            
            with open("reportes/prestamos_vencidos.html", "w", encoding="utf-8") as f:
                f.write(html_header.format(titulo="Préstamos Vencidos"))
                f.write("<table>\n")
                f.write("<tr><th>ID Usuario</th><th>Nombre Usuario</th><th>ID Libro</th><th>Título Libro</th><th>Fecha Préstamo</th><th>Fecha Límite</th></tr>\n")
                
                for prestamo in prestamos_vencidos:
                    if prestamo.fecha_devolucion:
                        fecha_limite = prestamo.fecha_devolucion
                    else:
                        # Calcular fecha límite para préstamos pendientes
                        fecha_prestamo = datetime.strptime(prestamo.fecha_prestamo, '%Y-%m-%d').date()
                        fecha_limite = (fecha_prestamo + timedelta(days=30)).strftime('%Y-%m-%d')
                    
                    f.write(f"<tr><td>{prestamo.id_usuario}</td><td>{prestamo.nombre_usuario}</td><td>{prestamo.id_libro}</td><td>{prestamo.titulo_libro}</td><td>{prestamo.fecha_prestamo}</td><td>{fecha_limite}</td></tr>\n")

                f.write("</table>\n")
                f.write(f"<p><strong>Total préstamos vencidos: {len(prestamos_vencidos)}</strong></p>\n")
                f.write(html_footer)
            
            print("Reportes HTML generados:")
            print("historial_prestamos.html")
            print("usuarios_unicos.html")
            print("libros_prestados.html")
            print("estadisticas_prestamos.html")
            print("prestamos_vencidos.html")
            
        except Exception as e:
            print(f"Error generando reportes HTML: {str(e)}")

#MENU PRINCIPAL
print("Iniciando Sistema de Biblioteca Digital...")
biblioteca = BibliotecaDigital()

while True:
    print("-"*50)
    print("SISTEMA DE BIBLIOTECA DIGITAL")
    print("1. Cargar usuarios desde archivo")
    print("2. Cargar libros desde archivo")
    print("3. Cargar registro de préstamos desde archivo")
    print("4. Mostrar historial de préstamos")
    print("5. Mostrar listado de usuarios únicos")
    print("6. Mostrar listado de libros prestados")
    print("7. Mostrar estadísticas de préstamos")
    print("8. Mostrar préstamos vencidos")
    print("9. Exportar todos los reportes a HTML")
    print("10. Salir")
    print("-"*50)
        
    opcion = int(input("Seleccione una opción (1-10): "))
        
    match opcion:
        case 1:
            biblioteca.cargar_usuarios_desde_archivo()
        case 2:
            biblioteca.cargar_libros_desde_archivo()
        case 3:
            biblioteca.cargar_prestamos_desde_archivo()
        case 4:
            biblioteca.mostrar_historial_prestamos()
        case 5:
            biblioteca.mostrar_usuarios_unicos()
        case 6:
            biblioteca.mostrar_libros_prestados()
        case 7:
            biblioteca.mostrar_estadisticas_prestamos()
        case 8:
            biblioteca.mostrar_prestamos_vencidos()
        case 9:
            biblioteca.exportar_reportes_html()
        case 10:
            print("FIN - GABRIEL AJIN Y VELVETH UBEDO")
            break
            
    input("ENTER PARA SEGUIR--- ")
