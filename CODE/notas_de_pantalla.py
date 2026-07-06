import tkinter as tk
from tkinter import ttk
import os
import time
import random
import datetime
import base64
import threading
import platform
import random

try:
    import psutil
    PSUTIL_DISPONIBLE = True
except ImportError:
    PSUTIL_DISPONIBLE = False

class NotasMatrixTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL_OVR_v5.0")
        self.root.geometry("480x800")
        self.root.configure(bg="#000000")
        
        self.root.attributes('-topmost', True)
        self.sector_actual = "SECTOR_A"
        self.passkey = "2808"
        self.archivos = {
            "SECTOR_A": "notas_a.txt",
            "SECTOR_B": "notas_b.txt",
            "SECTOR_C": "notas_c.txt"
        }
        self.es_transparente = False
        self.modo_cifrado = False
        self.matrix_chars = "アカサタナハマヤラワガザダバパイウエオ0123456789$+-*/=%\"'#&_(),.;:?!"
        
        # Nuevos Estados
        self.audio_activado = True
        self.uplink_time = 0
        self.uplink_total = 0
        
        # Configuración de Estilos Retro
        self.configurar_estilos()
        
        # Interfaz
        self.crear_interfaz()
        
        # Procesos de fondo
        self.cargar_notas()
        self.actualizar_reloj()
        self.auto_guardado_ciclo()
        self.simular_logs()
        self.actualizar_recursos()
        self.animar_red_ascii()
        self.glitch_rutina()
        
        # Keybindings
        self.root.bind("<Control-t>", lambda e: self.toggle_transparencia())
        self.root.bind("<Escape>", lambda e: self.protocolo_panico())
        self.root.bind("<Control-s>", lambda e: self.guardar_notas())
        self.root.protocol("WM_DELETE_WINDOW", self.guardar_y_cerrar)

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#000000", borderwidth=0)
        style.configure("TNotebook.Tab", background="#050505", foreground="#008800", borderwidth=0, padding=[10, 2], font=("Consolas", 8))
        style.map("TNotebook.Tab", background=[("selected", "#000000")], foreground=[("selected", "#00FF00")])
        style.configure("TFrame", background="#000000", borderwidth=0)

    def crear_interfaz(self):
        self.main_container = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        self.main_container.pack(fill='both', expand=True)

        # Barra Superior
        self.top_bar = tk.Frame(self.main_container, bg="#050505")
        self.top_bar.pack(fill='x', side='top')
        
        self.frame_sectores = tk.Frame(self.top_bar, bg="#050505")
        self.frame_sectores.pack(side='left')
        
        self.btn_sectores = {}
        for sec in self.archivos.keys():
            btn = tk.Button(self.frame_sectores, text=f"[{sec}]", bg="#050505", fg="#004400", 
                           font=("Consolas", 8), relief="flat", command=lambda s=sec: self.cambiar_sector(s))
            btn.pack(side='left', padx=5)
            self.btn_sectores[sec] = btn
            
        self.btn_lock = tk.Button(self.top_bar, text="[ LOCK_CORE ]", bg="#050505", fg="#FF0000",
                                font=("Consolas", 8, "bold"), relief="flat", command=self.solicitar_cifrado)
        self.btn_lock.pack(side='right', padx=10)
        
        # Etiqueta Pomodoro (Uplink)
        self.lbl_uplink = tk.Label(self.top_bar, text="", bg="#050505", fg="#00FFFF", font=("Consolas", 8, "bold"))
        self.lbl_uplink.pack(side='right', padx=10)
        
        self.actualizar_estilo_botones_sector()

        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill='both', expand=True, padx=2, pady=2)

        # --- PESTAÑA: TERMINAL ---
        self.tab_notas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_notas, text=" >_ TERMINAL ")

        self.editor_container = tk.Frame(self.tab_notas, bg="#000000")
        self.editor_container.pack(fill='both', expand=True)

        self.area_texto = tk.Text(
            self.editor_container, bg="#000000", fg="#00FF00", insertbackground="#00FF00",
            font=("Consolas", 12), wrap="word", undo=True, padx=10, pady=10,
            relief="flat", borderwidth=0
        )
        self.area_texto.pack(fill='both', expand=True)

        self.canvas_matrix = tk.Canvas(self.editor_container, bg="#000000", highlightthickness=0)
        self.drops = []

        # --- CLI (Command Line Interface) ---
        self.cli_frame = tk.Frame(self.tab_notas, bg="#0A0A0A")
        self.cli_frame.pack(fill='x')
        tk.Label(self.cli_frame, text=" >", font=("Consolas", 10, "bold"), bg="#0A0A0A", fg="#00FF00").pack(side='left')
        self.cli_input = tk.Entry(self.cli_frame, bg="#0A0A0A", fg="#00FF00", font=("Consolas", 10), 
                                 insertbackground="#00FF00", relief="flat", borderwidth=0)
        self.cli_input.pack(side='left', fill='x', expand=True, padx=5)
        self.cli_input.bind("<Return>", self.ejecutar_comando)
        
        self.status_bar = tk.Label(
            self.tab_notas, text=" -- READY -- ", font=("Consolas", 8), 
            bg="#050505", fg="#006600", anchor="w"
        )
        self.status_bar.pack(fill='x')

        self.area_texto.tag_configure("urgente", foreground="#FF0000", font=("Consolas", 12, "bold"))
        self.area_texto.tag_configure("tarea", foreground="#00FFFF", font=("Consolas", 12, "italic"))
        self.area_texto.tag_configure("hecho", foreground="#444444", overstrike=True)
        self.area_texto.tag_configure("highlight", background="#333300")
        self.area_texto.bind("<KeyRelease>", self.refresh_ui)
        self.area_texto.bind("<KeyPress>", self.play_click, add="+")

        # --- PESTAÑA: SYSTEM ---
        self.tab_sys = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sys, text=" [ SYSTEM ] ")

        self.lbl_reloj = tk.Label(self.tab_sys, text="00:00:00", font=("Consolas", 20, "bold"), bg="#000000", fg="#00FF00")
        self.lbl_reloj.pack(pady=(10, 2))

        # Gráfico de Red ASCII
        self.net_canvas = tk.Canvas(self.tab_sys, height=60, bg="#000000", highlightthickness=0)
        self.net_canvas.pack(fill='x', padx=20)
        self.net_data = [random.randint(5, 45) for _ in range(40)]

        self.resource_frame = tk.Frame(self.tab_sys, bg="#000000")
        self.resource_frame.pack(fill='x', padx=30, pady=5)
        self.cpu_label = tk.Label(self.resource_frame, text="CPU [||||      ]", font=("Consolas", 9), bg="#000000", fg="#00FF00")
        self.cpu_label.pack(anchor='w')
        self.ram_label = tk.Label(self.resource_frame, text="RAM [||||||    ]", font=("Consolas", 9), bg="#000000", fg="#00FF00")
        self.ram_label.pack(anchor='w')

        firma_ascii = (
            "┌──────────────────────────────────────────┐\n"
            "│  AUTHORIZED OPERATOR: J.M. CAAMAÑO       │\n"
            "│  DIVISION: CREATOR & SYSADMIN            │\n"
            "│  NODE_STATUS: ONLINE                     │\n"
            "└──────────────────────────────────────────┘"
        )
        tk.Label(self.tab_sys, text=firma_ascii, font=("Consolas", 8), bg="#000000", fg="#FFFFFF").pack(pady=5)

        self.log_feed = tk.Text(self.tab_sys, bg="#000000", fg="#004400", font=("Consolas", 8), height=6, relief="flat")
        self.log_feed.pack(fill='x', padx=20)
        self.log_feed.config(state="disabled")

        # Aumentado el height para acomodar los atajos ocultos
        self.leyenda_box = tk.Text(self.tab_sys, bg="#000000", fg="#FFFFFF", font=("Consolas", 8), height=17, relief="flat", padx=30)
        self.leyenda_box.pack(fill='x', pady=5)
        self.setup_leyenda_estilizada()

        self.dibujar_scanlines()

    def setup_leyenda_estilizada(self):
        self.leyenda_box.tag_configure("red", foreground="#FF0000", font=("Consolas", 8, "bold"))
        self.leyenda_box.tag_configure("cyan", foreground="#00FFFF", font=("Consolas", 8, "italic"))
        self.leyenda_box.tag_configure("yellow", foreground="#FFFF00", font=("Consolas", 8, "bold"))
        self.leyenda_box.tag_configure("dim", foreground="#333333")
        linea_div = " ══════════════════════════════════════════\n"
        
        self.leyenda_box.insert(tk.END, linea_div, "dim")
        self.leyenda_box.insert(tk.END, " COMANDOS CLI:\n")
        self.leyenda_box.insert(tk.END, " /clear force > Borra sector \n")
        self.leyenda_box.insert(tk.END, " /find [X]    > Busca texto \n")
        self.leyenda_box.insert(tk.END, " /report      > Genera Informe\n")
        self.leyenda_box.insert(tk.END, " /analyze     > Stats Tácticas\n")
        self.leyenda_box.insert(tk.END, " /uplink [m]  > Timer Pomodoro\n")
        self.leyenda_box.insert(tk.END, " /audio off   > Mutea sonidos\n")
        self.leyenda_box.insert(tk.END, linea_div, "dim")
        self.leyenda_box.insert(tk.END, " ATAJOS OCULTOS:\n", "yellow")
        self.leyenda_box.insert(tk.END, " [Ctrl + T] > Toggle Transparencia\n")
        self.leyenda_box.insert(tk.END, " [ESC]      > Protocolo de Pánico\n")
        self.leyenda_box.insert(tk.END, " [Ctrl + S] > Forzar Guardado\n")
        self.leyenda_box.insert(tk.END, linea_div, "dim")
        self.leyenda_box.insert(tk.END, " !!! > CRÍTICA (Rojo)\n", "red")
        self.leyenda_box.insert(tk.END, " >>> > ACTIVA (Cian)\n", "cyan")
        self.leyenda_box.insert(tk.END, " OK  > FINALIZADA\n", "gray")
        self.leyenda_box.insert(tk.END, linea_div, "dim")
        self.leyenda_box.config(state="disabled")


    def ejecutar_comando(self, event=None):
        cmd_full = self.cli_input.get().strip()
        self.cli_input.delete(0, tk.END)
        if not cmd_full: return

        parts = cmd_full.split(" ", 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "/clear":
            messagebox = None
            if messagebox.askyesno("SISTEMA", "¿WIPE TOTAL DEL SECTOR ACTUAL?"):
                self.area_texto.delete("1.0", tk.END)
                self.guardar_notas()
                self.play_sound("success")
        elif cmd == "/find":
            self.area_texto.tag_remove("highlight", "1.0", tk.END)
            start = "1.0"
            while True:
                pos = self.area_texto.search(args, start, tk.END)
                if not pos: break
                self.area_texto.tag_add("highlight", pos, f"{pos}+{len(args)}c")
                start = f"{pos}+{len(args)}c"
            self.play_sound("success")
        elif cmd == "/report":
            self.generar_reporte_ascii()
            self.play_sound("success")
        elif cmd == "/hex":
            self.status_bar.config(text=" -- HEX_MODE_SIMULATED -- ")
        elif cmd == "/analyze":
            self.mostrar_analisis()
            self.play_sound("success")
        elif cmd == "/uplink":
            try:
                mins = int(args)
                self.iniciar_uplink(mins)
                self.play_sound("success")
            except ValueError:
                self.status_bar.config(text=" !! UPLINK REQUIERE MINUTOS (ej: /uplink 25) !! ", fg="#FF0000")
                self.play_sound("error")
        elif cmd == "/audio":
            self.audio_activado = (args != "off")
            self.status_bar.config(text=f" >> AUDIO {'ON' if self.audio_activado else 'OFF'} << ", fg="#00FFFF")
        else:
            self.status_bar.config(text=f" !! COMMAND_NOT_FOUND: {cmd} !! ", fg="#FF0000")
            self.play_sound("error")

    def generar_reporte_ascii(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"REPORT_{self.sector_actual}_{timestamp}.txt"
        contenido = self.area_texto.get("1.0", tk.END).strip()
        
        reporte = (
            f"╔══════════════════════════════════════════════════════╗\n"
            f"║ SEGURIDAD OVR - REPORTE DE SECTOR: {self.sector_actual: <17} ║\n"
            f"╠══════════════════════════════════════════════════════╣\n"
            f"║ FECHA: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'): <45} ║\n"
            f"╚══════════════════════════════════════════════════════╝\n\n"
            f"{contenido}\n\n"
            f"--- FIN DEL REGISTRO ---\n"
        )
        with open(fname, "w", encoding="utf-8") as f:
            f.write(reporte)
        self.status_bar.config(text=f" >> REPORTE GENERADO: {fname} ", fg="#00FFFF")

    def animar_red_ascii(self):
        self.net_canvas.delete("all")
        self.net_data.pop(0)
        self.net_data.append(random.randint(5, 55))
        
        w = 400
        step = w / len(self.net_data)
        for i in range(len(self.net_data)-1):
            x1, y1 = i * step, 60 - self.net_data[i]
            x2, y2 = (i+1) * step, 60 - self.net_data[i+1]
            self.net_canvas.create_line(x1, y1, x2, y2, fill="#004400", width=1)
            if i % 5 == 0:
                self.net_canvas.create_text(x1, 55, text=".", fill="#00FF00", font=("Consolas", 6))
        
        self.root.after(500, self.animar_red_ascii)

    # --- NUEVAS FUNCIONES Y MEJORAS ---
    def play_sound(self, tipo):
        if not self.audio_activado: return
        if tipo == "error":
            self.root.bell()
        elif tipo == "success":
            self.root.bell()

    def play_click(self, event=None):
        if self.audio_activado and event and event.char:
            if platform.system() == "Windows":
                try:
                    import winsound
                    threading.Thread(target=lambda: winsound.Beep(1200, 5), daemon=True).start()
                except:
                    pass

    def mostrar_analisis(self):
        texto = self.area_texto.get("1.0", tk.END)
        pendientes = texto.count(">>>")
        criticas = texto.count("!!!")
        completadas = texto.count("OK")
        palabras = len(texto.split())
        estabilidad = max(0, 100 - (criticas * 15) - (pendientes * 5) + (completadas * 5))
        
        analisis = (f"\n\n==================================\n"
                    f">> ANÁLISIS TÁCTICO DE SECTOR <<\n"
                    f" TAREAS PENDIENTES : {pendientes}\n"
                    f" ALERTAS CRÍTICAS  : {criticas}\n"
                    f" RESOLUCIONES (OK) : {completadas}\n"
                    f" VOLUMEN DE DATOS  : {palabras} words\n"
                    f" ESTABILIDAD       : {estabilidad}%\n"
                    f"==================================\n")
        self.area_texto.insert(tk.END, analisis)
        self.area_texto.see(tk.END)
        self.status_bar.config(text=" >> ANÁLISIS COMPLETADO << ", fg="#00FFFF")

    def iniciar_uplink(self, minutos):
        self.uplink_total = minutos * 60
        self.uplink_time = self.uplink_total
        self.actualizar_uplink()
        
    def actualizar_uplink(self):
        if self.uplink_time > 0:
            m, s = divmod(self.uplink_time, 60)
            progreso = int((1 - (self.uplink_time / self.uplink_total)) * 10)
            barra = "█" * progreso + "░" * (10 - progreso)
            self.lbl_uplink.config(text=f"UPLINK [{barra}] {m:02d}:{s:02d}")
            self.uplink_time -= 1
            self.root.after(1000, self.actualizar_uplink)
        elif self.uplink_total > 0:
            self.lbl_uplink.config(text="[ UPLINK CERRADO ]", fg="#FF0000")
            self.play_sound("error")
            self.hacer_parpadeo_rojo()
            self.uplink_total = 0
            self.root.after(5000, lambda: self.lbl_uplink.config(text=""))
            
    def hacer_parpadeo_rojo(self):
        orig_bg = self.area_texto.cget("bg")
        self.area_texto.config(bg="#330000")
        self.root.after(200, lambda: self.area_texto.config(bg=orig_bg))
        self.root.after(400, lambda: self.area_texto.config(bg="#330000"))
        self.root.after(600, lambda: self.area_texto.config(bg=orig_bg))

    def glitch_rutina(self):
        if not self.modo_cifrado and random.random() < 0.02: 
            orig_bg = self.area_texto.cget("bg")
            self.area_texto.config(bg="#001100")
            self.status_bar.config(text=" !! INTERFERENCIA DETECTADA !! ", fg="#FFFF00")
            self.log_feed.config(state="normal")
            self.log_feed.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] TRACE INITIATED...\n")
            self.log_feed.see(tk.END)
            self.log_feed.config(state="disabled")
            self.root.after(300, lambda: self.area_texto.config(bg=orig_bg))
            self.root.after(1500, self.refresh_ui)
        self.root.after(10000, self.glitch_rutina)

    def cifrar_texto(self, texto):
        # Cifrado sencillo XOR + Base64
        cifrado = "".join(chr(ord(c) ^ ord(self.passkey[i % len(self.passkey)])) for i, c in enumerate(texto))
        return base64.b64encode(cifrado.encode('utf-8')).decode('utf-8')

    def descifrar_texto(self, b64_texto):
        try:
            descifrado_bytes = base64.b64decode(b64_texto).decode('utf-8')
            return "".join(chr(ord(c) ^ ord(self.passkey[i % len(self.passkey)])) for i, c in enumerate(descifrado_bytes))
        except Exception:
            return b64_texto # Fallback: si no está codificado, devolver tal cual

    def protocolo_panico(self):
        """Bloqueo inmediato y minimización (Trigger: Escape)"""
        if not self.modo_cifrado:
            self.toggle_cifrado()
        self.root.iconify()

    def solicitar_cifrado(self):
        if not self.modo_cifrado:
            self.toggle_cifrado()
        else:
            self.abrir_ventana_password()

    def abrir_ventana_password(self):
        self.win_pass = tk.Toplevel(self.root)
        self.win_pass.title("AUTH")
        self.win_pass.geometry("250x120")
        self.win_pass.configure(bg="#050505")
        self.win_pass.attributes("-topmost", True)
        self.win_pass.resizable(False, False)
        
        tk.Label(self.win_pass, text="CLEARANCE CODE:", font=("Consolas", 9), bg="#050505", fg="#00FF00").pack(pady=10)
        self.entry_pass = tk.Entry(self.win_pass, bg="#000", fg="#00FF00", font=("Consolas", 10), insertbackground="#00FF00", show="*", relief="flat", justify="center")
        self.entry_pass.pack(pady=5)
        self.entry_pass.focus_set()
        self.entry_pass.bind("<Return>", lambda e: self.verificar_pass())

    def verificar_pass(self):
        if self.entry_pass.get() == self.passkey:
            self.win_pass.destroy()
            self.toggle_cifrado()
        else:
            self.entry_pass.delete(0, tk.END)
            self.status_bar.config(text=" !! ACCESS_DENIED !! ", fg="#FF0000")

    def toggle_cifrado(self):
        self.modo_cifrado = not self.modo_cifrado
        if self.modo_cifrado:
            self.area_texto.pack_forget()
            self.cli_frame.pack_forget()
            self.canvas_matrix.pack(fill='both', expand=True)
            self.canvas_matrix.update()
            
            width = self.canvas_matrix.winfo_width()
            font_size = 15
            columns = max(1, width // font_size)
            self.drops = [random.randint(-50, 0) for _ in range(columns)]
            
            self.btn_lock.config(text="[ UNLOCK_CORE ]", fg="#00FF00")
            self.run_matrix_animation()
        else:
            self.canvas_matrix.pack_forget()
            self.area_texto.pack(fill='both', expand=True)
            self.cli_frame.pack(fill='x')
            self.btn_lock.config(text="[ LOCK_CORE ]", fg="#FF0000")
            self.analizar_texto()

    def run_matrix_animation(self):
        if not self.modo_cifrado: return
        self.canvas_matrix.delete("all")
        height = self.canvas_matrix.winfo_height()
        font_size = 15
        for i in range(len(self.drops)):
            char = random.choice(self.matrix_chars)
            x, y = i * font_size, self.drops[i] * font_size
            color = "#FFFFFF" if random.random() > 0.97 else "#00FF41"
            self.canvas_matrix.create_text(x, y, text=char, fill=color, font=("Consolas", font_size))
            self.drops[i] += 1
            if y > height and random.random() > 0.95: self.drops[i] = 0
        self.root.after(50, self.run_matrix_animation)

    def cambiar_sector(self, nuevo_sector):
        if self.modo_cifrado: return
        self.guardar_notas()
        self.sector_actual = nuevo_sector
        self.actualizar_estilo_botones_sector()
        self.cargar_notas(efecto=True)

    def actualizar_estilo_botones_sector(self):
        for sec, btn in self.btn_sectores.items():
            if sec == self.sector_actual: btn.config(fg="#00FF00", font=("Consolas", 8, "bold"))
            else: btn.config(fg="#004400", font=("Consolas", 8))

    def actualizar_recursos(self):
        if PSUTIL_DISPONIBLE:
            cpu = int(psutil.cpu_percent(interval=None))
            ram = int(psutil.virtual_memory().percent)
        else:
            # Fallback en caso de no tener psutil instalado
            cpu = random.randint(5, 25)
            ram = random.randint(30, 45)
            
        def bar(val):
            filled = val // 10
            return f"[{'|'*filled}{' '*(10-filled)}]"
            
        self.cpu_label.config(text=f"CPU {bar(cpu)} {cpu:02d}%")
        self.ram_label.config(text=f"RAM {bar(ram)} {ram:02d}%")
        self.root.after(2000, self.actualizar_recursos)

    def dibujar_scanlines(self):
        self.main_container.delete("scanline")
        for i in range(0, 1200, 3):
            self.main_container.create_line(0, i, 1000, i, fill="#080808", tags="scanline", width=1)
        self.main_container.tag_lower("scanline")

    def refresh_ui(self, event=None):
        if not self.modo_cifrado: self.analizar_texto()
        texto = self.area_texto.get("1.0", tk.END)
        lineas = texto.count('\n')
        self.status_bar.config(text=f" -- ACTIVE -- | {self.sector_actual} | LNS: {lineas} | CHR: {len(texto)-1} ")

    def analizar_texto(self):
        for tag in ["urgente", "tarea", "hecho"]: self.area_texto.tag_remove(tag, "1.0", tk.END)
        self._aplicar_tag_a_linea("!!!", "urgente")
        self._aplicar_tag_a_linea(">>>", "tarea")
        self._aplicar_tag_a_linea("OK", "hecho")

    def _aplicar_tag_a_linea(self, patron, tag_name):
        start = "1.0"
        while True:
            pos = self.area_texto.search(patron, start, tk.END)
            if not pos: break
            idx = pos.split('.')[0]
            self.area_texto.tag_add(tag_name, f"{idx}.0", f"{idx}.end")
            start = f"{idx}.end"

    def toggle_transparencia(self):
        """Activa o desactiva la opacidad de la ventana (Trigger: Ctrl+T)"""
        self.es_transparente = not self.es_transparente
        self.root.attributes('-alpha', 0.6 if self.es_transparente else 1.0)

    def simular_logs(self):
        logs = ["UPLINK_ESTABLISHED", "SECTOR_SCAN...", "BUFFER_CLEARED", "CORE_SYNC", "FIREWALL_STABLE", "WARNING: TRACE DETECTED", "DDoS_PREVENTED"]
        self.log_feed.config(state="normal")
        color = "#004400"
        pick = random.choice(logs)
        if "WARNING" in pick: color = "#FF0000"
        self.log_feed.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {pick}\n")
        self.log_feed.see(tk.END)
        self.log_feed.config(state="disabled")
        self.root.after(random.randint(4000, 10000), self.simular_logs)

    def actualizar_reloj(self):
        self.lbl_reloj.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.actualizar_reloj)

    def auto_guardado_ciclo(self):
        self.guardar_notas()
        self.root.after(15000, self.auto_guardado_ciclo)

    def cargar_notas(self, efecto=False):
        fname = self.archivos[self.sector_actual]
        if os.path.exists(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    
                # Aplicar desencriptado transparente
                contenido_real = self.descifrar_texto(contenido)
                
                self.area_texto.delete("1.0", tk.END)
                self.area_texto.insert(tk.END, contenido_real)
                self.analizar_texto()
            except: pass

    def guardar_notas(self, event=None):
        if self.modo_cifrado: return 
        try:
            fname = self.archivos[self.sector_actual]
            contenido = self.area_texto.get("1.0", tk.END).rstrip('\n')
            
            # Aplicar encriptado antes de guardar al disco
            contenido_seguro = self.cifrar_texto(contenido)
            
            with open(fname, "w", encoding="utf-8") as f:
                f.write(contenido_seguro)
            self.status_bar.config(fg="#00FF00")
            self.root.after(200, lambda: self.status_bar.config(fg="#006600"))
        except: pass

    def guardar_y_cerrar(self):
        self.guardar_notas()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotasMatrixTerminal(root)
    root.mainloop()