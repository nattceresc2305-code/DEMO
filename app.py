import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

# -----------------------------
# Inicializar datos en sesión
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

if "contador_facturas" not in st.session_state:
    st.session_state.contador_facturas = 1001


# -----------------------------
# Función generar PDF
# -----------------------------
def generar_pdf(carrito, numero_factura):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = 800

    # Encabezado
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "LUBRICENTRO")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "San Martin 50, Santiago, Chile")
    y -= 15
    c.drawString(50, y, "Tel: (9) 1234-5678")
    y -= 25

    c.drawString(50, y, f"N° Factura: {numero_factura}")
    y -= 15
    c.drawString(50, y, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 30

    # Tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Producto")
    c.drawString(300, y, "Cant.")
    c.drawString(360, y, "Precio")
    c.drawString(450, y, "Monto")
    y -= 15

    c.setFont("Helvetica", 10)
    subtotal = 0

    for item in carrito:
        monto = item["cantidad"] * item["precio"]
        subtotal += monto

        c.drawString(50, y, item["nombre"])
        c.drawString(310, y, str(item["cantidad"]))
        c.drawString(370, y, f"${item['precio']}")
        c.drawString(460, y, f"${monto}")
        y -= 20

    iva = round(subtotal * 0.19)
    total = subtotal + iva

    y -= 10
    c.drawString(350, y, f"Subtotal: ${subtotal}")
    y -= 15
    c.drawString(350, y, f"IVA (19%): ${iva}")
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, f"TOTAL: ${total}")

    y -= 40
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Gracias por su compra.")

    c.save()
    buffer.seek(0)
    return buffer


# -----------------------------
# Interfaz
# -----------------------------
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

        numero_factura = st.session_state.contador_facturas
        pdf = generar_pdf(st.session_state.carrito, numero_factura)

        # Descontar stock
        for item in st.session_state.carrito:
            st.session_state.inventario[item["codigo"]]["cantidad"] -= item["cantidad"]

        st.session_state.carrito = []
        st.session_state.contador_facturas += 1

        st.success("Venta realizada correctamente")

        st.download_button(
            label="📥 Descargar Factura PDF",
            data=pdf,
            file_name=f"factura_{numero_factura}.pdf",
            mime="application/pdf"
        )

else:
    st.info("El carrito está vacío")

# -----------------------------
# Inventario actual
# -----------------------------
st.subheader("📊 Inventario Actual")

for codigo, data in sorted(st.session_state.inventario.items(), key=lambda x: x[1]["cantidad"]):
    st.write(f"{codigo} | {data['nombre']} | Stock: {data['cantidad']} | Precio: ${data['precio']}")
