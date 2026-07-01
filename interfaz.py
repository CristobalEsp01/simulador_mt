import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from main import simular_mt


PALETA = {
    "fondo":        "#fbeef4",
    "panel":        "#ffffff",
    "lila":         "#cdb4f0",
    "lila_oscuro":  "#a988e0",
    "rosa":         "#f7c5dd",
    "rosa_fuerte":  "#e89cc0",
    "texto":        "#5a4a6a",
    "texto_suave":  "#8a7ba0",
    "borde":        "#e6d4ef",
    "ok":           "#6fbf8a",
    "no":           "#df8aa0",
    "cinta_bg":     "#fdf6fb",
}

FUENTE = "Segoe UI"
SIMBOLO_BLANCO = "B"  # fijo, igual que en main.py::ingresar_datos_mt_estricto


class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.tip = None
        widget.bind("<Enter>", self._mostrar)
        widget.bind("<Leave>", self._ocultar)

    def _mostrar(self, _=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(
            self.tip, text=self.texto, justify="left",
            background="#4a3a5a", foreground="white",
            font=(FUENTE, 9), padx=8, pady=5, wraplength=280,
        )
        lbl.pack()

    def _ocultar(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


class SimuladorApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Maquina de Turing  -  INFO 139")
        self.raiz.configure(bg=PALETA["fondo"])
        self.raiz.minsize(820, 600)
        self._centrar_ventana(960, 720)

        self.maquina_lista = False
        self.datos = {}

        self._estilos()
        self._construir()

    def _centrar_ventana(self, ancho, alto):
        self.raiz.update_idletasks()
        pantalla_w = self.raiz.winfo_screenwidth()
        pantalla_h = self.raiz.winfo_screenheight()
        x = max(0, (pantalla_w - ancho) // 2)
        y = max(0, (pantalla_h - alto) // 2 - 20)
        self.raiz.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ----------------------------------------------------------------- estilo
    def _estilos(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=PALETA["fondo"], borderwidth=0, tabmargins=(2, 2, 2, 0))
        s.configure(
            "TNotebook.Tab", background=PALETA["rosa"],
            foreground=PALETA["texto"], font=(FUENTE, 11, "bold"),
            padding=(20, 10), borderwidth=0,
        )
        s.map(
            "TNotebook.Tab",
            background=[("selected", PALETA["lila"])],
            foreground=[("selected", "#ffffff")],
            # Por defecto 'clam' agranda la pestaña seleccionada para que
            # se solape con el panel de contenido. Lo anulamos para que
            # ambas pestañas midan siempre lo mismo, sin importar cual
            # este activa.
            expand=[("selected", (0, 0, 0, 0))],
        )
        # El layout por defecto de 'clam' dibuja un anillo de foco
        # (Notebook.focus) dentro de la pestaña activa, lo que le resta
        # espacio de padding y la hace ver mas chica que la inactiva.
        # Redefinimos el layout sin ese elemento para que ambas pestañas
        # midan exactamente lo mismo.
        s.layout("TNotebook.Tab", [
            ("Notebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("Notebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("Notebook.label", {"side": "top", "sticky": ""}),
                        ],
                    }),
                ],
            }),
        ])

    def _titulo(self, padre, texto, sub=None):
        cont = tk.Frame(padre, bg=PALETA["fondo"])
        cont.pack(fill="x", pady=(4, 10))
        tk.Label(
            cont, text=texto, bg=PALETA["fondo"], fg=PALETA["texto"],
            font=(FUENTE, 15, "bold"),
        ).pack(anchor="w")
        if sub:
            tk.Label(
                cont, text=sub, bg=PALETA["fondo"], fg=PALETA["texto_suave"],
                font=(FUENTE, 10), justify="left",
            ).pack(anchor="w", pady=(2, 0))
        return cont

    def _boton(self, padre, texto, comando, color=None, ancho=14):
        color = color or PALETA["lila"]
        b = tk.Button(
            padre, text=texto, command=comando,
            bg=color, fg="white", font=(FUENTE, 10, "bold"),
            relief="flat", cursor="hand2", padx=10, pady=8,
            activebackground=PALETA["lila_oscuro"], activeforeground="white",
            width=ancho, bd=0,
        )
        def _hover_in(_):  b.configure(bg=PALETA["lila_oscuro"])
        def _hover_out(_): b.configure(bg=color)
        b.bind("<Enter>", _hover_in)
        b.bind("<Leave>", _hover_out)
        return b

    def _entrada(self, padre, ancho=40):
        e = tk.Entry(
            padre, font=(FUENTE, 11), bg="white", fg=PALETA["texto"],
            relief="flat", highlightthickness=2,
            highlightbackground=PALETA["borde"],
            highlightcolor=PALETA["lila"], width=ancho,
        )
        return e

    def _dibujar_gatito(self, canvas, cx, cy, tam=14, cuerpo="#f3ead6", puntos="#6b4a3a",
                         mejillas="#f6b8c9", ojos="#5ec3ea"):
        """Dibuja un gatito siames tierno con formas vectoriales (ovalos y
        triangulos): cuerpo color crema, 'puntos' oscuros en orejas/mascara/
        nariz (la marca caracteristica de la raza) y ojos azules. No depende
        de fuentes de emoji, asi se ve igual en cualquier sistema."""
        t = tam

        # orejas (siames: solidas, del color oscuro de los "puntos")
        for lado in (-1, 1):
            canvas.create_polygon(
                cx + lado * t * 0.85, cy - t * 0.25,
                cx + lado * t * 0.30, cy - t * 1.35,
                cx + lado * t * 0.05, cy - t * 0.45,
                fill=puntos, outline=puntos, width=1,
            )

        # cabeza (base crema)
        canvas.create_oval(
            cx - t, cy - t * 0.55, cx + t, cy + t * 0.95,
            fill=cuerpo, outline="#e0d2b8", width=1,
        )

        # mascara oscura alrededor de los ojos (tipico del siames)
        canvas.create_oval(
            cx - t * 0.68, cy - t * 0.12, cx + t * 0.68, cy + t * 0.40,
            fill=puntos, outline="",
        )

        # mejillas sonrosadas (se asoman bajo la mascara)
        canvas.create_oval(
            cx - t * 0.85, cy + t * 0.18, cx - t * 0.35, cy + t * 0.55,
            fill=mejillas, outline="",
        )
        canvas.create_oval(
            cx + t * 0.35, cy + t * 0.18, cx + t * 0.85, cy + t * 0.55,
            fill=mejillas, outline="",
        )

        # ojitos azules almendrados (marca distintiva del siames)
        canvas.create_oval(
            cx - t * 0.45, cy - t * 0.02, cx - t * 0.16, cy + t * 0.26,
            fill=ojos, outline="",
        )
        canvas.create_oval(
            cx + t * 0.16, cy - t * 0.02, cx + t * 0.45, cy + t * 0.26,
            fill=ojos, outline="",
        )
        # pupilas
        canvas.create_oval(
            cx - t * 0.35, cy + t * 0.02, cx - t * 0.24, cy + t * 0.20,
            fill=PALETA["texto"], outline="",
        )
        canvas.create_oval(
            cx + t * 0.24, cy + t * 0.02, cx + t * 0.35, cy + t * 0.20,
            fill=PALETA["texto"], outline="",
        )
        # brillito en los ojos
        canvas.create_oval(
            cx - t * 0.33, cy + t * 0.00, cx - t * 0.25, cy + t * 0.08,
            fill="white", outline="",
        )
        canvas.create_oval(
            cx + t * 0.26, cy + t * 0.00, cx + t * 0.34, cy + t * 0.08,
            fill="white", outline="",
        )

        # nariz (tambien de color "punto")
        canvas.create_polygon(
            cx - t * 0.10, cy + t * 0.32,
            cx + t * 0.10, cy + t * 0.32,
            cx, cy + t * 0.45,
            fill=puntos, outline="",
        )

        # bigotes
        for lado in (-1, 1):
            canvas.create_line(
                cx + lado * t * 0.45, cy + t * 0.40,
                cx + lado * t * 1.25, cy + t * 0.30,
                fill="#c9b79a", width=1,
            )
            canvas.create_line(
                cx + lado * t * 0.45, cy + t * 0.50,
                cx + lado * t * 1.25, cy + t * 0.50,
                fill="#c9b79a", width=1,
            )

    # ------------------------------------------------------------- estructura
    def _construir(self):
        cabecera = tk.Frame(self.raiz, bg=PALETA["lila"], height=70)
        cabecera.pack(fill="x")
        cabecera.pack_propagate(False)
        gato_header = tk.Canvas(
            cabecera, width=54, height=54, bg=PALETA["lila"], highlightthickness=0,
        )
        gato_header.pack(side="right", padx=18)
        self._dibujar_gatito(gato_header, 27, 30, tam=14)
        tk.Label(
            cabecera, text="✿  Maquina de Turing", bg=PALETA["lila"],
            fg="white", font=(FUENTE, 20, "bold"),
        ).pack(side="left", padx=24)
        tk.Label(
            cabecera, text="Reconocedora de lenguajes · cinta semi-infinita",
            bg=PALETA["lila"], fg="#f3e9ff", font=(FUENTE, 10),
        ).pack(side="left", pady=(14, 0))

        self.nb = ttk.Notebook(self.raiz)
        self.nb.pack(fill="both", expand=True, padx=16, pady=14)

        self.tab_def = tk.Frame(self.nb, bg=PALETA["fondo"])
        self.tab_sim = tk.Frame(self.nb, bg=PALETA["fondo"])
        self.nb.add(self.tab_def, text="  1 · Definir maquina  ")
        self.nb.add(self.tab_sim, text="  2 · Evaluar palabras  ")
        self.nb.tab(1, state="disabled")

        self._tab_definicion()
        self._tab_simulacion()

        # --- gatitos de decoracion (no interfieren con la logica ni el scroll) ---
        gato_esq1 = tk.Canvas(
            self.tab_def, width=42, height=42, bg=PALETA["fondo"], highlightthickness=0,
        )
        gato_esq1.place(relx=1.0, rely=0.0, anchor="ne", x=-34, y=8)
        self._dibujar_gatito(gato_esq1, 21, 24, tam=11)

        gato_esq2 = tk.Canvas(
            self.tab_def, width=42, height=42, bg=PALETA["fondo"], highlightthickness=0,
        )
        gato_esq2.place(relx=0.0, rely=1.0, anchor="sw", x=8, y=-8)
        self._dibujar_gatito(gato_esq2, 21, 24, tam=11)

    # ------------------------------------------------------------- pestaña 1
    def _tab_definicion(self):
        lienzo = tk.Canvas(self.tab_def, bg=PALETA["fondo"], highlightthickness=0)
        barra = tk.Scrollbar(self.tab_def, orient="vertical", command=lienzo.yview)
        lienzo.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        lienzo.pack(side="left", fill="both", expand=True)

        cont = tk.Frame(lienzo, bg=PALETA["fondo"])
        ventana = lienzo.create_window((0, 0), window=cont, anchor="nw")

        def _ajustar(_=None):
            lienzo.configure(scrollregion=lienzo.bbox("all"))
            lienzo.itemconfig(ventana, width=lienzo.winfo_width())
        cont.bind("<Configure>", _ajustar)
        lienzo.bind("<Configure>", _ajustar)
        lienzo.bind_all("<Button-4>", lambda e: lienzo.yview_scroll(-1, "units"))
        lienzo.bind_all("<Button-5>", lambda e: lienzo.yview_scroll(1, "units"))

        cont = tk.Frame(cont, bg=PALETA["fondo"])
        cont.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._titulo(
            cont, "Define los componentes de tu maquina",
            "Completa cada campo. Pasa el cursor sobre el simbolo (?) si tienes dudas.\n"
            "Los estados, el alfabeto de la cinta, el alfabeto de entrada y el simbolo "
            "blanco se infieren automaticamente a partir de las transiciones.",
        )

        grid = tk.Frame(cont, bg=PALETA["fondo"])
        grid.pack(fill="x")

        campos = [
            ("Estado inicial", "inicial",
             "Estado donde comienza la maquina.  Ej:  q0"),
            ("Estados finales", "finales",
             "Estados de aceptacion separados por espacios.  Ej:  qf"),
        ]

        self.campos = {}
        for fila, (etq, clave, ayuda) in enumerate(campos):
            f = tk.Frame(grid, bg=PALETA["fondo"])
            f.grid(row=fila, column=0, sticky="w", pady=7)

            lbl_box = tk.Frame(f, bg=PALETA["fondo"])
            lbl_box.pack(anchor="w")
            tk.Label(
                lbl_box, text=etq, bg=PALETA["fondo"], fg=PALETA["texto"],
                font=(FUENTE, 11, "bold"), width=20, anchor="w",
            ).pack(side="left")
            ayuda_lbl = tk.Label(
                lbl_box, text=" (?) ", bg=PALETA["rosa"], fg=PALETA["texto"],
                font=(FUENTE, 9, "bold"), cursor="question_arrow",
            )
            ayuda_lbl.pack(side="left", padx=(4, 0))
            Tooltip(ayuda_lbl, ayuda)

            e = self._entrada(f, ancho=46)
            e.pack(anchor="w", pady=(4, 0))
            self.campos[clave] = e

        # transiciones
        self._titulo(
            cont, "Transiciones",
            "Formato:  estado  simbolo  ->  nuevo_estado  simbolo_escrito  movimiento\n"
            "El movimiento es D (derecha) o I (izquierda).   Ej:  q0 1 -> q1 X D",
        )

        trans_box = tk.Frame(cont, bg=PALETA["fondo"])
        trans_box.pack(fill="x", pady=(0, 6))

        entrada_trans = tk.Frame(trans_box, bg=PALETA["fondo"])
        entrada_trans.pack(fill="x")
        self.entry_trans = self._entrada(entrada_trans, ancho=40)
        self.entry_trans.pack(side="left", ipady=2)
        self.entry_trans.bind("<Return>", lambda _: self._agregar_transicion())
        self._boton(
            entrada_trans, "+ Agregar", self._agregar_transicion,
            color=PALETA["rosa_fuerte"], ancho=12,
        ).pack(side="left", padx=8)
        self._boton(
            entrada_trans, "Quitar sel.", self._quitar_transicion,
            color=PALETA["lila"], ancho=12,
        ).pack(side="left")

        lista_frame = tk.Frame(
            cont, bg=PALETA["panel"], highlightthickness=2,
            highlightbackground=PALETA["borde"],
        )
        lista_frame.pack(fill="both", expand=True, pady=(8, 6))
        self.lista_trans = tk.Listbox(
            lista_frame, font=("Consolas", 11), bg=PALETA["panel"],
            fg=PALETA["texto"], relief="flat", selectbackground=PALETA["lila"],
            selectforeground="white", height=7, activestyle="none",
            highlightthickness=0,
        )
        self.lista_trans.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb = tk.Scrollbar(lista_frame, command=self.lista_trans.yview)
        sb.pack(side="right", fill="y")
        self.lista_trans.config(yscrollcommand=sb.set)
        self.transiciones_crudas = []

        barra = tk.Frame(cont, bg=PALETA["fondo"])
        barra.pack(fill="x", pady=(6, 4))
        self._boton(
            barra, "✓ Construir maquina", self._construir_maquina,
            color=PALETA["lila_oscuro"], ancho=20,
        ).pack(side="left")
        self._boton(
            barra, "Cargar ejemplo", self._cargar_ejemplo,
            color=PALETA["rosa_fuerte"], ancho=16,
        ).pack(side="left", padx=8)
        self._boton(
            barra, "Limpiar todo", self._limpiar_definicion,
            color=PALETA["rosa"], ancho=14,
        ).pack(side="left")

    # ------------------------------------------------------------- pestaña 2
    def _tab_simulacion(self):
        cont = tk.Frame(self.tab_sim, bg=PALETA["fondo"])
        cont.pack(fill="both", expand=True, padx=20, pady=10)

        self.resumen_lbl = tk.Label(
            cont, text="", bg=PALETA["fondo"], fg=PALETA["texto_suave"],
            font=(FUENTE, 10), justify="left", anchor="w",
        )
        self.resumen_lbl.pack(fill="x", pady=(0, 8))

        self._titulo(
            cont, "Evalua una palabra",
            "Escribe una palabra usando solo el alfabeto de entrada y presiona Evaluar.",
        )

        fila = tk.Frame(cont, bg=PALETA["fondo"])
        fila.pack(fill="x", pady=(0, 10))
        self.entry_palabra = self._entrada(fila, ancho=34)
        self.entry_palabra.pack(side="left", ipady=4)
        self.entry_palabra.bind("<Return>", lambda _: self._evaluar())
        self.btn_evaluar = self._boton(
            fila, "▶ Evaluar", self._evaluar,
            color=PALETA["lila_oscuro"], ancho=12,
        )
        self.btn_evaluar.pack(side="left", padx=8)
        tk.Label(
            fila, text="(la palabra vacia se evalua dejando el campo en blanco)",
            bg=PALETA["fondo"], fg=PALETA["texto_suave"], font=(FUENTE, 9),
        ).pack(side="left", padx=4)

        # tarjeta de resultado
        self.tarjeta = tk.Frame(
            cont, bg=PALETA["panel"], highlightthickness=2,
            highlightbackground=PALETA["borde"],
        )
        self.tarjeta.pack(fill="x", pady=(0, 12))
        self.resultado_lbl = tk.Label(
            self.tarjeta, text="Aun no has evaluado ninguna palabra.",
            bg=PALETA["panel"], fg=PALETA["texto_suave"],
            font=(FUENTE, 13, "bold"), pady=18,
        )
        self.resultado_lbl.pack()

        cinta_titulo = tk.Label(
            cont, text="Cinta final", bg=PALETA["fondo"], fg=PALETA["texto"],
            font=(FUENTE, 11, "bold"),
        )
        cinta_titulo.pack(anchor="w")
        cinta_frame = tk.Frame(
            cont, bg=PALETA["cinta_bg"], highlightthickness=2,
            highlightbackground=PALETA["borde"],
        )
        cinta_frame.pack(fill="x", pady=(4, 12))
        self.cinta_canvas = tk.Canvas(
            cinta_frame, bg=PALETA["cinta_bg"], height=100, highlightthickness=0,
        )
        cinta_scroll = tk.Scrollbar(
            cinta_frame, orient="horizontal", command=self.cinta_canvas.xview,
        )
        self.cinta_canvas.configure(xscrollcommand=cinta_scroll.set)
        self.cinta_canvas.pack(fill="x", side="top")
        cinta_scroll.pack(fill="x", side="bottom")

        tk.Label(
            cont, text="Historial", bg=PALETA["fondo"], fg=PALETA["texto"],
            font=(FUENTE, 11, "bold"),
        ).pack(anchor="w")
        self.historial = scrolledtext.ScrolledText(
            cont, font=("Consolas", 10), bg=PALETA["panel"],
            fg=PALETA["texto"], relief="flat", height=8,
            highlightthickness=2, highlightbackground=PALETA["borde"],
        )
        self.historial.pack(fill="both", expand=True)
        self.historial.configure(state="disabled")

        botones = tk.Frame(cont, bg=PALETA["fondo"])
        botones.pack(fill="x", pady=(8, 0))
        self._boton(
            botones, "← Volver a definir", lambda: self.nb.select(0),
            color=PALETA["rosa"], ancho=18,
        ).pack(side="left")
        self._boton(
            botones, "Limpiar historial", self._limpiar_historial,
            color=PALETA["lila"], ancho=16,
        ).pack(side="left", padx=8)

    # ----------------------------------------------------------- acciones t1
    def _agregar_transicion(self):
        txt = self.entry_trans.get().strip()
        if not txt:
            return
        self.transiciones_crudas.append(txt)
        self.lista_trans.insert("end", "  " + txt)
        self.entry_trans.delete(0, "end")

    def _quitar_transicion(self):
        sel = self.lista_trans.curselection()
        if not sel:
            return
        idx = sel[0]
        self.lista_trans.delete(idx)
        del self.transiciones_crudas[idx]

    def _limpiar_definicion(self):
        for e in self.campos.values():
            e.delete(0, "end")
        self.entry_trans.delete(0, "end")
        self.lista_trans.delete(0, "end")
        self.transiciones_crudas.clear()

    def _cargar_ejemplo(self):
        # Cadenas binarias con una cantidad PAR de 1s (incluye la cadena vacia).
        # Maquina de una sola pasada: el estado inicial lee directamente todo
        # el alfabeto de entrada, por lo que la inferencia automatica
        # (estados, alfabeto de cinta, alfabeto de entrada) funciona sin ambiguedad.
        self._limpiar_definicion()
        ejemplo = {
            "inicial": "q0",
            "finales": "qf",
        }
        for clave, valor in ejemplo.items():
            self.campos[clave].insert(0, valor)

        trans = [
            "q0 0 -> q0 0 D",
            "q0 1 -> q1 1 D",
            "q1 0 -> q1 0 D",
            "q1 1 -> q0 1 D",
            "q0 B -> qf B D",
        ]
        for t in trans:
            self.transiciones_crudas.append(t)
            self.lista_trans.insert("end", "  " + t)

        messagebox.showinfo(
            "Ejemplo cargado",
            "Se cargo una maquina que reconoce cadenas binarias con una cantidad\n"
            "PAR de 1s (la cadena vacia tambien se acepta, ya que tiene cero 1s).\n\n"
            "Construye la maquina y prueba palabras como  11,  1100,  0000\n"
            "(aceptadas) frente a  1,  100,  111  (rechazadas).",
        )

    def _parsear_transicion(self, txt):
        if "->" in txt:
            izq, der = txt.split("->")
            est_act, sim_lei = izq.strip().split()
            n_est, sim_esc, mov = der.strip().split()
        else:
            est_act, sim_lei, n_est, sim_esc, mov = txt.split()
        return est_act, sim_lei, n_est, sim_esc, mov.upper()

    def _construir_maquina(self):
        try:
            inicial = self.campos["inicial"].get().strip()
            finales = set(self.campos["finales"].get().strip().split())
            blanco = SIMBOLO_BLANCO

            if not inicial:
                raise ValueError("Debes ingresar el estado inicial.")
            if not finales:
                raise ValueError("Debes ingresar al menos un estado final.")
            if not self.transiciones_crudas:
                raise ValueError("Debes ingresar al menos una transicion.")

            transiciones = {}
            estados = {inicial} | finales
            alf_cinta = {blanco}

            for crudo in self.transiciones_crudas:
                try:
                    ea, sl, ne, se, mv = self._parsear_transicion(crudo)
                except ValueError:
                    raise ValueError(f"Transicion con formato invalido:\n  {crudo}")
                if mv not in ("D", "I"):
                    raise ValueError(f"El movimiento debe ser D o I:\n  {crudo}")

                estados.add(ea)
                estados.add(ne)
                alf_cinta.add(sl)
                alf_cinta.add(se)

                transiciones.setdefault(ea, {})[sl] = (ne, se, mv)

            if inicial not in estados:
                raise ValueError("El estado inicial debe aparecer en al menos una transicion.")
            if not finales.issubset(estados):
                raise ValueError(
                    "Los estados finales deben aparecer en las transiciones (como origen o destino)."
                )

            # Alfabeto de entrada: simbolos que el estado inicial es capaz de leer
            # directamente, excluyendo el blanco (misma inferencia que main.py).
            alf_entrada = set()
            if inicial in transiciones:
                alf_entrada = {s for s in transiciones[inicial].keys() if s != blanco}
            if not alf_entrada:
                alf_entrada = {s for s in alf_cinta if s not in (blanco, "X", "Y")}

        except ValueError as err:
            messagebox.showerror("Revisa la definicion", str(err))
            return

        self.datos = {
            "inicial": inicial,
            "finales": finales,
            "transiciones": transiciones,
            "entrada": alf_entrada,
            "blanco": blanco,
        }
        self.maquina_lista = True

        self.resumen_lbl.config(
            text=(
                f"Estado inicial: {inicial}      "
                f"Finales: {{{', '.join(sorted(finales))}}}      "
                f"Blanco: {blanco}\n"
                f"Estados detectados: {{{', '.join(sorted(estados))}}}\n"
                f"Alfabeto de entrada (inferido): {{{', '.join(sorted(alf_entrada))}}}      "
                f"Transiciones: {len(self.transiciones_crudas)}"
            )
        )

        self.nb.tab(1, state="normal")
        self.nb.select(1)
        self.entry_palabra.focus_set()
        messagebox.showinfo(
            "Maquina lista",
            "La maquina se construyo correctamente.\n"
            "Ya puedes evaluar todas las palabras que quieras.",
        )

    # ----------------------------------------------------------- acciones t2
    def _evaluar(self):
        if not self.maquina_lista or getattr(self, "_animando", False):
            return
        palabra = self.entry_palabra.get().strip()

        for c in palabra:
            if c not in self.datos["entrada"]:
                messagebox.showwarning(
                    "Caracter invalido",
                    f"El caracter '{c}' no pertenece al alfabeto de entrada.",
                )
                return

        # El veredicto ACEPTADA/RECHAZADA y la cinta final salen exclusivamente
        # de tu logica original en main.py -- eso no se toca.
        aceptada, cinta_final = simular_mt(
            self.datos["inicial"],
            self.datos["finales"],
            self.datos["transiciones"],
            palabra,
            self.datos["blanco"],
        )
        mostrada = palabra if palabra else "ε (vacia)"

        # Traza de pasos SOLO para animar al gatito; es un espejo visual del
        # mismo algoritmo, no reemplaza ni altera el resultado de simular_mt.
        pasos = self._generar_pasos(
            self.datos["inicial"], self.datos["finales"],
            self.datos["transiciones"], palabra, self.datos["blanco"],
        )

        self.tarjeta.config(highlightbackground=PALETA["borde"])
        self.resultado_lbl.config(text="Caminando por la cinta...", fg=PALETA["texto_suave"])

        self._animar_gato(pasos, 0, aceptada, cinta_final, mostrada)

    def _generar_pasos(self, inicial, finales, transiciones, palabra, blanco, tope=400):
        """Reproduce el mismo algoritmo de main.py::simular_mt paso a paso,
        solo para poder animar al gatito. No decide aceptacion/rechazo."""
        cinta = list(palabra) if palabra != "" else [blanco]
        cabezal = 0
        estado = inicial
        pasos = [{"cinta": cinta.copy(), "cabezal": cabezal}]
        historial = set()

        while estado not in finales and len(pasos) <= tope:
            cinta_str = "".join(cinta)
            config = (cinta_str, cabezal, estado)
            if config in historial:
                break
            historial.add(config)

            if cabezal >= len(cinta):
                cinta.append(blanco)
            elif cabezal < 0:
                break

            simbolo = cinta[cabezal]
            if estado in transiciones and simbolo in transiciones[estado]:
                nuevo_estado, simbolo_escrito, movimiento = transiciones[estado][simbolo]
                cinta[cabezal] = simbolo_escrito
                estado = nuevo_estado
                cabezal += 1 if movimiento == "D" else -1
                pasos.append({"cinta": cinta.copy(), "cabezal": cabezal})
            else:
                break

        # Si la traza es muy larga, la resumimos para que la animacion no
        # se demore una eternidad (esto es solo cosmetico).
        MAX_CUADROS = 60
        if len(pasos) > MAX_CUADROS:
            paso = len(pasos) / MAX_CUADROS
            indices = sorted({int(i * paso) for i in range(MAX_CUADROS)} | {len(pasos) - 1})
            pasos = [pasos[i] for i in indices]

        return pasos

    def _animar_gato(self, pasos, indice, aceptada, cinta_final, mostrada):
        self._animando = True
        self.btn_evaluar.config(state="disabled")

        frame = pasos[indice]
        es_ultimo = indice == len(pasos) - 1
        self._dibujar_cinta(
            frame["cinta"], self.datos["blanco"],
            cabezal=frame["cabezal"], caminando=(not es_ultimo) and (indice % 2 == 0),
        )

        if not es_ultimo:
            self.raiz.after(
                220, lambda: self._animar_gato(pasos, indice + 1, aceptada, cinta_final, mostrada)
            )
            return

        # Fin de la animacion: mostramos el veredicto real ya calculado.
        if aceptada:
            self.tarjeta.config(highlightbackground=PALETA["ok"])
            self.resultado_lbl.config(
                text=f"✓  ACEPTADA\n'{mostrada}' pertenece al lenguaje",
                fg=PALETA["ok"],
            )
        else:
            self.tarjeta.config(highlightbackground=PALETA["no"])
            self.resultado_lbl.config(
                text=f"✕  RECHAZADA\n'{mostrada}' no pertenece al lenguaje",
                fg=PALETA["no"],
            )

        # Redibujamos con el ultimo cuadro de la propia animacion (en vez de
        # la cinta "recortada" de simular_mt) para que el gatito se quede
        # sentado justo donde termino, en lugar de desaparecer.
        self._dibujar_cinta(
            frame["cinta"], self.datos["blanco"], cabezal=frame["cabezal"], caminando=False,
        )
        self._registrar(mostrada, aceptada, cinta_final)

        self.btn_evaluar.config(state="normal")
        self._animando = False

    def _dibujar_cinta(self, cinta, blanco, cabezal=None, caminando=False):
        self.cinta_canvas.delete("all")
        celdas = list(cinta) if cinta else [blanco]
        ancho = 46
        margen = 12
        y = 46

        for i, simbolo in enumerate(celdas):
            x = margen + i * ancho
            self.cinta_canvas.create_rectangle(
                x, y, x + ancho - 4, y + 40,
                fill="white", outline=PALETA["lila"], width=2,
            )
            self.cinta_canvas.create_text(
                x + (ancho - 4) / 2, y + 20, text=simbolo,
                font=("Consolas", 14, "bold"), fill=PALETA["texto"],
            )

        cx = None
        if cabezal is not None:
            idx = max(0, min(cabezal, len(celdas) - 1))
            cx = margen + idx * ancho + (ancho - 4) / 2
            cy = (y - 22) - (4 if caminando else 0)  # pequeno salto al "caminar"
            self._dibujar_gatito(self.cinta_canvas, cx, cy, tam=13)

        total = margen * 2 + len(celdas) * ancho
        ancho_visible = max(self.cinta_canvas.winfo_width(), 1)
        self.cinta_canvas.configure(scrollregion=(0, 0, max(total, ancho_visible), 90))

        if cx is not None:
            # mantiene al gatito visible mientras camina por cintas largas
            frac = max(0.0, min(1.0, (cx - ancho_visible / 2) / max(total, 1)))
            self.cinta_canvas.xview_moveto(frac)
        else:
            self.cinta_canvas.xview_moveto(0)

    def _registrar(self, palabra, aceptada, cinta):
        estado = "ACEPTADA" if aceptada else "RECHAZADA"
        linea = f"{palabra:<18} →  {estado:<10} cinta: '{cinta}'\n"
        self.historial.configure(state="normal")
        self.historial.insert("end", linea)
        self.historial.see("end")
        self.historial.configure(state="disabled")

    def _limpiar_historial(self):
        self.historial.configure(state="normal")
        self.historial.delete("1.0", "end")
        self.historial.configure(state="disabled")


def main():
    raiz = tk.Tk()
    SimuladorApp(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()