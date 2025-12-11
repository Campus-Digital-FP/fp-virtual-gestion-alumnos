import subprocess

def run_moosh_command(moodle, command, capture=False, timeout=10):
    print("run_moosh_command(...)")
    print("command:", command)

    command_string = f"docker exec {moodle['container_name']} {command}"

    try:
        if capture:
            result = subprocess.run(
                command_string,
                shell=True,           # interpreta el comando como string
                capture_output=True,  # captura stdout y stderr
                text=True,            # salida en str
                timeout=timeout       # segundos máximo
            )
            return result.stdout
        else:
            subprocess.run(
                command_string,
                shell=True,
                timeout=timeout
            )
    except subprocess.TimeoutExpired:
        print(f"⏱️ El comando tardó más de {timeout} segundos y fue cancelado.")
        return ""


def run_command(command, capture=False, timeout=10):
    print("run_command(...)")
    print("command:", command)

    try:
        if capture:
            result = subprocess.run(
                command,
                shell=True,           # mantiene compatibilidad con tu string de comando
                capture_output=True,  # guarda stdout y stderr
                text=True,            # convierte a str
                timeout=timeout       # segundos máximo
            )
            return result.stdout
        else:
            subprocess.run(
                command,
                shell=True,
                timeout=timeout
            )
    except subprocess.TimeoutExpired:
        print(f"⏱️ El comando tardó más de {timeout} segundos y fue cancelado.")
        return ""