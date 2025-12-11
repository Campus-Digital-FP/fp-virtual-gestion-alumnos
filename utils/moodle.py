import io
import os
from utils.moosh import run_moosh_command, run_command

def get_alumnos_moodle_no_borrados(moodle):
    print("get_alumnos_moodle_no_borrados(...)")
    """
    Devuelve una lista de alumnos (omite usuarios con username que empiece por prof) que actualmente están en moodle:
    #
    """
    cmd = "moosh -n user-list -n 50000 \"deleted = 0 and username not like 'prof%' \" " #listado de usuarios limitado a 50.000 # username (id), email,
    alumnos_moodle = run_moosh_command(moodle, cmd, True)
    
    alumnos = []    
    
    data_s = io.StringIO(alumnos_moodle).read()
    lines = data_s.splitlines()
    alumno = [
        {
            "username": line.split()[0],
            "userid": line.split()[1].replace("(","").replace("),",""),
            "email": line.split()[2].replace(",",""), # email del dominio google
            "email_sigad": "", # email de sigad
        }
        for line in lines
       
    ]
    alumnos.extend(alumno)

    # Recorro cada alumno y le añado el email de sigad
    for al in alumnos:
        
        command = '''\
            mysql --user=\"{DB_USER}\" --password=\"{DB_PASS}\" --host=\"{DB_HOST}\" -D \"{DB_NAME}\"  --execute=\"
                SELECT data
                FROM mdl_user_info_data
                where fieldid = 4 and userid = {id_usuario}
            \" | tail -n +2
            '''.format(DB_USER = os.getenv("DB_USER"), DB_PASS = os.getenv("DB_PASS"), DB_HOST = os.getenv("DB_HOST"), DB_NAME = os.getenv("DB_NAME"), id_usuario = al["userid"] )

        email_sigad = run_command( command , True).rstrip()
    
        print("email_sigad: ", email_sigad)

        al["email_sigad"] = email_sigad
    
    # Devuelvo el listado de alumnos que cumplen las condiciones
    return alumnos