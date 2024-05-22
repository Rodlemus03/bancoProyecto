PGDMP  ,    8                |            banco    16.2    16.2 L    G           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            H           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            I           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            J           1262    210829    banco    DATABASE     x   CREATE DATABASE banco WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE banco;
                postgres    false            �            1259    210898    autenticacion    TABLE       CREATE TABLE public.autenticacion (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    token character varying(255) NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion timestamp without time zone NOT NULL
);
 !   DROP TABLE public.autenticacion;
       public         heap    postgres    false            �            1259    210897    autenticacion_id_seq    SEQUENCE     �   CREATE SEQUENCE public.autenticacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.autenticacion_id_seq;
       public          postgres    false    224            K           0    0    autenticacion_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.autenticacion_id_seq OWNED BY public.autenticacion.id;
          public          postgres    false    223            �            1259    210926    estados_cuenta    TABLE     �   CREATE TABLE public.estados_cuenta (
    id integer NOT NULL,
    tarjeta_id integer NOT NULL,
    fecha_corte date NOT NULL,
    saldo_anterior numeric(15,2) NOT NULL,
    saldo_nuevo numeric(15,2) NOT NULL
);
 "   DROP TABLE public.estados_cuenta;
       public         heap    postgres    false            �            1259    210925    estados_cuenta_id_seq    SEQUENCE     �   CREATE SEQUENCE public.estados_cuenta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.estados_cuenta_id_seq;
       public          postgres    false    226            L           0    0    estados_cuenta_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.estados_cuenta_id_seq OWNED BY public.estados_cuenta.id;
          public          postgres    false    225            �            1259    210938    historial_transacciones    TABLE     �   CREATE TABLE public.historial_transacciones (
    id integer NOT NULL,
    transaccion_id integer NOT NULL,
    fecha timestamp without time zone,
    detalle json
);
 +   DROP TABLE public.historial_transacciones;
       public         heap    postgres    false            �            1259    210937    historial_transacciones_id_seq    SEQUENCE     �   CREATE SEQUENCE public.historial_transacciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.historial_transacciones_id_seq;
       public          postgres    false    228            M           0    0    historial_transacciones_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.historial_transacciones_id_seq OWNED BY public.historial_transacciones.id;
          public          postgres    false    227            �            1259    211040    notificaciones    TABLE     �   CREATE TABLE public.notificaciones (
    id integer NOT NULL,
    titulo character varying(100),
    contenido character varying(200),
    usuario integer
);
 "   DROP TABLE public.notificaciones;
       public         heap    postgres    false            �            1259    211039    notificaciones_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notificaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.notificaciones_id_seq;
       public          postgres    false    232            N           0    0    notificaciones_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.notificaciones_id_seq OWNED BY public.notificaciones.id;
          public          postgres    false    231            �            1259    210952    personas    TABLE     �   CREATE TABLE public.personas (
    id integer NOT NULL,
    nombre character varying(200),
    apellido character varying(200),
    telefono character varying(15),
    correo character varying(150),
    usuario integer
);
    DROP TABLE public.personas;
       public         heap    postgres    false            �            1259    210951    personas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.personas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.personas_id_seq;
       public          postgres    false    230            O           0    0    personas_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.personas_id_seq OWNED BY public.personas.id;
          public          postgres    false    229            �            1259    210873    saldos    TABLE       CREATE TABLE public.saldos (
    id integer NOT NULL,
    tarjeta_id integer NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    saldo_actual numeric(15,2) NOT NULL,
    saldo_disponible numeric(15,2) NOT NULL,
    saldo_al_corte numeric(15,2) NOT NULL
);
    DROP TABLE public.saldos;
       public         heap    postgres    false            �            1259    210872    saldos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.saldos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.saldos_id_seq;
       public          postgres    false    222            P           0    0    saldos_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.saldos_id_seq OWNED BY public.saldos.id;
          public          postgres    false    221            �            1259    210841    tarjetas    TABLE     �  CREATE TABLE public.tarjetas (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    numero_tarjeta character varying(16) NOT NULL,
    fecha_vencimiento date NOT NULL,
    cvv character varying(3) NOT NULL,
    estado character varying(20) DEFAULT 'activa'::character varying,
    fecha_corte date NOT NULL,
    limite_credito numeric(15,2) NOT NULL,
    saldo_actual numeric(15,2) DEFAULT 0,
    saldo_al_corte numeric(15,2) DEFAULT 0
);
    DROP TABLE public.tarjetas;
       public         heap    postgres    false            �            1259    210840    tarjetas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tarjetas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.tarjetas_id_seq;
       public          postgres    false    218            Q           0    0    tarjetas_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.tarjetas_id_seq OWNED BY public.tarjetas.id;
          public          postgres    false    217            �            1259    210858    transacciones    TABLE       CREATE TABLE public.transacciones (
    id integer NOT NULL,
    tarjeta_id integer NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    monto numeric(15,2) NOT NULL,
    tipo character varying(50) NOT NULL,
    descripcion text
);
 !   DROP TABLE public.transacciones;
       public         heap    postgres    false            �            1259    210857    transacciones_id_seq    SEQUENCE     �   CREATE SEQUENCE public.transacciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.transacciones_id_seq;
       public          postgres    false    220            R           0    0    transacciones_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.transacciones_id_seq OWNED BY public.transacciones.id;
          public          postgres    false    219            �            1259    210831    usuarios    TABLE     �   CREATE TABLE public.usuarios (
    id integer NOT NULL,
    "user" character varying(100) NOT NULL,
    contrasena character varying(255) NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.usuarios;
       public         heap    postgres    false            �            1259    210830    usuarios_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usuarios_id_seq;
       public          postgres    false    216            S           0    0    usuarios_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;
          public          postgres    false    215            �           2604    210901    autenticacion id    DEFAULT     t   ALTER TABLE ONLY public.autenticacion ALTER COLUMN id SET DEFAULT nextval('public.autenticacion_id_seq'::regclass);
 ?   ALTER TABLE public.autenticacion ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223    224            �           2604    210929    estados_cuenta id    DEFAULT     v   ALTER TABLE ONLY public.estados_cuenta ALTER COLUMN id SET DEFAULT nextval('public.estados_cuenta_id_seq'::regclass);
 @   ALTER TABLE public.estados_cuenta ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    226    226            �           2604    210941    historial_transacciones id    DEFAULT     �   ALTER TABLE ONLY public.historial_transacciones ALTER COLUMN id SET DEFAULT nextval('public.historial_transacciones_id_seq'::regclass);
 I   ALTER TABLE public.historial_transacciones ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227    228            �           2604    211043    notificaciones id    DEFAULT     v   ALTER TABLE ONLY public.notificaciones ALTER COLUMN id SET DEFAULT nextval('public.notificaciones_id_seq'::regclass);
 @   ALTER TABLE public.notificaciones ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231    232            �           2604    210955    personas id    DEFAULT     j   ALTER TABLE ONLY public.personas ALTER COLUMN id SET DEFAULT nextval('public.personas_id_seq'::regclass);
 :   ALTER TABLE public.personas ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229    230            �           2604    210876 	   saldos id    DEFAULT     f   ALTER TABLE ONLY public.saldos ALTER COLUMN id SET DEFAULT nextval('public.saldos_id_seq'::regclass);
 8   ALTER TABLE public.saldos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222            z           2604    210844    tarjetas id    DEFAULT     j   ALTER TABLE ONLY public.tarjetas ALTER COLUMN id SET DEFAULT nextval('public.tarjetas_id_seq'::regclass);
 :   ALTER TABLE public.tarjetas ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            ~           2604    210861    transacciones id    DEFAULT     t   ALTER TABLE ONLY public.transacciones ALTER COLUMN id SET DEFAULT nextval('public.transacciones_id_seq'::regclass);
 ?   ALTER TABLE public.transacciones ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219    220            x           2604    210834    usuarios id    DEFAULT     j   ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);
 :   ALTER TABLE public.usuarios ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            <          0    210898    autenticacion 
   TABLE DATA           `   COPY public.autenticacion (id, usuario_id, token, fecha_creacion, fecha_expiracion) FROM stdin;
    public          postgres    false    224   �[       >          0    210926    estados_cuenta 
   TABLE DATA           b   COPY public.estados_cuenta (id, tarjeta_id, fecha_corte, saldo_anterior, saldo_nuevo) FROM stdin;
    public          postgres    false    226   
\       @          0    210938    historial_transacciones 
   TABLE DATA           U   COPY public.historial_transacciones (id, transaccion_id, fecha, detalle) FROM stdin;
    public          postgres    false    228   '\       D          0    211040    notificaciones 
   TABLE DATA           H   COPY public.notificaciones (id, titulo, contenido, usuario) FROM stdin;
    public          postgres    false    232   D\       B          0    210952    personas 
   TABLE DATA           S   COPY public.personas (id, nombre, apellido, telefono, correo, usuario) FROM stdin;
    public          postgres    false    230   ]       :          0    210873    saldos 
   TABLE DATA           g   COPY public.saldos (id, tarjeta_id, fecha, saldo_actual, saldo_disponible, saldo_al_corte) FROM stdin;
    public          postgres    false    222   Z]       6          0    210841    tarjetas 
   TABLE DATA           �   COPY public.tarjetas (id, usuario_id, numero_tarjeta, fecha_vencimiento, cvv, estado, fecha_corte, limite_credito, saldo_actual, saldo_al_corte) FROM stdin;
    public          postgres    false    218   w]       8          0    210858    transacciones 
   TABLE DATA           X   COPY public.transacciones (id, tarjeta_id, fecha, monto, tipo, descripcion) FROM stdin;
    public          postgres    false    220   '^       4          0    210831    usuarios 
   TABLE DATA           J   COPY public.usuarios (id, "user", contrasena, fecha_registro) FROM stdin;
    public          postgres    false    216   `       T           0    0    autenticacion_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.autenticacion_id_seq', 1, false);
          public          postgres    false    223            U           0    0    estados_cuenta_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.estados_cuenta_id_seq', 1, false);
          public          postgres    false    225            V           0    0    historial_transacciones_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.historial_transacciones_id_seq', 1, false);
          public          postgres    false    227            W           0    0    notificaciones_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.notificaciones_id_seq', 15, true);
          public          postgres    false    231            X           0    0    personas_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.personas_id_seq', 1, true);
          public          postgres    false    229            Y           0    0    saldos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.saldos_id_seq', 1, false);
          public          postgres    false    221            Z           0    0    tarjetas_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.tarjetas_id_seq', 4, true);
          public          postgres    false    217            [           0    0    transacciones_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.transacciones_id_seq', 35, true);
          public          postgres    false    219            \           0    0    usuarios_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);
          public          postgres    false    215            �           2606    210904     autenticacion autenticacion_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.autenticacion
    ADD CONSTRAINT autenticacion_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.autenticacion DROP CONSTRAINT autenticacion_pkey;
       public            postgres    false    224            �           2606    210931 "   estados_cuenta estados_cuenta_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.estados_cuenta
    ADD CONSTRAINT estados_cuenta_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.estados_cuenta DROP CONSTRAINT estados_cuenta_pkey;
       public            postgres    false    226            �           2606    210945 4   historial_transacciones historial_transacciones_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.historial_transacciones
    ADD CONSTRAINT historial_transacciones_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.historial_transacciones DROP CONSTRAINT historial_transacciones_pkey;
       public            postgres    false    228            �           2606    211045 "   notificaciones notificaciones_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.notificaciones
    ADD CONSTRAINT notificaciones_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.notificaciones DROP CONSTRAINT notificaciones_pkey;
       public            postgres    false    232            �           2606    210959    personas personas_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.personas DROP CONSTRAINT personas_pkey;
       public            postgres    false    230            �           2606    210879    saldos saldos_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.saldos
    ADD CONSTRAINT saldos_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.saldos DROP CONSTRAINT saldos_pkey;
       public            postgres    false    222            �           2606    210851 $   tarjetas tarjetas_numero_tarjeta_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.tarjetas
    ADD CONSTRAINT tarjetas_numero_tarjeta_key UNIQUE (numero_tarjeta);
 N   ALTER TABLE ONLY public.tarjetas DROP CONSTRAINT tarjetas_numero_tarjeta_key;
       public            postgres    false    218            �           2606    210849    tarjetas tarjetas_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.tarjetas
    ADD CONSTRAINT tarjetas_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.tarjetas DROP CONSTRAINT tarjetas_pkey;
       public            postgres    false    218            �           2606    210866     transacciones transacciones_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.transacciones
    ADD CONSTRAINT transacciones_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.transacciones DROP CONSTRAINT transacciones_pkey;
       public            postgres    false    220            �           2606    210837    usuarios usuarios_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            postgres    false    216            �           2606    210905 +   autenticacion autenticacion_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.autenticacion
    ADD CONSTRAINT autenticacion_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);
 U   ALTER TABLE ONLY public.autenticacion DROP CONSTRAINT autenticacion_usuario_id_fkey;
       public          postgres    false    216    224    4745            �           2606    210932 -   estados_cuenta estados_cuenta_tarjeta_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.estados_cuenta
    ADD CONSTRAINT estados_cuenta_tarjeta_id_fkey FOREIGN KEY (tarjeta_id) REFERENCES public.tarjetas(id);
 W   ALTER TABLE ONLY public.estados_cuenta DROP CONSTRAINT estados_cuenta_tarjeta_id_fkey;
       public          postgres    false    226    218    4749            �           2606    210946 C   historial_transacciones historial_transacciones_transaccion_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial_transacciones
    ADD CONSTRAINT historial_transacciones_transaccion_id_fkey FOREIGN KEY (transaccion_id) REFERENCES public.transacciones(id);
 m   ALTER TABLE ONLY public.historial_transacciones DROP CONSTRAINT historial_transacciones_transaccion_id_fkey;
       public          postgres    false    4751    220    228            �           2606    211046 *   notificaciones notificaciones_usuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notificaciones
    ADD CONSTRAINT notificaciones_usuario_fkey FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;
 T   ALTER TABLE ONLY public.notificaciones DROP CONSTRAINT notificaciones_usuario_fkey;
       public          postgres    false    232    4745    216            �           2606    210960    personas personas_usuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_usuario_fkey FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;
 H   ALTER TABLE ONLY public.personas DROP CONSTRAINT personas_usuario_fkey;
       public          postgres    false    230    4745    216            �           2606    210880    saldos saldos_tarjeta_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.saldos
    ADD CONSTRAINT saldos_tarjeta_id_fkey FOREIGN KEY (tarjeta_id) REFERENCES public.tarjetas(id);
 G   ALTER TABLE ONLY public.saldos DROP CONSTRAINT saldos_tarjeta_id_fkey;
       public          postgres    false    4749    218    222            �           2606    210852 !   tarjetas tarjetas_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarjetas
    ADD CONSTRAINT tarjetas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);
 K   ALTER TABLE ONLY public.tarjetas DROP CONSTRAINT tarjetas_usuario_id_fkey;
       public          postgres    false    218    4745    216            �           2606    210867 +   transacciones transacciones_tarjeta_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.transacciones
    ADD CONSTRAINT transacciones_tarjeta_id_fkey FOREIGN KEY (tarjeta_id) REFERENCES public.tarjetas(id);
 U   ALTER TABLE ONLY public.transacciones DROP CONSTRAINT transacciones_tarjeta_id_fkey;
       public          postgres    false    4749    220    218            <      x������ � �      >      x������ � �      @      x������ � �      D   �   x�����0�����CAe���17�
