import streamlit as st
from datetime import datetime

# -----------------------------
# Inventario inicial
# -----------------------------
if "inventario" not in st.session_state:
    st.session_state.inventario = {
        'ACE001': {'nombre': 'Aceite Motor 5W30', 'cantidad': 10, 'precio': 15000},
        'FILTRO01': {'nombre': 'Filtro Aceite', 'cantidad': 5, 'precio': 7000},
        'LUBRI02': {'nombre': 'Lubricante Frenos', 'cantidad': 2, 'precio': 12000},
        'ACE002': {'nombre': 'Aceite Motor 10W40', 'cantidad': 1, 'precio': 16000}
    }

if "carrito" not in st.session_state:
    st.session_state.carrito = []

st.title("🛢️ Sistema Web - Lubricentro")

# -----------------------------
# Buscar producto
# -----------------------------
st.subheader("🔍 Buscar Producto")

busqueda = st.text_input("Ingrese código o nombre")

if busqueda:
    encontrados = []
    for codigo, data in st.session_state.inventario.items():
        if busqueda.lower() in codigo.lower() or busqueda.lower() in data["nombre"].lower():
            encontrados.append((codigo, data))

    if encontrados:
        for codigo, data in encontrados:
            st.write(f"**{codigo} - {data['nombre']}**")
            st.write(f"Stock: {data['cantidad']}")
            st.write(f"Precio: ${data['precio']}")
            st.divider()
    else:
        st.error("Producto no encontrado")

# -----------------------------
# Agregar al carrito
# -----------------------------
st.subheader("🛒 Agregar al Carrito")

codigo = st.selectbox("Seleccione producto", list(st.session_state.inventario.keys()))
cantidad = st.number_input("Cantidad", min_value=1, step=1)

if st.button("Agregar al carrito"):
    producto = st.session_state.inventario[codigo]

    if cantidad > producto["cantidad"]:
        st.error("No hay suficiente stock")
    else:
        st.session_state.carrito.append({
            "codigo": codigo,
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio": producto["precio"]
        })
        st.success("Producto agregado al carrito")

# -----------------------------
# Mostrar carrito
# -----------------------------
st.subheader("📦 Carrito Actual")

if st.session_state.carrito:
    subtotal = 0
    for item in st.session_state.carrito:
        monto = item["cantidad"] * item["precio"]
        subtotal += monto
        st.write(f"{item['nombre']} | Cantidad: {item['cantidad']} | Monto: ${monto}")

    iva = round(subtotal * 0.19)
    total = subtotal + iva

    st.divider()
    st.write(f"Subtotal: ${subtotal}")
    st.write(f"IVA (19%): ${iva}")
    st.write(f"### Total: ${total}")

    # -----------------------------
    # Botón vender
    # -----------------------------
    if st.button("💰 Vender Todo"):
        for item in st.session_state.carrito:
            st.session_state.inventario[item["codigo"]]["cantidad"] -= item["cantidad"]

        st.session_state.carrito = []
        st.success("Venta realizada correctamente")

else:
    st.info("El carrito está vacío")

# -----------------------------
# Inventario actual
# -----------------------------
st.subheader("📊 Inventario Actual")

for codigo, data in sorted(st.session_state.inventario.items(), key=lambda x: x[1]["cantidad"]):
    st.write(f"{codigo} | {data['nombre']} | Stock: {data['cantidad']} | Precio: ${data['precio']}")
