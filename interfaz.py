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
        self.raiz.geometry("960x720")
        self.raiz.minsize(820, 600)

        self.maquina_lista = False
        self.datos = {}

        self._estilos()
        self._construir()

    # ----------------------------------------------------------------- estilo
    def _estilos(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=PALETA["fondo"], borderwidth=0)
        s.configure(
            "TNotebook.Tab", background=PALETA["rosa"],
            foreground=PALETA["texto"], font=(FUENTE, 11, "bold"),
            padding=(20, 10), borderwidth=0,
        )
        s.map(
            "TNotebook.Tab",
            background=[("selected", PALETA["lila"])],
            foreground=[("selected", "#ffffff")],
        )

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

    # ------------------------------------------------------------- estructura
    def _construir(self):
        cabecera = tk.Frame(self.raiz, bg=PALETA["lila"], height=70)
        cabecera.pack(fill="x")
        cabecera.pack_propagate(False)
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
            "Completa cada campo. Pasa el cursor sobre el simbolo (?) si tienes dudas.",
        )

        grid = tk.Frame(cont, bg=PALETA["fondo"])
        grid.pack(fill="x")

        campos = [
            ("Estados", "estados",
             "Todos los estados separados por espacios.  Ej:  q0 q1 q2 qf"),
            ("Estado inicial", "inicial",
             "Estado donde comienza la maquina.  Debe estar en la lista de estados.  Ej:  q0"),
            ("Estados finales", "finales",
             "Estados de aceptacion separados por espacios.  Ej:  qf"),
            ("Alfabeto de la cinta", "cinta",
             "Todos los simbolos que pueden aparecer en la cinta, incluido el blanco.  Ej:  0 1 X Y B"),
            ("Simbolo blanco", "blanco",
             "El simbolo que representa una celda vacia.  Debe estar en el alfabeto de la cinta.  Ej:  B"),
            ("Alfabeto de entrada", "entrada",
             "Simbolos validos en las palabras a evaluar (sin el blanco).  Ej:  0 1"),
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
        self._boton(
            fila, "▶ Evaluar", self._evaluar,
            color=PALETA["lila_oscuro"], ancho=12,
        ).pack(side="left", padx=8)
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
        self.cinta_canvas = tk.Canvas(
            cont, bg=PALETA["cinta_bg"], height=70, highlightthickness=2,
            highlightbackground=PALETA["borde"],
        )
        self.cinta_canvas.pack(fill="x", pady=(4, 12))

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
        # a^n b^n : reconoce cadenas con igual numero de a seguidas de b
        self._limpiar_definicion()
        ejemplo = {
            "estados": "q0 q1 q2 q3 qf",
            "inicial": "q0",
            "finales": "qf",
            "cinta": "a b X Y B",
            "blanco": "B",
            "entrada": "a b",
        }
        for clave, valor in ejemplo.items():
            self.campos[clave].insert(0, valor)

        trans = [
            "q0 a -> q1 X D",
            "q1 a -> q1 a D",
            "q1 Y -> q1 Y D",
            "q1 b -> q2 Y I",
            "q2 Y -> q2 Y I",
            "q2 a -> q2 a I",
            "q2 X -> q0 X D",
            "q0 Y -> q3 Y D",
            "q3 Y -> q3 Y D",
            "q3 B -> qf B D",
        ]
        for t in trans:
            self.transiciones_crudas.append(t)
            self.lista_trans.insert("end", "  " + t)

        messagebox.showinfo(
            "Ejemplo cargado",
            "Se cargo una maquina que reconoce el lenguaje  a^n b^n  (n >= 1).\n\n"
            "Construye la maquina y prueba palabras como  ab,  aabb,  aaabbb\n"
            "(aceptadas) frente a  aab  o  abb  (rechazadas).",
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
            estados = set(self.campos["estados"].get().strip().split())
            inicial = self.campos["inicial"].get().strip()
            finales = set(self.campos["finales"].get().strip().split())
            alf_cinta = set(self.campos["cinta"].get().strip().split())
            blanco = self.campos["blanco"].get().strip()
            alf_entrada = set(self.campos["entrada"].get().strip().split())

            if not estados:
                raise ValueError("Debes ingresar al menos un estado.")
            if inicial not in estados:
                raise ValueError("El estado inicial no esta en el conjunto de estados.")
            if not finales:
                raise ValueError("Debes ingresar al menos un estado final.")
            if not finales.issubset(estados):
                raise ValueError("Los estados finales deben pertenecer al conjunto de estados.")
            if not alf_cinta:
                raise ValueError("El alfabeto de la cinta no puede estar vacio.")
            if blanco not in alf_cinta:
                raise ValueError("El simbolo blanco debe estar en el alfabeto de la cinta.")
            if not alf_entrada:
                raise ValueError("El alfabeto de entrada no puede estar vacio.")
            if blanco in alf_entrada:
                raise ValueError("El alfabeto de entrada no puede incluir el simbolo blanco.")
            if not self.transiciones_crudas:
                raise ValueError("Debes ingresar al menos una transicion.")

            transiciones = {est: {} for est in estados}
            for crudo in self.transiciones_crudas:
                try:
                    ea, sl, ne, se, mv = self._parsear_transicion(crudo)
                except ValueError:
                    raise ValueError(f"Transicion con formato invalido:\n  {crudo}")
                if ea not in estados or ne not in estados:
                    raise ValueError(f"Estado inexistente en la transicion:\n  {crudo}")
                if sl not in alf_cinta or se not in alf_cinta:
                    raise ValueError(f"Simbolo fuera del alfabeto de la cinta:\n  {crudo}")
                if mv not in ("D", "I"):
                    raise ValueError(f"El movimiento debe ser D o I:\n  {crudo}")
                transiciones[ea][sl] = (ne, se, mv)

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
                f"Alfabeto de entrada: {{{', '.join(sorted(alf_entrada))}}}      "
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
        if not self.maquina_lista:
            return
        palabra = self.entry_palabra.get().strip()

        for c in palabra:
            if c not in self.datos["entrada"]:
                messagebox.showwarning(
                    "Caracter invalido",
                    f"El caracter '{c}' no pertenece al alfabeto de entrada.",
                )
                return

        aceptada, cinta = simular_mt(
            self.datos["inicial"],
            self.datos["finales"],
            self.datos["transiciones"],
            palabra,
            self.datos["blanco"],
        )

        mostrada = palabra if palabra else "ε (vacia)"
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

        self._dibujar_cinta(cinta, self.datos["blanco"])
        self._registrar(mostrada, aceptada, cinta)

    def _dibujar_cinta(self, cinta, blanco):
        self.cinta_canvas.delete("all")
        celdas = list(cinta) if cinta else [blanco]
        ancho = 46
        margen = 12
        y = 14
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
        total = margen * 2 + len(celdas) * ancho
        self.cinta_canvas.configure(scrollregion=(0, 0, total, 70))

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
