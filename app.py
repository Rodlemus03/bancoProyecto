from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from flask_cors import CORS
import secrets
from functools import wraps
from modelos import loginBd,get_persona_by_usuario_id,ingresar_tarjeta,obtener_tarjetas_nuevas_por_usuario_id,activar_tarjetabd,obtener_tarjetas_activas_por_usuario_id,bloquear_tarjetabd,obtener_tarjetas_bloqueadas_por_usuario_id,desbloquear_tarjetabd,obtener_saldo_tarjeta_por_id,obtener_saldo_al_corte_tarjeta_por_id,obtener_limite_credito_por_id,obtener_tarjeta_por_detalles,ingresar_transaccion,obtener_transacciones_por_usuario,obtener_transacciones_por_tarjeta,generar_pdf,agregar_notificacion,obtener_notificaciones_por_usuario
import random
from datetime import datetime, timedelta

app=Flask(__name__)
app.secret_key=secrets.token_hex(16)
CORS(app)

# Decorador para verificar si el usuario está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("No estás autenticado", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    notis=obtener_notificaciones_por_usuario(session['user']['id'])
    return render_template('home.html',notificaciones=notis)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        contra = request.form['password']
        user = loginBd(username, contra)
        if user:
            persona=get_persona_by_usuario_id(user.id)
            session['user']={
                'id':persona.id,
                'nombre':persona.nombre,
                'apellido':persona.apellido,
                'telefono':persona.telefono,
                'correo':persona.correo            
            }
            return redirect(url_for('home'))
        else:
            flash("Credenciales incorrectas", "error")  # Mensaje de error flash
    return render_template('index.html')  # Renderiza el formulario de inicio de sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_credit_card_number(prefix, length):
    number = prefix
    while len(number) < (length - 1):
        digit = str(random.randint(0, 9))
        number.append(digit)
    checksum_digit = luhn_checksum(int(''.join(number)) * 10)
    number.append(str((10 - checksum_digit) % 10))
    return ''.join(number)

def generate_cvv():
    return '{:03d}'.format(random.randint(0, 999))

def generate_expiration_date():
    today = datetime.today()
    future_date = today + timedelta(days=random.randint(365, 365*5))  # 1 to 5 years in the future
    return future_date.date()
def generate_credit_card(name):
    card_types = {
        'Visa': ['4', 16],
        'MasterCard': ['5', 16],
        'American Express': ['3', 15]
    }
    
    if name not in card_types:
        raise ValueError("Nombre de tarjeta no soportado. Use 'Visa', 'MasterCard', or 'American Express'.")

    prefix, length = card_types[name]
    card_number = generate_credit_card_number(list(prefix), length)
    cvv = generate_cvv()
    expiration_date = generate_expiration_date()
    estado = 'activa'
    fecha_corte = expiration_date.replace(day=1)  # Primer día del mes
    
    return {
        'numero_tarjeta': card_number,
        'fecha_vencimiento': expiration_date,
        'cvv': cvv,
        'estado': estado,
        'fecha_corte': fecha_corte,
        'limite_credito': random.randint(1000, 10000),  # Ejemplo de límite de crédito aleatorio
        'saldo_actual': 0,
        'saldo_al_corte': 0
    }

# Ejemplo de uso

@app.route('/compra')
def compra():
    return render_template('compra1.html')

@app.route('/formulario_solicitud_tarjeta')
@login_required
def formulario_solicitud_tarjeta():
    return render_template('formulario_tarjeta.html')

@app.route('/solicitud_tarjeta',methods=['GET','POST'])
@login_required
def solicitud_tarjeta():
    tarjeta = generate_credit_card('Visa')
    ingresar_tarjeta(session['user']['id'],tarjeta['numero_tarjeta'],tarjeta['fecha_vencimiento'],tarjeta['cvv'],'nueva',tarjeta['fecha_corte'],tarjeta['limite_credito'],tarjeta['saldo_actual'],tarjeta['saldo_al_corte'])

    return render_template('home.html')