M� ����-��q8������C�;&�s�@A��C�s�I�	���1JQ*(T�Y
j��w9����(�����iX����]��#�,Oy�� �'��R��k����j���(*#(%U�|ck:=�
��f՚w���6�-�W�&W�8o&t�P���)�0�/ݙ��)�eaY��oJ�      B   ,   x�3�LL��̃��F�&f���Cznbf�^r~.�!W� ;��      :      x������ � �      6   �   x�U�9
�@�Zs�1ڗ��1�҇�?٘����㋀@]"�D0��F��>��4a�_��N���pC����/=�Yӄ-�׷���0�����B�rRTՖ.�<,ĐKճ-���# ����r�\���u�!�Uh.*�*��@����Xu7k籍1�ڢ:�      8   �  x���Mn�0���)|��Em{�n��(P ��4�i:�t"۰?<Q�O�S�����¸ 5���Eɦ@@�^/���:}9>��c����޷���v�IzF4Q`v��i#� T�X	%���zFmF�Z��$C��C�պ�f��A�q>T�T��@X�!,���pW҄����.�kyۖ���}�Xg�G�l ����R{T*A�Q��ҩuش4)*\�l���gx��CcDc����ȁ�8���ǃa(j4����d�`��M+1�v�f�P!$�����L�c�K�^�9�GrLë�8'qL���A��T2: 1n�ή���4.��J��%Zrر65p�6���A�X2FU}�Q{F�W:Νcp-�3�q�B5�Y#��!��pT�O��Mz��v��Ok�� �!���Q俐��r�� ���t��a7Ԁ��8cـR%��u{"����8�PP}?Zh@�W���7�)s      4   0   x�3�LL��̃�FF&����f
F�V��V��z&��fFf\1z\\\ �
6     