from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Date, DECIMAL, JSON,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import date

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(100), nullable=False)
    contrasena = Column(String(255), nullable=False)  # La contraseña debe ser hasheada
    fecha_registro = Column(TIMESTAMP, default=datetime.utcnow)

    tarjetas = relationship('Tarjeta', back_populates='usuario')
    autenticaciones = relationship('Autenticacion', back_populates='usuario')
    notificaciones = relationship('Notificacion', back_populates='usuario_rel')

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    contenido = Column(String(200))
    usuario = Column(Integer, ForeignKey('usuarios.id'))
    

    usuario_rel = relationship('Usuario', back_populates='notificaciones')

class Tarjeta(Base):
    __tablename__ = 'tarjetas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    numero_tarjeta = Column(String(16), unique=True, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    cvv = Column(String(3), nullable=False)
    estado = Column(String(20), default='activa')
    fecha_corte = Column(Date, nullable=False)
    limite_credito = Column(DECIMAL(15, 2), nullable=False)
    saldo_actual = Column(DECIMAL(15, 2), default=0)
    saldo_al_corte = Column(DECIMAL(15, 2), default=0)

    usuario = relationship('Usuario', back_populates='tarjetas')
    transacciones = relationship('Transaccion', back_populates='tarjeta')
    saldos = relationship('Saldo', back_populates='tarjeta')
    estados_cuenta = relationship('EstadoCuenta', back_populates='tarjeta')

class Transaccion(Base):
    __tablename__ = 'transacciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarjeta_id = Column(Integer, ForeignKey('tarjetas.id'), nullable=False)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)
    monto = Column(DECIMAL(15, 2), nullable=False)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(String)

    tarjeta = relationship('Tarjeta', back_populates='transacciones')
    historial_transacciones = relationship('HistorialTransaccion', back_populates='transaccion')

class Saldo(Base):
    __tablename__ = 'saldos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarjeta_id = Column(Integer, ForeignKey('tarjetas.id'), nullable=False)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)
    saldo_actual = Column(DECIMAL(15, 2), nullable=False)
    saldo_disponible = Column(DECIMAL(15, 2), nullable=False)
    saldo_al_corte = Column(DECIMAL(15, 2), nullable=False)

    tarjeta = relationship('Tarjeta', back_populates='saldos')

class EstadoCuenta(Base):
    __tablename__ = 'estados_cuenta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarjeta_id = Column(Integer, ForeignKey('tarjetas.id'), nullable=False)
    fecha_corte = Column(Date, nullable=False)
    saldo_anterior = Column(DECIMAL(15, 2), nullable=False)
    saldo_nuevo = Column(DECIMAL(15, 2), nullable=False)

    tarjeta = relationship('Tarjeta', back_populates='estados_cuenta')

class Autenticacion(Base):
    __tablename__ = 'autenticacion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    token = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_expiracion = Column(TIMESTAMP, nullable=False)

    usuario = relationship('Usuario', back_populates='autenticaciones')

class HistorialTransaccion(Base):
    __tablename__ = 'historial_transacciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaccion_id = Column(Integer, ForeignKey('transacciones.id'), nullable=False)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)
    detalle = Column(JSON)

    transaccion = relationship('Transaccion', back_populates='historial_transacciones')

class Personas(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200))
    apellido = Column(String(200))
    telefono = Column(String(15))
    correo = Column(String(150))
    usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

# Configuración de la base de datos
DATABASE_URL = 'postgresql://postgres:pelu1503@localhost:5432/banco'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)

def loginBd(username, password):
    session = Session()
    try:
        user = session.query(Usuario).filter_by(user=username, contrasena=password).one()
        session.close()
        return user
    except NoResultFound:
        session.close()
        return None
    except SQLAlchemyError as e:
        print("Error al autenticar usuario:", e)
        session.close()
        return None

def get_persona_by_usuario_id(usuario_id):
    session = Session()
    try:
        persona = session.query(Personas).filter_by(usuario=usuario_id).one()
        session.close()
        return persona
    except NoResultFound:
        session.close()
        return None
    except SQLAlchemyError as e:
        print("Error al obtener la información de la persona:", e)
        session.close()
        return None

def ingresar_tarjeta(usuario_id, numero_tarjeta, fecha_vencimiento, cvv, estado, fecha_corte, limite_credito, saldo_actual, saldo_al_corte):
    session = Session()
    try:
        # Obtén el objeto Usuario completo a partir de su ID
        usuario = session.query(Usuario).filter_by(id=usuario_id).one()

        # Crea una nueva instancia de Tarjeta
        tarjeta = Tarjeta(
            usuario=usuario,  # Asigna el objeto Usuario completo
            numero_tarjeta=numero_tarjeta,
            fecha_vencimiento=fecha_vencimiento,
            cvv=cvv,
            estado=estado,
            fecha_corte=fecha_corte,
            limite_credito=limite_credito,
            saldo_actual=saldo_actual,
            saldo_al_corte=saldo_al_corte
        )

        # Agrega la nueva tarjeta a la sesión y la guarda en la base de datos
        session.add(tarjeta)
        session.commit()

        return True
    except NoResultFound:
        session.close()
        return None
    except SQLAlchemyError as e:
        print("Error al crear la tarjeta:", e)
        session.close()
        return None