@app.route('/lista_activar_tarjeta',methods=['GET','POST'])
@login_required
def listado_activar_tarjetas():
    #FALTA
    tarjetas_nuevas=obtener_tarjetas_nuevas_por_usuario_id(session['user']['id'])
    return render_template('activar_tarjeta.html',tarjetas_nuevas=tarjetas_nuevas)

@app.route('/activar_tarjeta',methods=['GET','POST'])
@login_required
def activar_tarjeta():
    tarjeta_id=request.form.get('tarjeta_id')
    activar_tarjetabd(tarjeta_id)
    return render_template('home.html')

@app.route('/listado_tarjetas_activas',methods=['GET','POST'])
@login_required
def listado_tarjetas_activas():
    usuarioId=session['user']['id']
    tarjetas_activas=obtener_tarjetas_activas_por_usuario_id(usuarioId)
    return render_template('bloquear_tarjeta.html',tarjetas_activas=tarjetas_activas)

@app.route('/bloquear_tarjeta',methods=['GET','POST'])
@login_required
def bloquear_tarjeta():
    tarjeta_id=request.form.get('tarjeta_id')
    agregar_notificacion(session['user']['id'],'BLOQUEO DE TARJETA','Se ha bloqueado con exito la tarjeta')
    bloquear_tarjetabd(tarjeta_id)
    return render_template('home.html')

@app.route('/listado_tarjetas_bloqueadas',methods=['GET','POST'])
@login_required
def listado_tarjetas_bloqueadas():
    usuarioId=session['user']['id']
    tarjetas_bloqueadas=obtener_tarjetas_bloqueadas_por_usuario_id(usuarioId)
    return render_template('desbloquear_tarjeta.html',tarjetas_bloqueadas=tarjetas_bloqueadas)

@app.route('/desbloquear_tarjeta',methods=['GET','POST'])
@login_required
def desbloquear_tarjeta():
    tarjeta_id=request.form.get('tarjeta_id')
    agregar_notificacion(session['user']['id'],'DESBLOQUEO DE TARJETA','Se ha desbloqueado con exito la tarjeta')

    desbloquear_tarjetabd(tarjeta_id)
    return render_template('home.html')

