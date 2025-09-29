import streamlit as st
import json
import os

# --- Estilo personalizado ---
st.set_page_config(
    page_title="🔍 PE File Visualizer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .section-header {
        font-size: 1.4em;
        font-weight: bold;
        color: #1f77b4;
        margin-top: 1.2em;
    }
    .key {
        font-weight: bold;
        color: #2ca02c;
    }
    .value {
        color: #d62728;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- Título ---
st.title("🔍 PE File Visualizer")
st.caption("Creado desde la salida JSON de `readpe -f json`")

# --- Carga de archivo ---
uploaded_file = st.file_uploader("📁 Sube el archivo JSON generado por `readpe`", type=["json"])

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        
        # --- Sidebar resumen rápido ---
        with st.sidebar:
            st.header("📊 Resumen")
            if "COFF/File header" in data:
                st.write(f"**Máquina:** {data['COFF/File header'].get('Machine', 'N/A')}")
                st.write(f"**Secciones:** {data['COFF/File header'].get('Number of sections', 'N/A')}")
            if "Optional/Image header" in data:
                subsys = data["Optional/Image header"].get("Subsystem required", "N/A")
                st.write(f"**Subsistema:** {subsys}")
            if "Imported functions" in data:
                dlls = [lib["Name"] for lib in data["Imported functions"]]
                st.write(f"**DLLs importadas:** {len(dlls)}")
                st.write(", ".join(dlls[:3]) + ("..." if len(dlls) > 3 else ""))

        # --- Visualización por secciones ---
        tabs = st.tabs([
            "HeaderCode", "PE & COFF", "Optional Header", 
            "Data Directories", "Imports", "Exports", "Sections"
        ])

        # 1. DOS Header
        with tabs[0]:
            st.subheader("DOS Header")
            if "DOS Header" in data:
                for k, v in data["DOS Header"].items():
                    st.text_input(k, v, key=f"dos_{k}", disabled=True)
            else:
                st.info("No disponible")

        # 2. PE & COFF
        with tabs[1]:
            st.subheader("PE Header")
            if "PE header" in data:
                st.code(data["PE header"]["Signature"], language="text")
            
            st.subheader("COFF / File Header")
            if "COFF/File header" in data:
                for k, v in data["COFF/File header"].items():
                    if isinstance(v, list):
                        st.markdown(f"**{k}:**")
                        for item in v:
                            st.code(item, language=None)
                    else:
                        st.text_input(k, v, key=f"coff_{k}", disabled=True)

        # 3. Optional Header
        with tabs[2]:
            st.subheader("Optional (Image) Header")
            if "Optional/Image header" in data:
                for k, v in data["Optional/Image header"].items():
                    if isinstance(v, dict):
                        st.markdown(f"**{k}:**")
                        for sk, sv in v.items():
                            st.text_input(sk, sv, key=f"opt_{k}_{sk}", disabled=True)
                    elif isinstance(v, list):
                        st.markdown(f"**{k}:**")
                        for item in v:
                            st.code(item, language=None)
                    else:
                        st.text_input(k, v, key=f"opt_{k}", disabled=True)

        # 4. Data Directories
        with tabs[3]:
            st.subheader("Data Directories")
            if "Data directories" in data and isinstance(data["Data directories"], list):
                for entry in data["Data directories"]:
                    if isinstance(entry, dict) and len(entry) == 1:
                        name, addr = next(iter(entry.items()))
                        st.markdown(f"- **{name}**: `{addr}`")
                    else:
                        st.json(entry)
            else:
                st.info("No hay directorios de datos")

        # 5. Imports
        with tabs[4]:
            st.subheader("Imported Functions")
            if "Imported functions" in data and isinstance(data["Imported functions"], list):
                for lib in data["Imported functions"]:
                    with st.expander(f"📦 {lib['Name']} ({len(lib['Functions'])} funciones)"):
                        for func in lib["Functions"]:
                            hint = func.get("Hint", "?")
                            name = func.get("Name", "???")
                            st.code(f"{name} (Hint: {hint})", language=None)
            else:
                st.info("No hay funciones importadas")

        # 6. Exports
        with tabs[5]:
            st.subheader("Exported Functions")
            if "Exported functions" in data and data["Exported functions"]:
                for exp in data["Exported functions"]:
                    st.code(str(exp), language=None)
            else:
                st.success("✅ No hay funciones exportadas (común en ejecutables)")

        # 7. Sections
        with tabs[6]:
            st.subheader("SectionsIn")
            if "Sections" in data and isinstance(data["Sections"], list):
                for sec in data["Sections"]:
                    name = sec.get("Name", "???")
                    virt_size = sec.get("Virtual Size", "N/A")
                    raw_size = sec.get("Size Of Raw Data", "N/A")
                    flags = ", ".join(sec.get("Characteristic Names", []))
                    
                    # Icono según características
                    icon = "🔵"
                    if "IMAGE_SCN_MEM_EXECUTE" in flags:
                        icon = "🔴"  # Ejecutable → posible shellcode
                    elif "IMAGE_SCN_MEM_WRITE" in flags:
                        icon = "🟡"  # Escritura → sospechoso si también ejecutable
                    
                    with st.expander(f"{icon} {name} | VSize: {virt_size} | RSize: {raw_size}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Direcciones**")
                            st.text(f"VA: {sec.get('Virtual Address', 'N/A')}")
                            st.text(f"Raw: {sec.get('Pointer To Raw Data', 'N/A')}")
                        with col2:
                            st.markdown("**Características**")
                            for flag in sec.get("Characteristic Names", []):
                                if "EXECUTE" in flag:
                                    st.warning(flag)
                                elif "WRITE" in flag:
                                    st.info(flag)
                                else:
                                    st.success(flag)
            else:
                st.info("No hay secciones")

    except Exception as e:
        st.error(f"❌ Error al procesar el JSON: {e}")
        st.code(str(e))
else:
    st.info("👆 Sube un archivo JSON generado con: `readpe tu_archivo.exe -f json > salida.json`")
    st.markdown("""
    ### Ejemplo de uso:
    ```bash
    readpe malware.exe -f json > malware.json
    streamlit run pe_gui_viewer.py
    ```
    """)