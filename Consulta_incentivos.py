import streamlit as st
import pandas as pd
import os
from glob import glob


# ===============================
# CONFIGURACIÓN DE PÁGINA
# ===============================

st.set_page_config(
    page_title="Consulta de Incentivos",
    page_icon="💰",
    layout="wide"
)


#===============================
# DISEÑO 
#===============================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(70, 90, 140, 0.18), transparent 35%),
            radial-gradient(circle at bottom right, rgba(40, 70, 120, 0.15), transparent 35%),
            #0b0f17;
    }

    div[data-testid="stMainBlockContainer"] {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* TARJETA GLASS */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
    }
    
    .glass-label {
    font-size: 14px;
    opacity: 0.7;
    margin-bottom: 6px;
}

.glass-value {
    font-size: 34px;
    font-weight: 700;
}

    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# TÍTULO
# ===============================

st.title("Consulta de Incentivos")

st.write(
    "Consulta el incentivo de un colaborador por medio de su ID"
)


# ===============================
# RUTA DE ARCHIVOS DE INCENTIVOS
# ===============================

ruta_incentivos = os.path.join(
    os.path.dirname(__file__),
    "Incentivos"
)


# ===============================
# BUSCAR ARCHIVOS DE INCENTIVOS
# ===============================

archivos = glob(
    os.path.join(
        ruta_incentivos,
        "Incentivo_Institucional_*.xlsx"
    )
)

archivos = sorted(
    archivos,
    key= os.path.getmtime,
    reverse= True
)


nombres_archivos = [
    os.path.basename(archivo)
    for archivo in archivos
]


def mostrar_fecha(nombre):

    fecha = (
        nombre
        .replace("Incentivo_Institucional_Quincena_", "")
        .replace("Incentivo_Institucional_Mensual_", "")
        .replace(".xlsx", "")
    )

    fecha = pd.to_datetime(fecha)

    return fecha.strftime("%d/%m/%Y")


archivo_seleccionado = st.selectbox(
    "📅 Seleccionar el Corte",
    nombres_archivos,
    format_func=mostrar_fecha
)


ruta_archivo = os .path.join(
    ruta_incentivos,
    archivo_seleccionado
)

#===============================
# CARGAR BASES DEL CORTES
#==============================

base_coord = pd.read_excel(
    ruta_archivo,
    sheet_name="Coordinadores"
)

base_gerente = pd.read_excel(
    ruta_archivo,
    sheet_name="Gerentes"
)


base_zonal = pd.read_excel(
    ruta_archivo,
    sheet_name="Zonales"
)

base_subdirector = pd.read_excel(
    ruta_archivo,
    sheet_name="Subdirectores"
)

print(ruta_archivo)



# ===============================
# CONSOLIDAR BASES
# ===============================

base_consolidada = pd.concat(
    [
        base_coord,
        base_gerente,
        base_zonal,
        base_subdirector
    ],
    ignore_index=True
)



# ===============================
# VALIDAR QUE EXISTAN ARCHIVOS
# ===============================

if not archivos:

    st.error(
        "No se encontraron archivos de incentivos en la carpeta."
    )

    st.stop()


# ===============================
# ORDENAR ARCHIVOS
# ===============================

archivos = sorted(
    archivos,
    key=os.path.getmtime,
    reverse=True
)


# ===============================
# OBTENER NOMBRES DE ARCHIVO
# ===============================

nombres_archivos = [
    os.path.basename(archivo)
    for archivo in archivos
]


# ===============================
# RUTA DEL ARCHIVO SELECCIONADO
# ===============================

ruta_archivo = os.path.join(
    ruta_incentivos,
    archivo_seleccionado
)


# ===============================
# CARGAR BASES DEL CORTE
# ===============================

base_coord = pd.read_excel(
    ruta_archivo,
    sheet_name="Coordinadores"
)

base_gerente = pd.read_excel(
    ruta_archivo,
    sheet_name="Gerentes"
)

base_zonal = pd.read_excel(
    ruta_archivo,
    sheet_name="Zonales"
)