@app.route('/api/saldo_tarjeta', methods=['GET'])
def saldo_tarjeta():
    # Verificar si se proporcionó el ID de la tarjeta en los parámetros de la solicitud
    tarjeta_id = request.args.get('tarjeta_id')
    
    if tarjeta_id is None:
        return jsonify({'error': 'Se debe proporcionar el ID de la tarjeta'}), 400
    
    try:
        saldo = obtener_saldo_tarjeta_por_id(int(tarjeta_id))
        if saldo is not None:
            return jsonify({'saldo': saldo}), 200
        else:
            return jsonify({'error': 'No se encontró la tarjeta o hubo un error al obtener el saldo'}), 404
    except ValueError:
        return jsonify({'error': 'ID de tarjeta no válido'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
    
@app.route('/api/saldo_al_corte_tarjeta', methods=['GET'])
def saldo_al_corte_tarjeta():
    # Verificar si se proporcionó el ID de la tarjeta en los parámetros de la solicitud
    tarjeta_id = request.args.get('tarjeta_id')
    
    if tarjeta_id is None:
        return jsonify({'error': 'Se debe proporcionar el ID de la tarjeta'}), 400
    
    try:
        saldo = obtener_saldo_al_corte_tarjeta_por_id(int(tarjeta_id))
        if saldo is not None:
            return jsonify({'saldo al corte': saldo}), 200
        else:
            return jsonify({'error': 'No se encontró la tarjeta o hubo un error al obtener el saldo'}), 404
    except ValueError:
        return jsonify({'error': 'ID de tarjeta no válido'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
    
@app.route('/api/limite_tarjeta', methods=['GET'])
def limite_tarjeta():
    # Verificar si se proporcionó el ID de la tarjeta en los parámetros de la solicitud
    tarjeta_id = request.args.get('tarjeta_id')
    
    if tarjeta_id is None:
        return jsonify({'error': 'Se debe proporcionar el ID de la tarjeta'}), 400
    
    try:
        saldo = obtener_limite_credito_por_id(int(tarjeta_id))
        if saldo is not None:
            return jsonify({'Limite': saldo}), 200
        else:
            return jsonify({'error': 'No se encontró la tarjeta o hubo un error al obtener el limite'}), 404
    except ValueError:
        return jsonify({'error': 'ID de tarjeta no válido'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
# Define tu nueva ruta API
@app.route('/api/crear_transaccion', methods=['POST'])
#@login_required
def api_crear_transaccion():
    try:
        data = request.json
        numero_tarjeta = data['numero_tarjeta']
        fecha_vencimiento = data['fecha_vencimiento']
        cvv = data['cvv']
        monto = data['monto']
        descripcion = data.get('descripcion', '')
        tipo=data['tipo']

        # Aquí debes encontrar el ID de la tarjeta basándote en el número de tarjeta, fecha de vencimiento y CVV
        # Esto asume que tienes una función para obtener la tarjeta. De lo contrario, ajusta según tu lógica.
        tarjeta = obtener_tarjeta_por_detalles(numero_tarjeta, fecha_vencimiento, cvv)
        if not tarjeta:
            return jsonify({'error': 'Tarjeta no encontrada'}), 404

        tarjeta_id = tarjeta.id

        fondos=tarjeta.limite_credito>=monto
        if fondos:
            # Crear la transacción
            ingresar_transaccion(tarjeta_id, monto, tipo, descripcion)
            agregar_notificacion(session['user']['id'],'TRANSACCION','Se ha realizado una transaccion de tipo: '+tipo+' por un monto de: '+str(monto))

            return jsonify({
                'mensaje': 'Transacción creada exitosamente'
            }), 201
        else:
            return jsonify({
                'mensaje': 'La tarjeta no cuenta con fondos'
            }), 401


    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al crear la transacción: {str(e)}'}), 500
    
@app.route('/ver_saldo_tarjetas',methods=['GET','POST'])
@login_required
def ver_saldo_tarjetas():
    usuarioId=session['user']['id']
    tarjetas_activas=obtener_tarjetas_activas_por_usuario_id(usuarioId)
    return render_template('saldos.html',tarjetas_activas=tarjetas_activas)

@app.route('/pagar_tarjeta', methods=['POST'])
@login_required
def pagar_tarjeta():
    try:
        data = request.get_json()
        tarjeta_id = data.get('tarjeta_id')
        monto = data.get('monto')
        respuesta=ingresar_transaccion(tarjeta_id,float(monto),'pago','pago de tarjeta')
        if not tarjeta_id or not monto:
            return jsonify({'error': 'Faltan datos necesarios para procesar el pago.'}), 400

        # Aquí se procesarían los datos recibidos, por ejemplo, registrando el pago en la base de datos.

        # Simulación de procesamiento exitoso
        return jsonify({'success': 'Pago procesado exitosamente.'}), 200

    except Exception as e:
        print(f"Error al procesar el pago: {e}")
        return render_template('home.html')
@app.route('/ver_movimientos')
@login_required
def ver_movimientos():
    id_usuario=session['user']['id']
    trx=obtener_transacciones_por_usuario(id_usuario)
    return render_template('transacciones.html',transacciones=trx)
    
@app.route('/listado_para_estado_cuenta')
@login_required
def listado_para_estado_cuenta():
    usuarioId=session['user']['id']
    tarjetas_activas=obtener_tarjetas_activas_por_usuario_id(usuarioId)
    return render_template('estados_cuenta.html',tarjetas_activas=tarjetas_activas)

@app.route('/generar_estado_cuenta',methods=['GET','POST'])
@login_required
def generar_estado_cuenta():
    tarjeta_id=request.form.get('tarjeta_id')
    trx=obtener_transacciones_por_tarjeta(tarjeta_id)
    pdf=generar_pdf(trx,tarjeta_id)
    return render_template('home.html')
#bloquear_tarjeta
    





        

       






if __name__=='__main__':
    app.run(debug=True)