def obtener_tarjetas_nuevas_por_usuario_id(usuario_id):
    session = Session()
    try:
        # Consulta todas las tarjetas del usuario con el estado 'nueva'
        tarjetas_nuevas = session.query(Tarjeta).filter_by(usuario_id=usuario_id, estado='nueva').all()
        session.close()
        return tarjetas_nuevas
    except Exception as e:
        print("Error al obtener tarjetas nuevas:", e)
        session.close()
        return None

def activar_tarjetabd(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID
        tarjeta = session.query(Tarjeta).filter_by(id=tarjeta_id, estado='nueva').one()
        # Cambiar el estado de la tarjeta a 'activa'
        tarjeta.estado = 'activa'
        # Confirmar los cambios en la base de datos
        session.commit()
        return True
    except NoResultFound:
        print("Tarjeta no encontrada o ya está activada.")
        session.close()
        return False
    except SQLAlchemyError as e:
        print("Error al activar la tarjeta:", e)
        session.close()
        return False

def obtener_tarjetas_activas_por_usuario_id(usuario_id):
    session = Session()
    try:
        # Consulta todas las tarjetas del usuario con el estado 'nueva'
        tarjetas_activas = session.query(Tarjeta).filter_by(usuario_id=usuario_id, estado='activa').all()
        session.close()
        return tarjetas_activas
    except Exception as e:
        print("Error al obtener tarjetas nuevas:", e)
        session.close()
        return None

def bloquear_tarjetabd(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID
        tarjeta = session.query(Tarjeta).filter_by(id=tarjeta_id, estado='activa').one()
        # Cambiar el estado de la tarjeta a 'bloqueada'
        tarjeta.estado = 'bloqueada'
        # Confirmar los cambios en la base de datos
        session.commit()
        return True
    except NoResultFound:
        print("Tarjeta no encontrada o ya está bloqueada.")
        session.close()
        return False
    except SQLAlchemyError as e:
        print("Error al activar la tarjeta:", e)
        session.close()
        return False

def obtener_tarjetas_bloqueadas_por_usuario_id(usuario_id):
    session = Session()
    try:
        # Consulta todas las tarjetas del usuario con el estado 'bloqueada'
        tarjetas_bloqueadas = session.query(Tarjeta).filter_by(usuario_id=usuario_id, estado='bloqueada').all()
        session.close()
        return tarjetas_bloqueadas
    except Exception as e:
        print("Error al obtener tarjetas bloqueadas:", e)
        session.close()
        return None

def desbloquear_tarjetabd(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID
        tarjeta = session.query(Tarjeta).filter_by(id=tarjeta_id, estado='bloqueada').one()
        # Cambiar el estado de la tarjeta a 'activa'
        tarjeta.estado = 'activa'
        # Confirmar los cambios en la base de datos
        session.commit()
        return True
    except NoResultFound:
        print("Tarjeta no encontrada o ya está desbloqueada.")
        session.close()
        return False
    except SQLAlchemyError as e:
        print("Error al activar la tarjeta:", e)
        session.close()
        return False
def obtener_saldo_tarjeta_por_id(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID y obtener su saldo
        saldo = session.query(func.coalesce(func.sum(Tarjeta.saldo_actual), 0)).filter_by(id=tarjeta_id).scalar()
        session.close()
        return saldo
    except Exception as e:
        print("Error al obtener saldo de la tarjeta:", e)
        session.close()
        return None
def obtener_saldo_al_corte_tarjeta_por_id(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID y obtener su saldo
        saldoCorte = session.query(func.coalesce(func.sum(Tarjeta.saldo_al_corte), 0)).filter_by(id=tarjeta_id).scalar()
        session.close()
        return saldoCorte
    except Exception as e:
        print("Error al obtener saldo de la tarjeta:", e)
        session.close()
        return None
    
def obtener_limite_credito_por_id(tarjeta_id):
    session = Session()
    try:
        # Buscar la tarjeta por su ID y obtener su saldo
        limite_credito = session.query(func.coalesce(func.sum(Tarjeta.limite_credito), 0)).filter_by(id=tarjeta_id).scalar()
        session.close()
        return limite_credito
    except Exception as e:
        print("Error al obtener limite de la tarjeta:", e)
        session.close()
        return None
    


def obtener_tarjeta_por_detalles(numero_tarjeta, fecha_vencimiento, cvv):
    sesion=Session()
    try:
        tarjeta = sesion.query(Tarjeta).filter_by(
            numero_tarjeta=numero_tarjeta,
            fecha_vencimiento=fecha_vencimiento,
            cvv=cvv
        ).first()
        return tarjeta
    except Exception as e:
        print(f'Error al obtener la tarjeta: {e}')
        return None
    
def ingresar_transaccion(tarjeta_id, monto, tipo, descripcion=''):
    sesion = Session()
    try:
        # Convertir monto a Decimal
        monto = Decimal(monto)
        
        # Crear la nueva transacción
        nueva_transaccion = Transaccion(
            tarjeta_id=tarjeta_id,
            monto=monto,
            tipo=tipo,
            descripcion=descripcion,
            fecha=datetime.utcnow()
        )
        sesion.add(nueva_transaccion)

        # Obtener la tarjeta correspondiente
        tarjeta = sesion.query(Tarjeta).filter_by(id=tarjeta_id).one()

        # Actualizar el límite de crédito y el saldo actual de la tarjeta
        if tipo == 'compra':
            tarjeta.limite_credito -= monto
            tarjeta.saldo_actual += monto
        elif tipo == 'pago':
            tarjeta.limite_credito += monto
            tarjeta.saldo_actual -= monto
            tarjeta.saldo_al_corte -= monto

        sesion.commit()
        return True
    except NoResultFound:
        sesion.rollback()
        sesion.close()
        return None
    except SQLAlchemyError as e:
        print("Error al crear la transaccion:", e)
        sesion.rollback()
        sesion.close()
        return None
    finally:
        sesion.close()

def obtener_transacciones_por_usuario(usuario_id):
    sesion = Session()
    try:
        # Obtener todas las tarjetas del usuario
        tarjetas = sesion.query(Tarjeta).filter_by(usuario_id=usuario_id).all()
        
        if not tarjetas:
            return None

        # Recoger todos los ids de tarjetas del usuario
        tarjeta_ids = [tarjeta.id for tarjeta in tarjetas]

        # Obtener todas las transacciones relacionadas con esas tarjetas
        transacciones = sesion.query(Transaccion).filter(Transaccion.tarjeta_id.in_(tarjeta_ids)).all()

        return transacciones
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print("Error al obtener las transacciones:", e)
        return None
    finally:
        sesion.close()

def generar_pdf(transacciones,tarjeta_id):
    # Crear un objeto PDF
    hoy=date.today()
    dia_hoy=hoy.day
    mes_hoy=hoy.month
    anio_hoy=hoy.year
    pdf = SimpleDocTemplate("estados_cuenta/estado_cuenta"+str(dia_hoy)+str(mes_hoy)+str(anio_hoy)+tarjeta_id[12:15]+".pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    # Crear contenido para el PDF
    contenido = []

    # Agregar título
    contenido.append(Paragraph("Estado de Cuenta", styles['Title']))
    contenido.append(Spacer(1, 12))

    # Agregar tabla de transacciones
    if transacciones:
        data = [['Fecha', 'Descripción', 'Monto','Tipo']]
        for trx in transacciones:
            data.append([trx.fecha, trx.descripcion, trx.monto,trx.tipo])
        tabla = Table(data)
        tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        contenido.append(tabla)
    else:
        contenido.append(Paragraph("No hay transacciones para esta tarjeta.", style_normal))

    # Generar el PDF
    pdf.build(contenido)

    return "estado_cuenta.pdf"
def obtener_transacciones_por_tarjeta(tarjeta_id):
    sesion = Session()
    try:
        # Obtener todas las tarjetas del usuario
        transacciones = sesion.query(Transaccion).filter_by(tarjeta_id=tarjeta_id).all()
        return transacciones
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print("Error al obtener las transacciones:", e)
        return None
    finally:
        sesion.close()

def agregar_notificacion(usuario_id, titulo, contenido):
    try:
        session=Session()
        # Crear una nueva instancia de Notificacion
        nueva_notificacion = Notificacion(
            titulo=titulo,
            contenido=contenido,
            usuario=usuario_id
        )
        
        # Agregar la nueva notificación a la sesión
        session.add(nueva_notificacion)
        
        # Confirmar la transacción
        session.commit()
    except SQLAlchemyError as e:
        # En caso de error, revertir la transacción
        session.rollback()
        # Manejar o registrar el error según sea necesario
        print(f"Error al agregar la notificación: {e}")
def obtener_notificaciones_por_usuario(usuario_id):
    sesion = Session()
    try:
        # Obtener todas las tarjetas del usuario
        notificacion = sesion.query(Notificacion).filter_by(usuario=usuario_id).all()
        
        return notificacion
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print("Error al obtener las transacciones:", e)
        return None
    finally:
        sesion.close()