base_subdirector = pd.read_excel(
    ruta_archivo,
    sheet_name="Subdirectores"
)


# ===============================
# CONSOLIDAR TODAS LAS BASES
# ===============================

base_consolidada = pd.concat(
    [
        base_coord,
        base_gerente,
        base_zonal,
        base_subdirector
    ],
    ignore_index=True
)


# ===============================
# CAPTURA DE ID
# ===============================

id_colaborador = st.text_input(
    "👤Ingresa el ID del colaborador"
)


# ===============================
# BOTÓN BUSCAR
# ===============================

buscar = st.button("Buscar")


# ===============================
# BUSCAR COLABORADOR
# ===============================

if buscar:

    # Convierte el ID escrito a número
    id_numero = pd.to_numeric(
        id_colaborador,
        errors="coerce"
    )


    # ===============================
    # VALIDAR ID
    # ===============================

    if pd.isna(id_numero):

        st.warning(
            "Ingresa un ID válido"
        )

        st.stop()


    # ===============================
    # BUSCAR ID
    # ===============================

    resultado = base_consolidada[
        base_consolidada["ID"] == id_numero
    ]


    # ===============================
    # SI NO ENCUENTRA EL ID
    # ===============================

    if resultado.empty:

        st.warning(
            "No se encontró un colaborador con ese ID"
        )


    # ===============================
    # SI ENCUENTRA AL COLABORADOR
    # ===============================

    else:

        # Toma la primera fila del resultado
        colaborador = resultado.iloc[0] 
        st.caption(
            f"📅 Corte consultado: {mostrar_fecha(archivo_seleccionado)}"
    )

        # ===============================
        # ESTRUCTURA
        # ===============================

        st.subheader("Estructura")

        col_sub, col_zona, col_sucursal, col_coord = st.columns(4)


        with col_sub:

            if (
                "Subdirección" in colaborador.index
                and pd.notna(colaborador["Subdirección"])
            ):

                st.markdown("**🏛️ Subdirección**")

                st.markdown(
                    f'<span style="color:#A9B0BC;">{colaborador["Subdirección"]}</span>',
                    unsafe_allow_html=True
                )


        with col_zona:

            if (
                "Zona" in colaborador.index
                and pd.notna(colaborador["Zona"])
            ):

                st.markdown("**🗺️ Zona**")

                st.markdown(
                    f'<span style="color:#A9B0BC;">{colaborador["Zona"]}</span>',
                    unsafe_allow_html=True
                )


        with col_sucursal:

            if (
                "Sucursal" in colaborador.index
                and pd.notna(colaborador["Sucursal"])
            ):

                st.markdown("**🏬 Sucursal**")

                st.markdown(
                    f'<span style="color:#A9B0BC;">{colaborador["Sucursal"]}</span>',
                    unsafe_allow_html=True
                )


        with col_coord:

            if (
                "Coordinación" in colaborador.index
                and pd.notna(colaborador["Coordinación"])
            ):

                st.markdown("**👥 Coordinación**")

                st.markdown(
                    f'<span style="color:#A9B0BC;">{colaborador["Coordinación"]}</span>',
                    unsafe_allow_html=True
                )
                
                
        # ===============================
        # DATOS DEL COLABORADOR
        # ===============================

        st.subheader(
            colaborador["NOMBRE COMPLETO"]
        )

        st.caption(
            colaborador["PUESTO"]
        )


        # ===============================
        # RESULTADOS PRINCIPALES
        # ===============================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.markdown(
                f"""
        <div class="glass-card">
            <div class="glass-label">Compensación Final</div>
            <div class="glass-value">${colaborador["Compensación Final"]:,.0f}</div>
        </div>
        """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
        <div class="glass-card">
            <div class="glass-label">Calidad de Cartera</div>
            <div class="glass-value">{colaborador["Calidad de Cartera"]:,.2%}</div>
        </div>
        """,
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                f"""
        <div class="glass-card">
            <div class="glass-label">Clasificación</div>
            <div class="glass-value">{colaborador["Clasificación"]}</div>
        </div>
        """,
                unsafe_allow_html=True
            )



        # ===============================
        # DETALLE DEL INCENTIVO
        # ===============================

        st.subheader("Detalle del Incentivo")

        col_colocado, col_dist, col_clientes, col_calidad, col_caida = st.columns(5)


        # ===============================
        # COLOCADO
        # ===============================

        with col_colocado:

            st.write("### Colocado")

            st.caption("Crecimiento")
            st.write(
                f'${colaborador["Colocado Neto Var"]:,.0f}'
            )

            st.caption("Meta")
            st.write(
                f'${colaborador["Meta Colocado"]:,.0f}'
            )

            st.caption("% obtenido")
            st.write(
                f'{colaborador["Colocado %"]:.0%}'
            )


        # ===============================
        # DISTRIBUIDORAS
        # ===============================

        with col_dist:

            st.write("### Distribuidoras")

            st.caption("Crecimiento")
            st.write(
                f'{colaborador["Distribuidoras Totales Var"]:,.0f}'
            )

            st.caption("Meta")
            st.write(
                f'{colaborador["Meta Distribuidoras"]:,.0f}'
            )

            st.caption("% obtenido")
            st.write(
                f'{colaborador["Distribuidoras %"]:.0%}'
            )


        # ===============================
        # CLIENTES
        # ===============================

        with col_clientes:

            st.write("### Clientes")

            st.caption("Crecimiento")
            st.write(
                f'{colaborador["Clientes Var"]:,.0f}'
            )

            st.caption("Meta")
            st.write(
                f'{colaborador["Meta Clientes"]:,.0f}'
            )

            st.caption("% obtenido")
            st.write(
                f'{colaborador["Clientes %"]:.0%}'
            )


        # ===============================
        # CALIDAD
        # ===============================

        with col_calidad:

            st.write("### Calidad")

            st.caption("Actual")
            st.write(
                f'{colaborador["Calidad de Cartera"]:.2%}'
            )

            st.caption("Variación")
            st.write(
                f'{colaborador["Calidad de Cartera Var"]:.2%}'
            )

            st.caption("% obtenido")
            st.write(
                f'{colaborador["Calidad %"]:.0%}'
            )


        # ===============================
        # CAÍDA
        # ===============================

        with col_caida:

            st.write("### Caída")

            st.caption("Actual")
            st.write(
                f'{colaborador["Calidad de Caida"]:.2%}'
            )

            st.caption("Variación")
            st.write(
                f'{colaborador["Calidad de Caida Var"]:.2%}'
            )

            st.caption("% obtenido")
            st.write(
                f'{colaborador["Caida %"]:.0%}'
            )


        # ===============================
        # RESUMEN DE COMPENSACIÓN
        # ===============================

        st.subheader("Resumen de Compensación")

        col_total, col_primera, col_final = st.columns(3)


        with col_total:

            st.caption("% Total Obtenido")
            st.write(
                f'### {colaborador["% Total Obtenido"]:.0%}'
            )


        with col_primera:

            st.caption("Primera Compensación")
            st.write(
                f'### ${colaborador["Primera Compensación"]:,.0f}'
            )


        with col_final:

            st.caption("Compensación Final")
            st.write(
                f'### ${colaborador["Compensación Final"]:,.0f}'
            )


        # ===============================
        # PENALIZADORES
        # ===============================

        st.subheader("Penalizadores")

        col_cartera, col_clientes_pen, col_dist_pen = st.columns(3)


        with col_cartera:

            st.caption("Factor Cartera")
            st.write(
                f'### {colaborador["Factor Cartera"]:.0%}'
            )


        with col_clientes_pen:

            st.caption("Penalizador Clientes")
            st.write(
                f'### {colaborador["Penalizador Clientes"]:.0%}'
            )


        with col_dist_pen:

            st.caption("Penalizador Distribuidoras")
            st.write(
                f'### {colaborador["Penalizador Distribuidoras"]:.0%}'
            )

# abrir consulta incentivos
#py -m streamlit run Consulta_incentivos.py
# streamlit run Consulta_incentivos.py