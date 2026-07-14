import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium", app_title="Estadística Inferencial — Cuaderno Interactivo")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    plt.rcParams.update({
        "_figure._figsize": (7.2, 4.0),
        "_figure.dpi": 120,
        "_figure.facecolor": "white",
        "_axes.facecolor": "white",
        "_axes.spines.top": False,
        "_axes.spines.right": False,
        "_axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.8,
        "font.size": 11,
        "_axes.titlesize": 12,
        "_axes.titleweight": "bold",
        "_axes.labelsize": 10.5,
        "_legend.frameon": False,
        "_legend.fontsize": 9.5,
    })

    # Paleta consistente para todo el cuaderno
    C = {
        "primary": "#2563eb",   # azul
        "accent":  "#f59e0b",   # ámbar
        "danger":  "#dc2626",   # rojo
        "success": "#16a34a",   # verde
        "purple":  "#7c3aed",
        "slate":   "#334155",
        "muted":   "#94a3b8",
    }

    def new_ax(_figsize=(7.2, 4.0)):
        _fig, _ax = plt.subplots(_figsize=_figsize)
        return _fig, _ax

    return C, new_ax, np, plt, stats


@app.cell
def _(mo):
    mo.md(
        r"""
        # 📊 Estadística Inferencial — Laboratorio Interactivo

        > Un cuaderno reactivo para **entender inferencia estadística tocándola**: mueves un control,
        > y las fórmulas, gráficas y decisiones se recalculan al instante.

        **Cómo usarlo.** marimo es *reactivo*: no hay que "correr celdas" en orden. Cambia cualquier
        *slider* o *dropdown* y todo lo que depende de él se actualiza solo. Las fórmulas en $\LaTeX$
        muestran **los valores actuales del simulador**, no símbolos abstractos.

        **Ruta pedagógica** (cada tema motiva al siguiente):

        1. **Inferencia estadística** — de la muestra a la población (Teorema del Límite Central).
        2. **Distribuciones** — Bernoulli, Binomial, Poisson, Uniforme, Normal.
        3. **Significancia, valor $p$ y tolerancia de riesgo** — $\alpha$, errores Tipo I/II, potencia.
        4. **Pruebas estadísticas** — qué prueba para qué distribución.
        5. **Regresión** — lineal y logística.
        6. **Correlación y causalidad** — por qué no son lo mismo.

        A lo largo del camino: 🧠 *intuición*, ⚠️ *trampas comunes*, ❓ *preguntas socráticas* y
        mini-*quizzes* de autoevaluación.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 1. ESTADÍSTICA INFERENCIAL
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1 · Estadística Inferencial

        La **estadística descriptiva** resume lo que *ya tienes*. La **estadística inferencial**
        da el salto arriesgado: usar una **muestra** para decir algo sobre una **población** que
        nunca observaste por completo.

        | Concepto | Población | Muestra |
        |---|---|---|
        | Qué es | todo el universo de interés | subconjunto que sí medimos |
        | Media | $\mu$ (parámetro, fijo/desconocido) | $\bar{x}$ (estadístico, aleatorio) |
        | Desv. | $\sigma$ | $s$ |

        Un **estimador** ($\bar{x}$) es una variable aleatoria: si tomaras *otra* muestra, saldría
        distinto. Esa variabilidad es el **error de muestreo**, y su magnitud es el **error estándar**:

        $$\mathrm{SE}(\bar{x}) = \frac{\sigma}{\sqrt{n}}$$

        La pieza que hace posible **toda** la inferencia clásica es el **Teorema del Límite Central (TLC)**:

        > Sin importar la forma de la población, la distribución de $\bar{x}$ tiende a una **Normal**
        > $\mathcal{N}\!\left(\mu,\ \sigma^2/n\right)$ cuando $n$ crece.

        ❓ *Pregunta socrática:* si la población es sesgadísima (p. ej. exponencial), ¿qué tiene que
        pasar con $n$ para que $\bar{x}$ ya "parezca" normal? Compruébalo abajo.
        """
    )
    return


@app.cell
def _(mo):
    clt_pop = mo.ui.dropdown(
        options=["Uniforme(0,1)", "Exponencial(1)", "Binomial(10, 0.15) — sesgada", "Normal(0,1)"],
        value="Exponencial(1)",
        label="Población de origen",
    )
    clt_n = mo.ui.slider(1, 200, value=5, step=1, label="Tamaño de muestra $n$", show_value=True)
    clt_reps = mo.ui.slider(200, 5000, value=2000, step=100, label="N.º de muestras", show_value=True)
    clt_seed = mo.ui.slider(0, 40, value=0, step=1, label="Semilla (re-muestrear)", show_value=True)

    controls_clt = mo.vstack([
        mo.md("**Controles — TLC**"),
        clt_pop,
        clt_n,
        clt_reps,
        clt_seed,
    ])
    controls_clt
    return clt_n, clt_pop, clt_reps, clt_seed


@app.cell
def _(C, clt_n, clt_pop, clt_reps, clt_seed, new_ax, np, stats):
    _rng = np.random.default_rng(int(clt_seed.value))
    _n = int(clt_n.value)
    _reps = int(clt_reps.value)

    # Muestreo + parámetros teóricos de la población
    if clt_pop.value.startswith("Uniforme"):
        _samples = _rng.uniform(0, 1, size=(_reps, _n))
        _mu, _sigma = 0.5, np.sqrt(1 / 12)
    elif clt_pop.value.startswith("Exponencial"):
        _samples = _rng.exponential(1.0, size=(_reps, _n))
        _mu, _sigma = 1.0, 1.0
    elif clt_pop.value.startswith("Binomial"):
        _samples = _rng.binomial(10, 0.15, size=(_reps, _n)).astype(float)
        _mu, _sigma = 1.5, np.sqrt(10 * 0.15 * 0.85)
    else:  # Normal
        _samples = _rng.normal(0, 1, size=(_reps, _n))
        _mu, _sigma = 0.0, 1.0

    clt_means = _samples.mean(axis=1)
    clt_se_theory = _sigma / np.sqrt(_n)
    clt_se_emp = clt_means.std(ddof=1)
    clt_mean_emp = clt_means.mean()
    clt_mu = _mu

    _fig, (axL, _axR) = new_ax(_figsize=(9.2, 3.6))
    _fig.subplots_adjust(wspace=0.28)

    # Izq: población
    _pop_draw = _samples.ravel()
    axL.hist(_pop_draw, bins=40, density=True, color=C["muted"], alpha=0.75)
    axL.axvline(_mu, color=C["danger"], lw=2, label=fr"$\mu={_mu:.2f}$")
    axL.set_title("Población (una muestra grande)")
    axL.set_xlabel("valor"); axL.set_ylabel("densidad"); axL._legend()

    # Der: distribución muestral de la media
    axR.hist(clt_means, bins=40, density=True, color=C["primary"], alpha=0.65,
             label=r"$\bar{x}$ simulada")
    _xx = np.linspace(clt_means.min(), clt_means.max(), 300)
    axR.plot(_xx, stats.norm.pdf(_xx, _mu, clt_se_theory), color=C["accent"], lw=2.5,
             label=r"$\mathcal{N}(\mu,\ \sigma^2/n)$ teórica")
    axR.axvline(_mu, color=C["danger"], lw=2)
    axR.set_title(f"Distribución muestral de $\\bar{{x}}$  (n={_n})")
    axR.set_xlabel(r"$\bar{x}$"); axR.set_ylabel("densidad"); axR._legend()

    _fig
    return clt_mean_emp, clt_mu, clt_se_emp, clt_se_theory


@app.cell
def _(clt_mean_emp, clt_mu, clt_n, clt_se_emp, clt_se_theory, mo):
    mo.md(
        rf"""
        **Fórmula con tus valores actuales:**

        $$\mathrm{{SE}}(\bar{{x}})=\frac{{\sigma}}{{\sqrt{{n}}}}=\frac{{\sigma}}{{\sqrt{{{int(clt_n.value)}}}}}
        \;\approx\;{clt_se_theory:.4f}$$

        | Cantidad | Teórico | Simulado (empírico) |
        |---|---|---|
        | Media de $\bar{{x}}$ | $\mu = {clt_mu:.3f}$ | ${clt_mean_emp:.3f}$ |
        | Error estándar | ${clt_se_theory:.4f}$ | ${clt_se_emp:.4f}$ |

        🧠 **Intuición:** el histograma azul se vuelve **más estrecho y más normal** al subir $n$
        (el SE cae como $1/\sqrt{{n}}$: para reducirlo a la mitad necesitas **4×** los datos).
        Nota que la media muestral acierta en $\mu$ aunque la población sea muy asimétrica.
        """
    )
    return


@app.cell
def _(mo):
    quiz_clt = mo.ui.radio(
        options=[
            "Duplicar n reduce el error estándar a la mitad",
            "Cuadruplicar n reduce el error estándar a la mitad",
            "El error estándar no depende de n",
        ],
        label="❓ Para reducir el error estándar a la mitad, ¿qué hago con $n$?",
    )
    quiz_clt
    return (quiz_clt,)


@app.cell
def _(mo, quiz_clt):
    _ok = "Cuadruplicar n reduce el error estándar a la mitad"
    if quiz_clt.value is None:
        _out = mo.md("*Elige una opción.*")
    elif quiz_clt.value == _ok:
        _out = mo.callout(mo.md(r"✅ **Correcto.** Como $SE=\sigma/\sqrt{n}$, para mitad de SE necesitas $4n$."), kind="success")
    else:
        _out = mo.callout(mo.md(r"❌ Casi. El $\sqrt{n}$ en el denominador implica que hace falta **4×** los datos, no 2×."), kind="warn")
    _out
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 2. DISTRIBUCIONES
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2 · Distribuciones de Probabilidad

        Una **distribución** es el "molde" que asigna probabilidad a cada resultado posible.
        Elegir la distribución correcta *es* modelar el fenómeno. Aquí las cinco fundamentales:

        - **Bernoulli** — un ensayo, dos resultados (éxito/fracaso). El ladrillo de todo.
        - **Binomial** — número de éxitos en $n$ Bernoulli independientes.
        - **Poisson** — conteos de eventos raros en un intervalo (llegadas, fallos, mutaciones).
        - **Uniforme** — todos los valores igual de probables (máxima ignorancia / continua).
        - **Normal** — el atractor universal (por el TLC); errores, sumas, promedios.

        Explora cada una: la fórmula ($\LaTeX$) usa **tus parámetros**, y se muestran media/varianza.
        """
    )
    return


@app.cell
def _(mo):
    dist_pick = mo.ui.dropdown(
        options=["Bernoulli", "Binomial", "Poisson", "Uniforme", "Normal"],
        value="Binomial",
        label="Distribución",
    )
    dist_pick
    return (dist_pick,)


@app.cell
def _(mo):
    # Todos los sliders definidos una vez (estables). Se muestran de forma condicional aparte.
    d_bp = mo.ui.slider(0.0, 1.0, value=0.3, step=0.01, label="$p$ (prob. de éxito)", show_value=True)
    d_n = mo.ui.slider(1, 60, value=20, step=1, label="$n$ (ensayos)", show_value=True)
    d_p = mo.ui.slider(0.01, 0.99, value=0.35, step=0.01, label="$p$ (prob. de éxito)", show_value=True)
    d_lam = mo.ui.slider(0.1, 25.0, value=4.0, step=0.1, label="$\\lambda$ (tasa media)", show_value=True)
    d_a = mo.ui.slider(-5.0, 5.0, value=0.0, step=0.1, label="$a$ (mínimo)", show_value=True)
    d_b = mo.ui.slider(-5.0, 10.0, value=4.0, step=0.1, label="$b$ (máximo)", show_value=True)
    d_mu = mo.ui.slider(-5.0, 5.0, value=0.0, step=0.1, label="$\\mu$ (media)", show_value=True)
    d_sigma = mo.ui.slider(0.2, 4.0, value=1.0, step=0.1, label="$\\sigma$ (desv. estándar)", show_value=True)
    return d_a, d_b, d_bp, d_lam, d_mu, d_n, d_p, d_sigma


@app.cell
def _(d_a, d_b, d_bp, d_lam, d_mu, d_n, d_p, d_sigma, dist_pick, mo):
    _sel = dist_pick.value
    if _sel == "Bernoulli":
        _ctrl = [d_bp]
    elif _sel == "Binomial":
        _ctrl = [d_n, d_p]
    elif _sel == "Poisson":
        _ctrl = [d_lam]
    elif _sel == "Uniforme":
        _ctrl = [d_a, d_b]
    else:
        _ctrl = [d_mu, d_sigma]
    mo.vstack([mo.md(f"**Parámetros — {_sel}**"), *_ctrl])
    return


@app.cell
def _(C, d_a, d_b, d_bp, d_lam, d_mu, d_n, d_p, d_sigma, dist_pick, new_ax, np, stats):
    _sel = dist_pick.value
    _fig, (axP, _axC) = new_ax(_figsize=(9.4, 3.6))
    _fig.subplots_adjust(wspace=0.28)

    if _sel == "Bernoulli":
        _p = float(d_bp.value)
        _k = np.array([0, 1]); _pmf = np.array([1 - _p, _p])
        axP.bar(_k, _pmf, width=0.5, color=C["primary"], alpha=0.85)
        axP.set_xticks([0, 1]); axP.set_title("PMF Bernoulli")
        axC.step([0, 1, 2], [0, 1 - _p, 1.0], where="post", color=C["accent"], lw=2.5)
        _mean, _var = _p, _p * (1 - _p)
    elif _sel == "Binomial":
        _n = int(d_n.value); _p = float(d_p.value)
        _k = np.arange(0, _n + 1); _pmf = stats.binom.pmf(_k, _n, _p)
        axP.bar(_k, _pmf, color=C["primary"], alpha=0.85)
        axP.set_title("PMF Binomial")
        axC.step(_k, np.cumsum(_pmf), where="post", color=C["accent"], lw=2.5)
        _mean, _var = _n * _p, _n * _p * (1 - _p)
    elif _sel == "Poisson":
        _lam = float(d_lam.value)
        _hi = int(max(10, _lam + 4 * np.sqrt(_lam) + 1))
        _k = np.arange(0, _hi); _pmf = stats.poisson.pmf(_k, _lam)
        axP.bar(_k, _pmf, color=C["primary"], alpha=0.85)
        axP.set_title("PMF Poisson")
        axC.step(_k, np.cumsum(_pmf), where="post", color=C["accent"], lw=2.5)
        _mean, _var = _lam, _lam
    elif _sel == "Uniforme":
        _a = float(d_a.value); _b = float(d_b.value)
        if _b <= _a:
            _b = _a + 0.1
        _x = np.linspace(_a - 1, _b + 1, 500)
        axP.plot(_x, stats.uniform.pdf(_x, _a, _b - _a), color=C["primary"], lw=2.5)
        axP.fill_between(_x, stats.uniform.pdf(_x, _a, _b - _a), color=C["primary"], alpha=0.2)
        axP.set_title("PDF Uniforme")
        axC.plot(_x, stats.uniform.cdf(_x, _a, _b - _a), color=C["accent"], lw=2.5)
        _mean, _var = (_a + _b) / 2, (_b - _a) ** 2 / 12
    else:  # Normal
        _mu = float(d_mu.value); _sg = float(d_sigma.value)
        _x = np.linspace(_mu - 4 * _sg, _mu + 4 * _sg, 500)
        axP.plot(_x, stats.norm.pdf(_x, _mu, _sg), color=C["primary"], lw=2.5)
        axP.fill_between(_x, stats.norm.pdf(_x, _mu, _sg), color=C["primary"], alpha=0.2)
        axP.set_title("PDF Normal")
        axC.plot(_x, stats.norm.cdf(_x, _mu, _sg), color=C["accent"], lw=2.5)
        _mean, _var = _mu, _sg ** 2

    axP.set_xlabel("valor"); axP.set_ylabel("probabilidad / densidad")
    axC.set_title("CDF acumulada"); axC.set_xlabel("valor"); axC.set_ylabel(r"$P(X \leq x)$")
    dist_mean = float(_mean); dist_var = float(_var)
    _fig
    return dist_mean, dist_var


@app.cell
def _(d_a, d_b, d_bp, d_lam, d_mu, d_n, d_p, d_sigma, dist_mean, dist_pick, dist_var, mo, np):
    _sel = dist_pick.value
    if _sel == "Bernoulli":
        _p = float(d_bp.value)
        _f = rf"$$P(X=x)={_p:.2f}^{{x}}\,(1-{_p:.2f})^{{1-x}},\qquad x\in\{{0,1\}}$$"
        _desc = "Un solo ensayo con dos resultados."
    elif _sel == "Binomial":
        _n = int(d_n.value); _p = float(d_p.value)
        _f = rf"$$P(X=k)=\binom{{{_n}}}{{k}}\,{_p:.2f}^{{k}}\,(1-{_p:.2f})^{{{_n}-k}}$$"
        _desc = "Suma de $n$ Bernoulli independientes."
    elif _sel == "Poisson":
        _lam = float(d_lam.value)
        _f = rf"$$P(X=k)=\frac{{{_lam:.2f}^{{k}}\,e^{{-{_lam:.2f}}}}}{{k!}}$$"
        _desc = "Límite de la Binomial cuando $n\\to\\infty$, $p\\to 0$, $np=\\lambda$ fijo."
    elif _sel == "Uniforme":
        _a = float(d_a.value); _b = float(d_b.value)
        _bb = _b if _b > _a else _a + 0.1
        _f = rf"$$f(x)=\frac{{1}}{{{_bb:.2f}-{_a:.2f}}}={1.0/(_bb-_a):.3f},\qquad x\in[{_a:.2f},{_bb:.2f}]$$"
        _desc = "Densidad constante; máxima incertidumbre en un rango."
    else:
        _mu = float(d_mu.value); _sg = float(d_sigma.value)
        _f = rf"$$f(x)=\frac{{1}}{{{_sg:.2f}\sqrt{{2\pi}}}}\;\exp\!\left(-\frac{{(x-{_mu:.2f})^2}}{{2\cdot{_sg:.2f}^{{2}}}}\right)$$"
        _desc = "El atractor universal (TLC): sumas y promedios convergen aquí."

    mo.vstack([
        mo.md(_f),
        mo.md(
            f"""
            {_desc}

            | Media $\\;\\mathbb{{E}}[X]$ | Varianza $\\;\\mathrm{{Var}}(X)$ | Desv. estándar |
            |---|---|---|
            | ${dist_mean:.3f}$ | ${dist_var:.3f}$ | ${np.sqrt(dist_var):.3f}$ |
            """
        ),
    ])
    return


@app.cell
def _(mo):
    mo.accordion({
        "🔗 Cómo se conectan (contenido extra de retención)": mo.md(
            r"""
            Las cinco no están aisladas: forman una **familia** unida por límites.

            $$
            \underbrace{\text{Bernoulli}(p)}_{\text{1 ensayo}}
            \;\xrightarrow[\text{suma de } n]{}\;
            \underbrace{\text{Binomial}(n,p)}_{\text{\# éxitos}}
            \;\xrightarrow[\;n\to\infty,\ np=\lambda\;]{}\;
            \underbrace{\text{Poisson}(\lambda)}_{\text{eventos raros}}
            $$

            $$
            \text{Binomial}(n,p)\;\xrightarrow[\;n\ \text{grande}\;]{\text{de Moivre–Laplace}}\;
            \mathcal{N}\!\big(np,\ np(1-p)\big)
            \qquad\qquad
            \bar{X}\;\xrightarrow[\;n\to\infty\;]{\text{TLC}}\;\mathcal{N}\!\Big(\mu,\ \tfrac{\sigma^2}{n}\Big)
            $$

            **Experimento mental:** pon la Binomial con $n=60$, $p$ pequeño (≈0.05) y compárala con
            una Poisson de $\lambda = np = 3$. Casi idénticas. Ahora sube $p$ a 0.5: la Binomial se
            vuelve una campana (Normal). *Una misma familia, distintos regímenes.*
            """
        )
    })
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 3. SIGNIFICANCIA, VALOR p, TOLERANCIA DE RIESGO
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3 · Significancia, Valor $p$ y Tolerancia de Riesgo

        Toda prueba de hipótesis es un **juicio bajo incertidumbre**:

        - $H_0$ (nula): "no pasa nada" (el efecto es cero).
        - $H_1$ (alternativa): "sí hay efecto".

        Asumimos $H_0$ verdadera, calculamos un **estadístico** (aquí $Z$) y preguntamos:
        *¿qué tan sorprendentes son mis datos si $H_0$ fuera cierta?* Esa sorpresa es el **valor $p$**:

        $$p = P(\text{observar algo tan o más extremo} \mid H_0\ \text{cierta})$$

        Tú fijas de antemano tu **tolerancia de riesgo** $\alpha$ (típico 0.05): la probabilidad
        máxima de **falso positivo** (error Tipo I) que estás dispuesto a aceptar. Regla: rechazas
        $H_0$ si $p < \alpha$.

        | | $H_0$ es cierta | $H_0$ es falsa |
        |---|---|---|
        | **Rechazo $H_0$** | ❌ Error Tipo I ($\alpha$) | ✅ Acierto (**potencia** $=1-\beta$) |
        | **No rechazo $H_0$** | ✅ Acierto | ❌ Error Tipo II ($\beta$) |

        $\alpha$ es *tu decisión* (tolerancia de riesgo); $\beta$ y la potencia dependen del efecto
        real y de $n$. Bajar $\alpha$ te protege de falsos positivos **pero sacrifica potencia**.
        Ese *trade-off* es el corazón del asunto.
        """
    )
    return


@app.cell
def _(mo):
    sig_d = mo.ui.slider(0.0, 1.5, value=0.4, step=0.05, label="Tamaño de efecto real (Cohen's $d$)", show_value=True)
    sig_n = mo.ui.slider(3, 300, value=40, step=1, label="Tamaño de muestra $n$", show_value=True)
    sig_alpha = mo.ui.slider(0.001, 0.20, value=0.05, step=0.001, label=r"Tolerancia de riesgo $\alpha$", show_value=True)
    sig_zobs = mo.ui.slider(-5.0, 5.0, value=2.1, step=0.05, label="Estadístico observado $z_{obs}$", show_value=True)
    mo.vstack([mo.md("**Controles — prueba $Z$ de dos colas**"), sig_d, sig_n, sig_alpha, sig_zobs])
    return sig_alpha, sig_d, sig_n, sig_zobs


@app.cell
def _(C, new_ax, np, sig_alpha, sig_d, sig_n, stats):
    _d = float(sig_d.value); _n = int(sig_n.value); _alpha = float(sig_alpha.value)
    _delta = _d * np.sqrt(_n)                       # no-centralidad bajo H1
    _zc = stats.norm.ppf(1 - _alpha / 2)            # valor crítico (dos colas)
    _power = stats.norm.sf(_zc - _delta) + stats.norm.cdf(-_zc - _delta)
    _beta = 1 - _power

    _fig, _ax = new_ax(_figsize=(9.0, 4.2))
    _x = np.linspace(-4, _delta + 4, 800)
    _h0 = stats.norm.pdf(_x, 0, 1)
    _h1 = stats.norm.pdf(_x, _delta, 1)

    ax.plot(_x, _h0, color=C["slate"], lw=2, label=r"$H_0:\ Z\sim\mathcal{N}(0,1)$")
    ax.plot(_x, _h1, color=C["success"], lw=2, label=fr"$H_1:\ Z\sim\mathcal{{N}}({_delta:.2f},1)$")

    # Región de rechazo (alpha) bajo H0
    _rej = (_x <= -_zc) | (_x >= _zc)
    ax.fill_between(_x, _h0, where=_rej, color=C["danger"], alpha=0.35,
                    label=fr"$\alpha={_alpha:.3f}$ (Tipo I)")
    # beta: no rechazo bajo H1
    _acc = (_x > -_zc) & (_x < _zc)
    ax.fill_between(_x, _h1, where=_acc, color=C["accent"], alpha=0.30,
                    label=fr"$\beta={_beta:.3f}$ (Tipo II)")
    # potencia
    ax.fill_between(_x, _h1, where=_rej, color=C["success"], alpha=0.25,
                    label=fr"potencia $={_power:.3f}$")

    for _v in (-_zc, _zc):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.3)
    ax.set_title("Errores Tipo I / II y potencia")
    ax.set_xlabel("estadístico $Z$"); ax.set_ylabel("densidad")
    ax._legend(loc="upper right", fontsize=8.5)

    sig_zc = float(_zc); sig_power = float(_power); sig_beta = float(_beta); sig_delta = float(_delta)
    _fig
    return sig_beta, sig_delta, sig_power, sig_zc


@app.cell
def _(mo, sig_alpha, sig_beta, sig_d, sig_delta, sig_n, sig_power, sig_zc):
    mo.md(
        rf"""
        **Con tus valores** ($d={float(sig_d.value):.2f}$, $n={int(sig_n.value)}$, $\alpha={float(sig_alpha.value):.3f}$):

        $$z_{{\text{{crítico}}}}=\Phi^{{-1}}\!\left(1-\tfrac{{\alpha}}{{2}}\right)={sig_zc:.3f}
        \qquad \delta = d\sqrt{{n}} = {sig_delta:.3f}$$

        $$\text{{potencia}} = 1-\beta = {sig_power:.3f}\qquad \beta = {sig_beta:.3f}$$

        🧠 **Lee la gráfica:** sube $n$ o el efecto $d$ → la curva verde ($H_1$) se aleja → **más
        potencia**. Baja $\alpha$ → las líneas críticas se separan → menos falsos positivos pero
        **más $\beta$** (menos potencia). No puedes minimizar ambos a la vez con $n$ fijo.
        """
    )
    return


@app.cell
def _(C, new_ax, np, sig_alpha, sig_zobs, stats):
    _z = float(sig_zobs.value); _alpha = float(sig_alpha.value)
    _p = 2 * stats.norm.sf(abs(_z))                 # dos colas
    _zc = stats.norm.ppf(1 - _alpha / 2)

    _fig, _ax = new_ax(_figsize=(9.0, 3.4))
    _x = np.linspace(-5, 5, 800); _y = stats.norm.pdf(_x)
    ax.plot(_x, _y, color=C["slate"], lw=2)
    _tail = (_x <= -abs(_z)) | (_x >= abs(_z))
    ax.fill_between(_x, _y, where=_tail, color=C["primary"], alpha=0.45,
                    label=fr"valor $p={_p:.4f}$")
    ax.axvline(_z, color=C["danger"], lw=2, label=fr"$z_{{obs}}={_z:.2f}$")
    for _v in (-_zc, _zc):
        ax.axvline(_v, color=C["accent"], ls="--", lw=1.2)
    ax.set_title("Valor $p$ como área en las colas")
    ax.set_xlabel("$Z$ bajo $H_0$"); ax.set_ylabel("densidad")
    ax._legend(loc="upper right", fontsize=9)

    sig_pval = float(_p)
    _fig
    return (sig_pval,)


@app.cell
def _(mo, sig_alpha, sig_pval, sig_zobs):
    _p = sig_pval; _a = float(sig_alpha.value)
    _decision = (
        mo.callout(mo.md(rf"**$p={_p:.4f} < \alpha={_a:.3f}$ → se rechaza $H_0$** (resultado *significativo*)."), kind="success")
        if _p < _a else
        mo.callout(mo.md(rf"**$p={_p:.4f} \geq \alpha={_a:.3f}$ → no se rechaza $H_0$** (no significativo)."), kind="warn")
    )
    mo.vstack([
        mo.md(
            rf"""
            $$p = 2\,\big(1-\Phi(|z_{{obs}}|)\big) = 2\,\big(1-\Phi({abs(float(sig_zobs.value)):.2f})\big) = {_p:.4f}$$
            """
        ),
        _decision,
    ])
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ⚠️ **La trampa más común del valor $p$.** El valor $p$ **NO** es:

            - la probabilidad de que $H_0$ sea cierta,
            - la probabilidad de que tu resultado sea por azar,
            - ni una medida del *tamaño* del efecto.

            Es solo: *"si $H_0$ fuera cierta, ¿qué tan seguido vería datos tan extremos?"*.
            Un $p$ pequeño con $n$ gigantesco puede señalar un efecto **trivial**. Reporta siempre
            el **tamaño de efecto** y un **intervalo de confianza**, no solo el $p$.
            """
        ),
        kind="danger",
    )
    return


@app.cell
def _(mo):
    quiz_p = mo.ui.radio(
        options=[
            "Hay 3% de probabilidad de que H0 sea cierta",
            "Si H0 fuera cierta, vería datos así de extremos el 3% de las veces",
            "Hay 97% de probabilidad de que mi hipótesis sea correcta",
        ],
        label="❓ Obtienes $p=0.03$. ¿Qué significa exactamente?",
    )
    quiz_p
    return (quiz_p,)


@app.cell
def _(mo, quiz_p):
    _ok = "Si H0 fuera cierta, vería datos así de extremos el 3% de las veces"
    if quiz_p.value is None:
        _out = mo.md("*Elige una opción.*")
    elif quiz_p.value == _ok:
        _out = mo.callout(mo.md("✅ **Exacto.** El $p$ condiciona *sobre* $H_0$; no dice la probabilidad de que $H_0$ sea cierta."), kind="success")
    else:
        _out = mo.callout(mo.md(r"❌ Esa es justo la mala interpretación. El $p$ es $P(\text{datos}\mid H_0)$, **no** $P(H_0\mid \text{datos})$."), kind="danger")
    _out
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 4. PRUEBAS ESTADÍSTICAS
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4 · Pruebas Estadísticas — ¿cuál para qué?

        La distribución de tus datos (y la pregunta) determina la prueba. Mapa de referencia:

        | Situación / Distribución | Pregunta típica | Prueba | Estadístico |
        |---|---|---|---|
        | Proporción (Bernoulli/Binomial) | ¿$p = p_0$? | Prueba **binomial exacta** / $z$ de proporciones | $z=\dfrac{\hat p - p_0}{\sqrt{p_0(1-p_0)/n}}$ |
        | Media, $\sigma$ conocida (Normal) | ¿$\mu = \mu_0$? | Prueba **$z$** | $z=\dfrac{\bar x-\mu_0}{\sigma/\sqrt n}$ |
        | Media, $\sigma$ desconocida | ¿$\mu = \mu_0$? | Prueba **$t$** de Student | $t=\dfrac{\bar x-\mu_0}{s/\sqrt n}$ |
        | Dos medias | ¿$\mu_1=\mu_2$? | **$t$** de 2 muestras (Welch) | $t=\dfrac{\bar x_1-\bar x_2}{\sqrt{s_1^2/n_1+s_2^2/n_2}}$ |
        | $>2$ medias | ¿todas iguales? | **ANOVA** ($F$) | $F=\dfrac{\text{var. entre}}{\text{var. dentro}}$ |
        | Conteos por categoría (Uniforme/multinomial) | ¿ajusta al modelo? | **$\chi^2$** bondad de ajuste | $\chi^2=\sum\dfrac{(O_i-E_i)^2}{E_i}$ |
        | Dos categóricas | ¿independientes? | **$\chi^2$** de independencia | idem, tabla de contingencia |
        | Tasa (Poisson) | ¿$\lambda=\lambda_0$? | Prueba **exacta de Poisson** | basada en $\sum X_i$ |
        | Sin normalidad | ¿medianas iguales? | **No paramétricas** (Mann–Whitney, Wilcoxon, Kruskal–Wallis) | rangos |

        Abajo, tres simuladores en vivo: **(a)** proporción, **(b)** medias ($t$), **(c)** bondad de
        ajuste $\chi^2$ (para la Uniforme).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### 4a · Prueba de proporción (Bernoulli / Binomial)""")
    return


@app.cell
def _(mo):
    prop_p0 = mo.ui.slider(0.05, 0.95, value=0.5, step=0.01, label="$p_0$ (proporción bajo $H_0$)", show_value=True)
    prop_n = mo.ui.slider(10, 500, value=100, step=5, label="$n$ (ensayos)", show_value=True)
    prop_k = mo.ui.slider(0, 500, value=60, step=1, label="$k$ (éxitos observados)", show_value=True)
    prop_alpha = mo.ui.slider(0.001, 0.20, value=0.05, step=0.001, label=r"$\alpha$", show_value=True)
    mo.vstack([prop_p0, prop_n, prop_k, prop_alpha])
    return prop_alpha, prop_k, prop_n, prop_p0


@app.cell
def _(mo, prop_alpha, prop_k, prop_n, prop_p0, stats):
    _p0 = float(prop_p0.value); _n = int(prop_n.value)
    _k = min(int(prop_k.value), _n); _a = float(prop_alpha.value)
    _phat = _k / _n
    _res = stats.binomtest(_k, _n, _p0, alternative="two-sided")
    _pval = _res.pvalue
    _z = (_phat - _p0) / (( _p0 * (1 - _p0) / _n) ** 0.5)

    _dec = (
        mo.callout(mo.md(rf"**$p={_pval:.4f} < \alpha={_a:.3f}$** → se rechaza $H_0$: la proporción difiere de ${_p0:.2f}$."), kind="success")
        if _pval < _a else
        mo.callout(mo.md(rf"**$p={_pval:.4f} \geq \alpha={_a:.3f}$** → no hay evidencia para rechazar $H_0$."), kind="warn")
    )
    mo.vstack([
        mo.md(
            rf"""
            $$\hat p=\frac{{k}}{{n}}=\frac{{{_k}}}{{{_n}}}={_phat:.3f}
            \qquad z=\frac{{\hat p-p_0}}{{\sqrt{{p_0(1-p_0)/n}}}}={_z:.3f}$$

            Prueba binomial exacta (dos colas): $\;p={_pval:.4f}$.
            """
        ),
        _dec,
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""### 4b · Prueba $t$ de dos muestras (Normal / comparar medias)""")
    return


@app.cell
def _(mo):
    t_diff = mo.ui.slider(0.0, 3.0, value=0.6, step=0.05, label="Diferencia real de medias", show_value=True)
    t_sd = mo.ui.slider(0.5, 4.0, value=1.5, step=0.1, label="Desv. estándar (común)", show_value=True)
    t_n = mo.ui.slider(5, 200, value=30, step=1, label="$n$ por grupo", show_value=True)
    t_alpha = mo.ui.slider(0.001, 0.20, value=0.05, step=0.001, label=r"$\alpha$", show_value=True)
    t_seed = mo.ui.slider(0, 40, value=1, step=1, label="Semilla", show_value=True)
    mo.vstack([t_diff, t_sd, t_n, t_alpha, t_seed])
    return t_alpha, t_diff, t_n, t_sd, t_seed


@app.cell
def _(C, new_ax, np, stats, t_diff, t_n, t_sd, t_seed):
    _rng = np.random.default_rng(int(t_seed.value))
    _n = int(t_n.value); _sd = float(t_sd.value); _dif = float(t_diff.value)
    _g1 = _rng.normal(0.0, _sd, _n)
    _g2 = _rng.normal(_dif, _sd, _n)
    _t, _pval = stats.ttest_ind(_g1, _g2, equal_var=False)

    _fig, _ax = new_ax(_figsize=(8.6, 3.6))
    _bins = np.linspace(min(_g1.min(), _g2.min()), max(_g1.max(), _g2.max()), 24)
    ax.hist(_g1, bins=_bins, alpha=0.55, color=C["primary"], label="Grupo A")
    ax.hist(_g2, bins=_bins, alpha=0.55, color=C["accent"], label="Grupo B")
    ax.axvline(_g1.mean(), color=C["primary"], lw=2, ls="--")
    ax.axvline(_g2.mean(), color=C["accent"], lw=2, ls="--")
    ax.set_title("Dos muestras: ¿misma media poblacional?")
    ax.set_xlabel("valor"); ax.set_ylabel("frecuencia"); ax._legend()

    t_stat = float(_t); t_pval = float(_pval)
    t_m1 = float(_g1.mean()); t_m2 = float(_g2.mean())
    _fig
    return t_m1, t_m2, t_pval, t_stat


@app.cell
def _(mo, t_alpha, t_m1, t_m2, t_pval, t_stat):
    _a = float(t_alpha.value)
    _dec = (
        mo.callout(mo.md(rf"**$p={t_pval:.4f} < \alpha={_a:.3f}$** → diferencia **significativa** entre grupos."), kind="success")
        if t_pval < _a else
        mo.callout(mo.md(rf"**$p={t_pval:.4f} \geq \alpha={_a:.3f}$** → no hay evidencia de diferencia."), kind="warn")
    )
    mo.vstack([
        mo.md(
            rf"""
            $$t=\frac{{\bar x_A-\bar x_B}}{{\sqrt{{s_A^2/n_A+s_B^2/n_B}}}}
            =\frac{{{t_m1:.3f}-{t_m2:.3f}}}{{\cdots}}={t_stat:.3f}\qquad p={t_pval:.4f}$$
            """
        ),
        _dec,
        mo.md("🧠 Baja la diferencia real a 0 y sube $n$: verás que rechazas $\\approx\\alpha\\%$ de las veces por puro azar (falsos positivos). Sube la diferencia: $p$ cae."),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""### 4c · Bondad de ajuste $\chi^2$ (¿los datos son Uniformes?)""")
    return


@app.cell
def _(mo):
    gof_k = mo.ui.slider(3, 12, value=6, step=1, label="N.º de categorías $k$ (p. ej. caras de un dado)", show_value=True)
    gof_N = mo.ui.slider(30, 2000, value=300, step=10, label="Tamaño de muestra $N$", show_value=True)
    gof_bias = mo.ui.slider(0.0, 1.0, value=0.0, step=0.02, label="Sesgo (0 = dado justo, 1 = muy cargado)", show_value=True)
    gof_alpha = mo.ui.slider(0.001, 0.20, value=0.05, step=0.001, label=r"$\alpha$", show_value=True)
    gof_seed = mo.ui.slider(0, 40, value=2, step=1, label="Semilla", show_value=True)
    mo.vstack([gof_k, gof_N, gof_bias, gof_alpha, gof_seed])
    return gof_N, gof_alpha, gof_bias, gof_k, gof_seed


@app.cell
def _(C, gof_N, gof_bias, gof_k, gof_seed, new_ax, np, stats):
    _rng = np.random.default_rng(int(gof_seed.value))
    _k = int(gof_k.value); _N = int(gof_N.value); _bias = float(gof_bias.value)

    _probs = np.ones(_k) / _k
    _tilt = np.linspace(1.0, 1.0 + 2.0 * _bias, _k)  # inclina las probabilidades
    _probs = _tilt / _tilt.sum()
    _obs = _rng.multinomial(_N, _probs)
    _exp = np.full(_k, _N / _k)
    _chi2, _pval = stats.chisquare(_obs, _exp)

    _fig, _ax = new_ax(_figsize=(8.6, 3.6))
    _idx = np.arange(1, _k + 1)
    ax.bar(_idx - 0.19, _obs, width=0.38, color=C["primary"], alpha=0.85, label="Observado $O_i$")
    ax.bar(_idx + 0.19, _exp, width=0.38, color=C["muted"], alpha=0.85, label="Esperado $E_i$")
    ax.set_xticks(_idx)
    ax.set_title("Bondad de ajuste a la Uniforme")
    ax.set_xlabel("categoría"); ax.set_ylabel("conteo"); ax._legend()

    gof_chi2 = float(_chi2); gof_pval = float(_pval); gof_df = _k - 1
    _fig
    return gof_chi2, gof_df, gof_pval


@app.cell
def _(gof_alpha, gof_chi2, gof_df, gof_pval, mo):
    _a = float(gof_alpha.value)
    _dec = (
        mo.callout(mo.md(rf"**$p={gof_pval:.4f} < \alpha={_a:.3f}$** → se rechaza la uniformidad (el dado está **cargado**)."), kind="success")
        if gof_pval < _a else
        mo.callout(mo.md(rf"**$p={gof_pval:.4f} \geq \alpha={_a:.3f}$** → compatible con un dado **justo**."), kind="warn")
    )
    mo.vstack([
        mo.md(
            rf"""
            $$\chi^2=\sum_{{i=1}}^{{k}}\frac{{(O_i-E_i)^2}}{{E_i}}={gof_chi2:.3f}
            \qquad \text{{g.l.}}=k-1={gof_df}\qquad p={gof_pval:.4f}$$
            """
        ),
        _dec,
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 5. REGRESIÓN
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5 · Regresión Lineal y Logística

        La regresión **modela una relación**. La diferencia clave es *qué* predice:

        - **Lineal** — predice un número continuo: $\hat y = \beta_0 + \beta_1 x$.
        - **Logística** — predice una *probabilidad* (salida binaria 0/1) vía la sigmoide.

        ### 5a · Regresión lineal (mínimos cuadrados, OLS)
        """
    )
    return


@app.cell
def _(mo):
    lin_b0 = mo.ui.slider(-5.0, 5.0, value=1.0, step=0.1, label=r"Intercepto real $\beta_0$", show_value=True)
    lin_b1 = mo.ui.slider(-3.0, 3.0, value=1.2, step=0.1, label=r"Pendiente real $\beta_1$", show_value=True)
    lin_noise = mo.ui.slider(0.1, 6.0, value=2.0, step=0.1, label="Ruido $\\sigma$", show_value=True)
    lin_n = mo.ui.slider(10, 400, value=80, step=5, label="$n$ (observaciones)", show_value=True)
    lin_seed = mo.ui.slider(0, 40, value=3, step=1, label="Semilla", show_value=True)
    mo.vstack([lin_b0, lin_b1, lin_noise, lin_n, lin_seed])
    return lin_b0, lin_b1, lin_n, lin_noise, lin_seed


@app.cell
def _(C, lin_b0, lin_b1, lin_n, lin_noise, lin_seed, new_ax, np):
    _rng = np.random.default_rng(int(lin_seed.value))
    _n = int(lin_n.value); _b0 = float(lin_b0.value); _b1 = float(lin_b1.value); _s = float(lin_noise.value)
    _x = _rng.uniform(0, 10, _n)
    _y = _b0 + _b1 * _x + _rng.normal(0, _s, _n)

    # OLS cerrado
    _b1h, _b0h = np.polyfit(_x, _y, 1)
    _yhat = _b0h + _b1h * _x
    _ss_res = np.sum((_y - _yhat) ** 2)
    _ss_tot = np.sum((_y - _y.mean()) ** 2)
    _r2 = 1 - _ss_res / _ss_tot if _ss_tot > 0 else 0.0

    _fig, (_ax1, _ax2) = new_ax(_figsize=(9.4, 3.6))
    _fig.subplots_adjust(wspace=0.28)
    _ax1.scatter(_x, _y, s=18, color=C["primary"], alpha=0.6, label="datos")
    _xs = np.array([_x.min(), _x.max()])
    _ax1.plot(_xs, _b0h + _b1h * _xs, color=C["danger"], lw=2.5, label="ajuste OLS")
    _ax1.plot(_xs, _b0 + _b1 * _xs, color=C["success"], lw=1.8, ls="--", label="recta real")
    _ax1.set_title("Ajuste lineal"); _ax1.set_xlabel("x"); _ax1.set_ylabel("y"); _ax1._legend(fontsize=8.5)

    _resid = _y - _yhat
    _ax2.scatter(_yhat, _resid, s=16, color=C["purple"], alpha=0.6)
    _ax2.axhline(0, color=C["slate"], lw=1.5)
    _ax2.set_title("Residuales (deberían verse sin patrón)")
    _ax2.set_xlabel(r"$\hat y$"); _ax2.set_ylabel("residual")

    lin_b0h = float(_b0h); lin_b1h = float(_b1h); lin_r2 = float(_r2)
    _fig
    return lin_b0h, lin_b1h, lin_r2


@app.cell
def _(lin_b0h, lin_b1h, lin_r2, mo):
    mo.md(
        rf"""
        $$\hat y = \hat\beta_0 + \hat\beta_1 x = {lin_b0h:.3f} + {lin_b1h:.3f}\,x
        \qquad R^2 = {lin_r2:.3f}$$

        $R^2$ es la fracción de varianza de $y$ explicada por el modelo. 🧠 Sube el ruido $\sigma$:
        $R^2$ cae aunque la pendiente estimada siga siendo insesgada. Baja $n$: la estimación se
        vuelve inestable (re-muestrea con la semilla y verás cuánto brinca $\hat\beta_1$).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### 5b · Regresión logística""")
    return


@app.cell
def _(np):
    def fit_logistic(X, y, iters=50):
        """Newton–Raphson (IRLS) para regresión logística. X incluye columna de 1s."""
        beta = np.zeros(X.shape[1])
        for _ in range(iters):
            eta = np.clip(X @ beta, -30, 30)
            p = 1.0 / (1.0 + np.exp(-eta))
            W = np.clip(p * (1 - p), 1e-9, None)
            grad = X.T @ (y - p)
            H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1])
            step = np.linalg.solve(H, grad)
            beta = beta + step
            if np.max(np.abs(step)) < 1e-8:
                break
        return beta
    return (fit_logistic,)


@app.cell
def _(mo):
    log_b0 = mo.ui.slider(-6.0, 6.0, value=-3.0, step=0.2, label=r"Intercepto real $\beta_0$", show_value=True)
    log_b1 = mo.ui.slider(-2.0, 2.0, value=0.8, step=0.05, label=r"Pendiente real $\beta_1$ (log-odds)", show_value=True)
    log_n = mo.ui.slider(30, 600, value=200, step=10, label="$n$", show_value=True)
    log_thr = mo.ui.slider(0.05, 0.95, value=0.5, step=0.05, label="Umbral de clasificación", show_value=True)
    log_seed = mo.ui.slider(0, 40, value=4, step=1, label="Semilla", show_value=True)
    mo.vstack([log_b0, log_b1, log_n, log_thr, log_seed])
    return log_b0, log_b1, log_n, log_seed, log_thr


@app.cell
def _(C, fit_logistic, log_b0, log_b1, log_n, log_seed, log_thr, new_ax, np):
    _rng = np.random.default_rng(int(log_seed.value))
    _n = int(log_n.value); _b0 = float(log_b0.value); _b1 = float(log_b1.value); _thr = float(log_thr.value)
    _x = _rng.uniform(0, 10, _n)
    _p_true = 1.0 / (1.0 + np.exp(-(_b0 + _b1 * _x)))
    _y = _rng.binomial(1, _p_true).astype(float)

    _X = np.column_stack([np.ones(_n), _x])
    _beta = fit_logistic(_X, _y)
    _b0h, _b1h = float(_beta[0]), float(_beta[1])

    _grid = np.linspace(0, 10, 300)
    _phat = 1.0 / (1.0 + np.exp(-(_b0h + _b1h * _grid)))

    # Matriz de confusión al umbral
    _pred = (1.0 / (1.0 + np.exp(-(_b0h + _b1h * _x)))) >= _thr
    _yb = _y.astype(bool)
    _TP = int(np.sum(_pred & _yb)); _TN = int(np.sum(~_pred & ~_yb))
    _FP = int(np.sum(_pred & ~_yb)); _FN = int(np.sum(~_pred & _yb))
    _acc = (_TP + _TN) / _n

    _fig, _ax = new_ax(_figsize=(8.6, 3.8))
    _jit = _rng.normal(0, 0.02, _n)
    ax.scatter(_x, _y + _jit, s=16, color=C["primary"], alpha=0.4, label="datos (0/1)")
    ax.plot(_grid, _phat, color=C["danger"], lw=2.5, label="prob. estimada (sigmoide)")
    ax.axhline(_thr, color=C["accent"], ls="--", lw=1.5, label=f"umbral={_thr:.2f}")
    ax.set_title("Regresión logística"); ax.set_xlabel("x"); ax.set_ylabel("y / P(y=1)")
    ax.set_ylim(-0.1, 1.1); ax._legend(fontsize=8.5, loc="center right")

    log_b0h = _b0h; log_b1h = _b1h; log_acc = float(_acc)
    log_TP, log_TN, log_FP, log_FN = _TP, _TN, _FP, _FN
    _fig
    return log_FN, log_FP, log_TN, log_TP, log_acc, log_b0h, log_b1h


@app.cell
def _(log_FN, log_FP, log_TN, log_TP, log_acc, log_b0h, log_b1h, mo):
    mo.md(
        rf"""
        $$\log\!\frac{{p}}{{1-p}} = \beta_0+\beta_1 x = {log_b0h:.3f} + {log_b1h:.3f}\,x
        \qquad\Longrightarrow\qquad p=\frac{{1}}{{1+e^{{-({log_b0h:.3f}+{log_b1h:.3f}\,x)}}}}$$

        **Matriz de confusión** al umbral elegido &nbsp;($\text{{exactitud}}={log_acc:.3f}$):

        | | Predijo 1 | Predijo 0 |
        |---|---|---|
        | **Real 1** | TP = {log_TP} | FN = {log_FN} |
        | **Real 0** | FP = {log_FP} | TN = {log_TN} |

        🧠 Mueve el **umbral**: bajarlo captura más positivos (↑TP) pero dispara falsos positivos
        (↑FP). Ese es el mismo *trade-off* $\alpha/\beta$ de la sección 3, ahora en clasificación.
        El coeficiente $\beta_1={log_b1h:.3f}$ es el cambio en **log-odds** por unidad de $x$;
        $e^{{\beta_1}}={__import__('math').exp(log_b1h):.3f}$ es el **odds ratio**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 6. CORRELACIÓN Y CAUSALIDAD
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6 · Correlación y Causalidad

        La **correlación de Pearson** $r\in[-1,1]$ mide *asociación lineal*:

        $$r=\frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2}\,\sqrt{\sum (y_i-\bar y)^2}}$$

        Dos advertencias que valen oro:

        1. $r$ solo ve lo **lineal**. Una relación fuerte pero curva puede dar $r\approx 0$.
        2. **Correlación $\neq$ causalidad.** Una tercera variable (*confusor*) puede crear
           correlación entre cosas que no se causan.
        """
    )
    return


@app.cell
def _(mo):
    cor_r = mo.ui.slider(-0.98, 0.98, value=0.6, step=0.02, label="Correlación objetivo $r$", show_value=True)
    cor_n = mo.ui.slider(20, 500, value=150, step=10, label="$n$", show_value=True)
    cor_seed = mo.ui.slider(0, 40, value=5, step=1, label="Semilla", show_value=True)
    mo.vstack([cor_r, cor_n, cor_seed])
    return cor_n, cor_r, cor_seed


@app.cell
def _(C, cor_n, cor_r, cor_seed, new_ax, np):
    _rng = np.random.default_rng(int(cor_seed.value))
    _n = int(cor_n.value); _r = float(cor_r.value)
    _z1 = _rng.normal(0, 1, _n); _z2 = _rng.normal(0, 1, _n)
    _x = _z1
    _y = _r * _z1 + np.sqrt(max(1 - _r ** 2, 0)) * _z2
    _remp = float(np.corrcoef(_x, _y)[0, 1])

    _fig, _ax = new_ax(_figsize=(6.4, 4.2))
    ax.scatter(_x, _y, s=18, color=C["primary"], alpha=0.55)
    ax.set_title(fr"$r_{{objetivo}}={_r:.2f}$   ·   $r_{{empírico}}={_remp:.2f}$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    cor_remp = _remp
    _fig
    return (cor_remp,)


@app.cell
def _(cor_remp, mo):
    mo.md(
        rf"""
        $r$ empírico en la muestra: $\;{cor_remp:.3f}$. 🧠 Con $n$ pequeño, el $r$ observado brinca
        mucho respecto al objetivo (variabilidad de muestreo, sección 1). Con $r=0$ verás una nube
        sin estructura.
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion({
        "⚠️ Anscombe: cuatro conjuntos, el mismo $r$ (contenido extra)": mo.md(
            r"""
            El **cuarteto de Anscombe** (1973) son cuatro conjuntos con media, varianza, recta de
            regresión y $r\approx 0.816$ **idénticos**, pero formas radicalmente distintas: uno lineal,
            uno curvo, uno con un *outlier* que inventa la pendiente, uno donde un solo punto domina.
            Moraleja: **siempre grafica antes de confiar en un número resumen.** (Corre la celda de
            abajo para verlos.)
            """
        )
    })
    return


@app.cell
def _(C, new_ax, np):
    # Cuarteto de Anscombe (valores clásicos)
    _x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], float)
    _x4 = np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], float)
    _y1 = np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])
    _y2 = np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])
    _y3 = np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73])
    _y4 = np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])
    _sets = [(_x, _y1, "I"), (_x, _y2, "II"), (_x, _y3, "III"), (_x4, _y4, "IV")]

    _fig, _axes = new_ax(_figsize=(9.4, 6.0))
    import matplotlib.pyplot as _plt
    _fig, _axes = _plt.subplots(2, 2, _figsize=(9.4, 6.0))
    for _ax, (_xx, _yy, _name) in zip(_axes.ravel(), _sets):
        _b1, _b0 = np.polyfit(_xx, _yy, 1)
        _rr = np.corrcoef(_xx, _yy)[0, 1]
        _ax.scatter(_xx, _yy, s=30, color=C["primary"], alpha=0.75)
        _xs = np.array([_xx.min(), _xx.max()])
        _ax.plot(_xs, _b0 + _b1 * _xs, color=C["danger"], lw=1.8)
        _ax.set_title(f"Conjunto {_name}  ·  r={_rr:.2f}", fontsize=10)
        _ax.grid(alpha=0.25)
    _fig.suptitle("Cuarteto de Anscombe — mismo r, historias distintas", fontweight="bold")
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""### 6b · El confusor: cómo nace una correlación *espuria*""")
    return


@app.cell
def _(mo):
    conf_zx = mo.ui.slider(0.0, 2.0, value=1.2, step=0.1, label=r"Efecto del confusor $Z \to X$", show_value=True)
    conf_zy = mo.ui.slider(0.0, 2.0, value=1.2, step=0.1, label=r"Efecto del confusor $Z \to Y$", show_value=True)
    conf_xy = mo.ui.slider(-1.0, 1.0, value=0.0, step=0.05, label=r"Efecto DIRECTO $X \to Y$", show_value=True)
    conf_n = mo.ui.slider(50, 800, value=300, step=10, label="$n$", show_value=True)
    conf_seed = mo.ui.slider(0, 40, value=6, step=1, label="Semilla", show_value=True)
    mo.vstack([
        mo.md("Modelo: $Z$ causa a $X$ **y** a $Y$. Pon el efecto directo $X\\to Y$ en **0** y observa la correlación *fantasma*."),
        conf_zx, conf_zy, conf_xy, conf_n, conf_seed,
    ])
    return conf_n, conf_seed, conf_xy, conf_zx, conf_zy


@app.cell
def _(C, conf_n, conf_seed, conf_xy, conf_zx, conf_zy, new_ax, np):
    _rng = np.random.default_rng(int(conf_seed.value))
    _n = int(conf_n.value)
    _a = float(conf_zx.value); _b = float(conf_zy.value); _c = float(conf_xy.value)
    _Z = _rng.normal(0, 1, _n)
    _X = _a * _Z + _rng.normal(0, 1, _n)
    _Y = _b * _Z + _c * _X + _rng.normal(0, 1, _n)

    _r_naive = float(np.corrcoef(_X, _Y)[0, 1])
    _rxy = _r_naive
    _rxz = float(np.corrcoef(_X, _Z)[0, 1])
    _ryz = float(np.corrcoef(_Y, _Z)[0, 1])
    _denom = np.sqrt(max((1 - _rxz ** 2) * (1 - _ryz ** 2), 1e-12))
    _r_partial = float((_rxy - _rxz * _ryz) / _denom)

    _fig, (_ax1, _ax2) = new_ax(_figsize=(9.4, 3.8))
    _fig.subplots_adjust(wspace=0.28)
    _ax1.scatter(_X, _Y, s=16, color=C["danger"], alpha=0.5)
    _ax1.set_title(fr"Correlación ingenua  $X\!-\!Y$:  $r={_r_naive:.2f}$")
    _ax1.set_xlabel("X"); _ax1.set_ylabel("Y")

    # Controlando Z: residuales de X~Z y Y~Z
    _bx = np.polyfit(_Z, _X, 1); _by = np.polyfit(_Z, _Y, 1)
    _rx = _X - (_bx[0] * _Z + _bx[1]); _ry = _Y - (_by[0] * _Z + _by[1])
    _ax2.scatter(_rx, _ry, s=16, color=C["success"], alpha=0.5)
    _ax2.set_title(fr"Controlando $Z$ (parcial):  $r={_r_partial:.2f}$")
    _ax2.set_xlabel("X | Z (residual)"); _ax2.set_ylabel("Y | Z (residual)")

    conf_naive = _r_naive; conf_partial = _r_partial; conf_c = _c
    _fig
    return conf_c, conf_naive, conf_partial


@app.cell
def _(conf_c, conf_naive, conf_partial, mo):
    _spurious = abs(conf_c) < 0.05 and abs(conf_naive) > 0.2
    _msg = (
        mo.callout(mo.md(
            rf"""**Correlación espuria detectada.** Aunque $X$ **no** causa a $Y$ (efecto directo ≈ 0),
            la correlación ingenua es $r={conf_naive:.2f}$. Al **controlar el confusor $Z$**, la
            correlación parcial colapsa a $r={conf_partial:.2f}$. La asociación era un artefacto de $Z$."""
        ), kind="danger")
        if _spurious else
        mo.callout(mo.md(
            rf"""Correlación ingenua $r={conf_naive:.2f}$ → parcial (controlando $Z$) $r={conf_partial:.2f}$.
            La diferencia entre ambas **es** el efecto del confusor."""
        ), kind="info")
    )
    mo.vstack([
        mo.md(
            rf"""
            $$r_{{XY\cdot Z}}=\frac{{r_{{XY}}-r_{{XZ}}\,r_{{YZ}}}}{{\sqrt{{(1-r_{{XZ}}^2)(1-r_{{YZ}}^2)}}}}
            \;=\;{conf_partial:.3f}$$
            """
        ),
        _msg,
        mo.md(
            r"""
            🧠 **La lección de causalidad.** "Controlar por $Z$" es lo que hacen los experimentos
            (aleatorización) y los métodos causales (DAGs, *back-door adjustment*). Sin identificar
            los confusores, cualquier correlación puede ser un espejismo. *Ejemplo clásico:* ventas
            de helado y ahogamientos correlacionan — el confusor es el **calor del verano**.
            """
        ),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# 7. LABORATORIO DE PRUEBAS DE HIPÓTESIS — SLIDERS INTERACTIVOS
# ============================================================================
@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7 · Laboratorio de Pruebas de Hipótesis — Configura tu Escenario

        Elige el tipo de prueba, define $H_0$ y los parámetros con **sliders**, y observa:
        - la **distribución bajo $H_0$** con región de rechazo,
        - la **fórmula con tus valores actuales** (estilo Excel),
        - el **valor $p$**, **estadístico** y **decisión final**.

        > 💡 Cambia cualquier slider y todo se recalcula al instante (reactividad marimo).
        """
    )
    return


@app.cell
def _(mo):
    hypo_test_type = mo.ui.dropdown(
        options=[
            "Prueba Z: media (σ conocida)",
            "Prueba t: media (σ desconocida)",
            "Prueba Z: proporción",
            "Prueba t: dos muestras (Welch)",
            "Prueba χ²: bondad de ajuste",
            "Prueba χ²: independencia (2×2)",
            "Prueba F: varianzas (dos muestras)",
        ],
        value="Prueba Z: media (σ conocida)",
        label="Tipo de prueba",
    )
    hypo_tail = mo.ui.dropdown(
        options=["Dos colas", "Cola derecha (>)", "Cola izquierda (<)"],
        value="Dos colas",
        label="Tipo de alternativa",
    )
    hypo_alpha = mo.ui.slider(0.001, 0.20, value=0.05, step=0.001, label=r"Nivel de significancia $\alpha$", show_value=True)
    mo.vstack([mo.md("**Configuración general**"), hypo_test_type, hypo_tail, hypo_alpha])
    return hypo_alpha, hypo_tail, hypo_test_type


@app.cell
def _(hypo_test_type, mo):
    _sel = hypo_test_type.value
    if _sel == "Prueba Z: media (σ conocida)":
        _controls = mo.vstack([
            mo.md("**Parámetros — Prueba Z para la media (σ conocida)**"),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$ (media poblacional bajo nula)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.5, step=0.1, label=r"$\sigma$ (desv. estándar poblacional conocida)", show_value=True),
            mo.ui.slider(1, 500, value=30, step=1, label="$n$ (tamaño de muestra)", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.5, step=0.1, label=r"$\bar{x}$ (media muestral observada)", show_value=True),
        ])
    elif _sel == "Prueba t: media (σ desconocida)":
        _controls = mo.vstack([
            mo.md("**Parámetros — Prueba t de Student para la media**"),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$", show_value=True),
            mo.ui.slider(1, 200, value=25, step=1, label="$n$", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.6, step=0.1, label=r"$\bar{x}$ (media muestral)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.2, step=0.1, label="$s$ (desv. estándar muestral)", show_value=True),
        ])
    elif _sel == "Prueba Z: proporción":
        _controls = mo.vstack([
            mo.md("**Parámetros — Prueba Z para proporción**"),
            mo.ui.slider(0.01, 0.99, value=0.5, step=0.01, label=r"$H_0:\ p_0$ (proporción bajo nula)", show_value=True),
            mo.ui.slider(10, 1000, value=100, step=5, label="$n$ (ensayos)", show_value=True),
            mo.ui.slider(0, 1000, value=60, step=1, label="$k$ (éxitos observados)", show_value=True),
        ])
    elif _sel == "Prueba t: dos muestras (Welch)":
        _controls = mo.vstack([
            mo.md("**Parámetros — Prueba t de dos muestras (Welch, varianzas desiguales)**"),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_1-\mu_2 = \Delta_0$", show_value=True),
            mo.ui.slider(2, 200, value=30, step=1, label="$n_1$", show_value=True),
            mo.ui.slider(2, 200, value=30, step=1, label="$n_2$", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.8, step=0.1, label=r"$\bar{x}_1$", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$\bar{x}_2$", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.5, step=0.1, label="$s_1$", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.2, step=0.1, label="$s_2$", show_value=True),
        ])
    elif _sel == "Prueba χ²: bondad de ajuste":
        _controls = mo.vstack([
            mo.md("**Parámetros — Bondad de ajuste χ² (multinomial vs teórica)**"),
            mo.ui.slider(2, 12, value=6, step=1, label="$k$ (número de categorías)", show_value=True),
            mo.ui.slider(10, 2000, value=300, step=10, label="$N$ (tamaño total)", show_value=True),
            mo.ui.slider(0.0, 1.0, value=0.2, step=0.02, label="Sesgo en probabilidades teóricas (0=uniforme)", show_value=True),
            mo.ui.slider(0, 40, value=1, step=1, label="Semilla (re-muestrear observados)", show_value=True),
        ])
    elif _sel == "Prueba χ²: independencia (2×2)":
        _controls = mo.vstack([
            mo.md("**Parámetros — Independencia χ² (tabla 2×2)**"),
            mo.ui.slider(0, 200, value=50, step=1, label="$a$ (fila 1, col 1)", show_value=True),
            mo.ui.slider(0, 200, value=30, step=1, label="$b$ (fila 1, col 2)", show_value=True),
            mo.ui.slider(0, 200, value=20, step=1, label="$c$ (fila 2, col 1)", show_value=True),
            mo.ui.slider(0, 200, value=40, step=1, label="$d$ (fila 2, col 2)", show_value=True),
        ])
    else:  # Prueba F: varianzas
        _controls = mo.vstack([
            mo.md("**Parámetros — Prueba F para igualdad de varianzas**"),
            mo.ui.slider(2, 200, value=25, step=1, label="$n_1$", show_value=True),
            mo.ui.slider(2, 200, value=30, step=1, label="$n_2$", show_value=True),
            mo.ui.slider(0.1, 10.0, value=2.0, step=0.1, label="$s_1^2$ (varianza muestra 1)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.0, step=0.1, label="$s_2^2$ (varianza muestra 2)", show_value=True),
        ])
    _controls


# ============================================================================
# MOSTRAR SOLO LA PRUEBA SELECCIONADA (renderizado condicional via markdown)
# ============================================================================
@app.cell
def _(hypo_test_type, mo):
    _mu0 = float(hypo_z_mu0.value)
    _sigma = float(hypo_z_sigma.value)
    _n = int(hypo_z_n.value)
    _xbar = float(hypo_z_xbar.value)
    _alpha = float(hypo_alpha.value)
    _tail = hypo_tail.value

    _se = _sigma / np.sqrt(_n)
    _z = (_xbar - _mu0) / _se

    if _tail == "Dos colas":
        _p = 2 * stats.norm.sf(abs(_z))
        _zc = stats.norm.ppf(1 - _alpha / 2)
        _crit = f"±{_zc:.3f}"
        _rej = (_z <= -_zc) or (_z >= _zc)
    elif _tail == "Cola derecha (>)":
        _p = stats.norm.sf(_z)
        _zc = stats.norm.ppf(1 - _alpha)
        _crit = f">{_zc:.3f}"
        _rej = _z >= _zc
    else:  # Cola izquierda
        _p = stats.norm.cdf(_z)
        _zc = stats.norm.ppf(_alpha)
        _crit = f"<{_zc:.3f}"
        _rej = _z <= _zc

    # Gráfica
    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _x = np.linspace(-4, 4, 800)
    _y = stats.norm.pdf(_x)
    ax.plot(_x, _y, color=C["slate"], lw=2, label=r"$H_0:\ Z\sim\mathcal{N}(0,1)$")

    if _tail == "Dos colas":
        _rej_mask = (_x <= -_zc) | (_x >= _zc)
    elif _tail == "Cola derecha (>)":
        _rej_mask = _x >= _zc
    else:
        _rej_mask = _x <= _zc
    ax.fill_between(_x, _y, where=_rej_mask, color=C["danger"], alpha=0.35, label=fr"Región de rechazo ($\alpha={_alpha:.3f}$)")
    ax.axvline(_z, color=C["primary"], lw=2.5, label=fr"$z_{{obs}}={_z:.3f}$")
    for _v in ([-_zc, _zc] if _tail == "Dos colas" else [_zc]):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.5)
    ax.set_title("Distribución bajo $H_0$ (Normal estándar) — Prueba Z para la media")
    ax.set_xlabel("$Z$"); ax.set_ylabel("densidad"); ax._legend(loc="upper right", fontsize=8.5)

    hypo_z_stat = _z; hypo_z_pval = _p; hypo_z_crit = _zc; hypo_z_reject = _rej; hypo_z_se = _se
    _fig
    return hypo_z_crit, hypo_z_pval, hypo_z_reject, hypo_z_se, hypo_z_stat


@app.cell
def _(hypo_alpha, hypo_tail, hypo_z_mu0, hypo_z_n, hypo_z_sigma, hypo_z_xbar, hypo_z_crit, hypo_z_pval, hypo_z_reject, hypo_z_se, hypo_z_stat, mo):
    _mu0 = float(hypo_z_mu0.value); _sigma = float(hypo_z_sigma.value)
    _n = int(hypo_z_n.value); _xbar = float(hypo_z_xbar.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value

    # Fórmula estilo Excel
    # Pre-compute strings with backslashes to avoid f-string backslash issues
    if _tail == "Cola derecha (>)":
        _rej_str = "z \\geq " + f"{hypo_z_crit:.3f}"
        _decision = "🟢 **Se RECHAZA $H_0$** (evidencia significativa)" if hypo_z_reject else "🔴 **NO se rechaza $H_0$** (evidencia insuficiente)"
    elif _tail == "Cola izquierda (<)":
        _rej_str = "z \\leq " + f"{hypo_z_crit:.3f}"
        _decision = "🟢 **Se RECHAZA $H_0$** (evidencia significativa)" if hypo_z_reject else "🔴 **NO se rechaza $H_0$** (evidencia insuficiente)"
    else:
        _rej_str = "z \\notin [ -" + f"{hypo_z_crit:.3f}" + ", " + f"{hypo_z_crit:.3f}" + " ]"
        _decision = "🟢 **Se RECHAZA $H_0$** (evidencia significativa)" if hypo_z_reject else "🔴 **NO se rechaza $H_0$** (evidencia insuficiente)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel):**

    $$z = \frac{{\bar{{x}} - \mu_0}}{{\sigma / \sqrt{{n}}}}
       = \frac{{{_xbar:.3f} - {_mu0:.3f}}}{{{_sigma:.3f} / \sqrt{{{_n}}}}}
       = \frac{{{_xbar - _mu0:.3f}}}{{{_sigma / np.sqrt(_n):.4f}}}
       = {hypo_z_stat:.4f}$$

    **Error estándar:** $\;SE = \sigma/\sqrt{{n}} = {_sigma:.3f}/\sqrt{{{_n}}} = {hypo_z_se:.4f}$

    **Región de rechazo ({_tail}):** ${_rej_str}$

    **Valor $p$:** ${hypo_z_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7b: t-test media (σ desconocida) ——————
@app.cell
def _(mo):
    hypo_t_mu0 = mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$", show_value=True)
    hypo_t_n = mo.ui.slider(2, 200, value=25, step=1, label="$n$", show_value=True)
    hypo_t_xbar = mo.ui.slider(-10.0, 10.0, value=0.6, step=0.1, label=r"$\bar{x}$", show_value=True)
    hypo_t_s = mo.ui.slider(0.1, 10.0, value=1.2, step=0.1, label="$s$ (muestral)", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Prueba t de Student para la media**"),
        hypo_t_mu0, hypo_t_n, hypo_t_xbar, hypo_t_s,
    ])
    return hypo_t_mu0, hypo_t_n, hypo_t_s, hypo_t_xbar


@app.cell
def _(C, hypo_alpha, hypo_tail, hypo_t_mu0, hypo_t_n, hypo_t_s, hypo_t_xbar, new_ax, np, stats):
    _mu0 = float(hypo_t_mu0.value); _n = int(hypo_t_n.value)
    _xbar = float(hypo_t_xbar.value); _s = float(hypo_t_s.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value
    _df = _n - 1
    _se = _s / np.sqrt(_n)
    _t = (_xbar - _mu0) / _se

    if _tail == "Dos colas":
        _p = 2 * stats.t.sf(abs(_t), _df)
        _tc = stats.t.ppf(1 - _alpha / 2, _df)
        _rej = (_t <= -_tc) or (_t >= _tc)
    elif _tail == "Cola derecha (>)":
        _p = stats.t.sf(_t, _df)
        _tc = stats.t.ppf(1 - _alpha, _df)
        _rej = _t >= _tc
    else:
        _p = stats.t.cdf(_t, _df)
        _tc = stats.t.ppf(_alpha, _df)
        _rej = _t <= _tc

    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _x = np.linspace(-4, 4, 800)
    _y = stats.t.pdf(_x, _df)
    ax.plot(_x, _y, color=C["slate"], lw=2, label=fr"$H_0:\ t\sim t_{{{_df}}}$")
    if _tail == "Dos colas":
        _rej_mask = (_x <= -_tc) | (_x >= _tc)
    elif _tail == "Cola derecha (>)":
        _rej_mask = _x >= _tc
    else:
        _rej_mask = _x <= _tc
    ax.fill_between(_x, _y, where=_rej_mask, color=C["danger"], alpha=0.35, label=fr"Región de rechazo ($\alpha={_alpha:.3f}$)")
    ax.axvline(_t, color=C["primary"], lw=2.5, label=fr"$t_{{obs}}={_t:.3f}$")
    for _v in ([-_tc, _tc] if _tail == "Dos colas" else [_tc]):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.5)
    ax.set_title(f"Distribución $t$ bajo $H_0$ (g.l.={_df}) — Prueba t para la media")
    ax.set_xlabel("$t$"); ax.set_ylabel("densidad"); ax._legend(loc="upper right", fontsize=8.5)

    hypo_t_stat = _t; hypo_t_pval = _p; hypo_t_crit = _tc; hypo_t_reject = _rej; hypo_t_se = _se; hypo_t_df = _df
    _fig
    return hypo_t_crit, hypo_t_df, hypo_t_pval, hypo_t_reject, hypo_t_se, hypo_t_stat


@app.cell
def _(hypo_alpha, hypo_tail, hypo_t_mu0, hypo_t_n, hypo_t_s, hypo_t_xbar, hypo_t_crit, hypo_t_df, hypo_t_pval, hypo_t_reject, hypo_t_se, hypo_t_stat, mo, np):
    _mu0 = float(hypo_t_mu0.value); _n = int(hypo_t_n.value)
    _xbar = float(hypo_t_xbar.value); _s = float(hypo_t_s.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value

    # Pre-compute strings to avoid f-string backslash issues
    if _tail == "Cola derecha (>)":
        _rej_str = "t \\geq " + f"{hypo_t_crit:.3f}"
    elif _tail == "Cola izquierda (<)":
        _rej_str = "t \\leq " + f"{hypo_t_crit:.3f}"
    else:
        _rej_str = "t \\notin [ -" + f"{hypo_t_crit:.3f}" + ", " + f"{hypo_t_crit:.3f}" + " ]"
    _decision = "🟢 **Se RECHAZA $H_0$** (evidencia significativa)" if hypo_t_reject else "🔴 **NO se rechaza $H_0$** (evidencia insuficiente)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel):**

    $$t = \frac{{\bar{{x}} - \mu_0}}{{s / \sqrt{{n}}}}
       = \frac{{{_xbar:.3f} - {_mu0:.3f}}}{{{_s:.3f} / \sqrt{{{_n}}}}}
       = \frac{{{_xbar - _mu0:.3f}}}{{{_s / np.sqrt(_n):.4f}}}
       = {hypo_t_stat:.4f}$$

    **Error estándar:** $\;SE = s/\sqrt{{n}} = {_s:.3f}/\sqrt{{{_n}}} = {hypo_t_se:.4f}$

    **Grados de libertad:** $\;df = n-1 = {hypo_t_df}$

    **Región de rechazo ({_tail}):** ${_rej_str}$

    **Valor $p$:** ${hypo_t_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7c: Z-test proporción ——————
@app.cell
def _(mo):
    hypo_p_p0 = mo.ui.slider(0.01, 0.99, value=0.5, step=0.01, label=r"$H_0:\ p_0$", show_value=True)
    hypo_p_n = mo.ui.slider(10, 1000, value=100, step=5, label="$n$", show_value=True)
    hypo_p_k = mo.ui.slider(0, 1000, value=60, step=1, label="$k$ (éxitos)", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Prueba Z para proporción**"),
        hypo_p_p0, hypo_p_n, hypo_p_k,
    ])
    return hypo_p_k, hypo_p_n, hypo_p_p0


@app.cell
def _(C, hypo_alpha, hypo_tail, hypo_p_k, hypo_p_n, hypo_p_p0, new_ax, np, stats):
    _p0 = float(hypo_p_p0.value); _n = int(hypo_p_n.value); _k = min(int(hypo_p_k.value), _n)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value
    _phat = _k / _n
    _se = np.sqrt(_p0 * (1 - _p0) / _n)
    _z = (_phat - _p0) / _se

    if _tail == "Dos colas":
        _p = 2 * stats.norm.sf(abs(_z))
        _zc = stats.norm.ppf(1 - _alpha / 2)
        _rej = (_z <= -_zc) or (_z >= _zc)
    elif _tail == "Cola derecha (>)":
        _p = stats.norm.sf(_z)
        _zc = stats.norm.ppf(1 - _alpha)
        _rej = _z >= _zc
    else:
        _p = stats.norm.cdf(_z)
        _zc = stats.norm.ppf(_alpha)
        _rej = _z <= _zc

    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _x = np.linspace(-4, 4, 800)
    _y = stats.norm.pdf(_x)
    ax.plot(_x, _y, color=C["slate"], lw=2, label=r"$H_0:\ Z\sim\mathcal{N}(0,1)$")
    if _tail == "Dos colas":
        _rej_mask = (_x <= -_zc) | (_x >= _zc)
    elif _tail == "Cola derecha (>)":
        _rej_mask = _x >= _zc
    else:
        _rej_mask = _x <= _zc
    ax.fill_between(_x, _y, where=_rej_mask, color=C["danger"], alpha=0.35, label=fr"Región de rechazo ($\alpha={_alpha:.3f}$)")
    ax.axvline(_z, color=C["primary"], lw=2.5, label=fr"$z_{{obs}}={_z:.3f}$")
    for _v in ([-_zc, _zc] if _tail == "Dos colas" else [_zc]):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.5)
    ax.set_title("Distribución bajo $H_0$ (Normal estándar) — Prueba Z para proporción")
    ax.set_xlabel("$Z$"); ax.set_ylabel("densidad"); ax._legend(loc="upper right", fontsize=8.5)

    hypo_p_stat = _z; hypo_p_pval = _p; hypo_p_crit = _zc; hypo_p_reject = _rej; hypo_p_se = _se; hypo_p_phat = _phat
    _fig
    return hypo_p_crit, hypo_p_phat, hypo_p_pval, hypo_p_reject, hypo_p_se, hypo_p_stat


@app.cell
def _(hypo_alpha, hypo_tail, hypo_p_k, hypo_p_n, hypo_p_p0, hypo_p_crit, hypo_p_phat, hypo_p_pval, hypo_p_reject, hypo_p_se, hypo_p_stat, mo, np):
    _p0 = float(hypo_p_p0.value); _n = int(hypo_p_n.value); _k = min(int(hypo_p_k.value), _n)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value

    # Pre-compute rejection region string to avoid f-string backslash issues
    if _tail == "Cola derecha (>)":
        _rej_str = f"z \\geq {hypo_p_crit:.3f}"
    elif _tail == "Cola izquierda (<)":
        _rej_str = f"z \\leq {hypo_p_crit:.3f}"
    else:
        _rej_str = f"z \\notin [ -{hypo_p_crit:.3f}, {hypo_p_crit:.3f} ]"

    _decision = "🟢 **Se RECHAZA $H_0$** (la proporción difiere significativamente de $p_0$)" if hypo_p_reject else "🔴 **NO se rechaza $H_0$** (compatible con $p_0$)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel):**

    $$\hat{{p}} = \frac{{k}}{{n}} = \frac{{{_k}}}{{{_n}}} = {hypo_p_phat:.4f}$$

    $$z = \frac{{\hat{{p}} - p_0}}{{\sqrt{{p_0(1-p_0)/n}}}}
       = \frac{{{hypo_p_phat:.4f} - {_p0:.3f}}}{{\sqrt{{{_p0:.3f}(1-{_p0:.3f})/{_n}}}}}
       = \frac{{{hypo_p_phat - _p0:.4f}}}{{{hypo_p_se:.4f}}}
       = {hypo_p_stat:.4f}$$

    **Error estándar:** $\;SE = \sqrt{{p_0(1-p_0)/n}} = {hypo_p_se:.4f}$

    **Región de rechazo ({_tail}):** ${_rej_str}$

    **Valor $p$:** ${hypo_p_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7d: t-test dos muestras (Welch) ——————
@app.cell
def _(mo):
    hypo_w_d0 = mo.ui.slider(-5.0, 5.0, value=0.0, step=0.1, label=r"$H_0:\ \Delta_0 = \mu_1-\mu_2$", show_value=True)
    hypo_w_n1 = mo.ui.slider(2, 200, value=30, step=1, label="$n_1$", show_value=True)
    hypo_w_n2 = mo.ui.slider(2, 200, value=30, step=1, label="$n_2$", show_value=True)
    hypo_w_x1 = mo.ui.slider(-10.0, 10.0, value=0.8, step=0.1, label=r"$\bar{x}_1$", show_value=True)
    hypo_w_x2 = mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$\bar{x}_2$", show_value=True)
    hypo_w_s1 = mo.ui.slider(0.1, 10.0, value=1.5, step=0.1, label="$s_1$", show_value=True)
    hypo_w_s2 = mo.ui.slider(0.1, 10.0, value=1.2, step=0.1, label="$s_2$", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Prueba t de dos muestras (Welch)**"),
        hypo_w_d0, hypo_w_n1, hypo_w_n2, hypo_w_x1, hypo_w_x2, hypo_w_s1, hypo_w_s2,
    ])
    return hypo_w_d0, hypo_w_n1, hypo_w_n2, hypo_w_s1, hypo_w_s2, hypo_w_x1, hypo_w_x2


@app.cell
def _(C, hypo_alpha, hypo_tail, hypo_w_d0, hypo_w_n1, hypo_w_n2, hypo_w_s1, hypo_w_s2, hypo_w_x1, hypo_w_x2, new_ax, np, stats):
    _d0 = float(hypo_w_d0.value); _n1 = int(hypo_w_n1.value); _n2 = int(hypo_w_n2.value)
    _x1 = float(hypo_w_x1.value); _x2 = float(hypo_w_x2.value)
    _s1 = float(hypo_w_s1.value); _s2 = float(hypo_w_s2.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value

    _se = np.sqrt(_s1**2 / _n1 + _s2**2 / _n2)
    _t = (_x1 - _x2 - _d0) / _se
    # g.l. Welch–Satterthwaite
    _df = (_s1**2/_n1 + _s2**2/_n2)**2 / ((_s1**2/_n1)**2/(_n1-1) + (_s2**2/_n2)**2/(_n2-1))
    _df = max(1, int(np.floor(_df)))

    if _tail == "Dos colas":
        _p = 2 * stats.t.sf(abs(_t), _df)
        _tc = stats.t.ppf(1 - _alpha / 2, _df)
        _rej = (_t <= -_tc) or (_t >= _tc)
    elif _tail == "Cola derecha (>)":
        _p = stats.t.sf(_t, _df)
        _tc = stats.t.ppf(1 - _alpha, _df)
        _rej = _t >= _tc
    else:
        _p = stats.t.cdf(_t, _df)
        _tc = stats.t.ppf(_alpha, _df)
        _rej = _t <= _tc

    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _x = np.linspace(-4, 4, 800)
    _y = stats.t.pdf(_x, _df)
    ax.plot(_x, _y, color=C["slate"], lw=2, label=fr"$H_0:\ t\sim t_{{{_df}}}$")
    if _tail == "Dos colas":
        _rej_mask = (_x <= -_tc) | (_x >= _tc)
    elif _tail == "Cola derecha (>)":
        _rej_mask = _x >= _tc
    else:
        _rej_mask = _x <= _tc
    ax.fill_between(_x, _y, where=_rej_mask, color=C["danger"], alpha=0.35, label=fr"Región de rechazo ($\alpha={_alpha:.3f}$)")
    ax.axvline(_t, color=C["primary"], lw=2.5, label=fr"$t_{{obs}}={_t:.3f}$")
    for _v in ([-_tc, _tc] if _tail == "Dos colas" else [_tc]):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.5)
    ax.set_title(f"Distribución $t$ bajo $H_0$ (g.l.≈{_df}) — Welch dos muestras")
    ax.set_xlabel("$t$"); ax.set_ylabel("densidad"); ax._legend(loc="upper right", fontsize=8.5)

    hypo_w_stat = _t; hypo_w_pval = _p; hypo_w_crit = _tc; hypo_w_reject = _rej; hypo_w_se = _se; hypo_w_df = _df
    _fig
    return hypo_w_crit, hypo_w_df, hypo_w_pval, hypo_w_reject, hypo_w_se, hypo_w_stat


@app.cell
def _(hypo_alpha, hypo_tail, hypo_w_d0, hypo_w_n1, hypo_w_n2, hypo_w_s1, hypo_w_s2, hypo_w_x1, hypo_w_x2, hypo_w_crit, hypo_w_df, hypo_w_pval, hypo_w_reject, hypo_w_se, hypo_w_stat, mo, np):
    _d0 = float(hypo_w_d0.value); _n1 = int(hypo_w_n1.value); _n2 = int(hypo_w_n2.value)
    _x1 = float(hypo_w_x1.value); _x2 = float(hypo_w_x2.value)
    _s1 = float(hypo_w_s1.value); _s2 = float(hypo_w_s2.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value

    # Pre-compute strings to avoid f-string backslash issues
    if _tail == "Cola derecha (>)":
        _rej_str = "t \\geq " + f"{hypo_w_crit:.3f}"
    elif _tail == "Cola izquierda (<)":
        _rej_str = "t \\leq " + f"{hypo_w_crit:.3f}"
    else:
        _rej_str = "t \\notin [ -" + f"{hypo_w_crit:.3f}" + ", " + f"{hypo_w_crit:.3f}" + " ]"
    _decision = "🟢 **Se RECHAZA $H_0$** (diferencia significativa entre medias)" if hypo_w_reject else "🔴 **NO se rechaza $H_0$** (sin evidencia de diferencia)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel — Welch):**

    $$SE = \sqrt{{\frac{{s_1^2}}{{n_1}} + \frac{{s_2^2}}{{n_2}}}}
       = \sqrt{{\frac{{{_s1:.3f}^2}}{{{_n1}}} + \frac{{{_s2:.3f}^2}}{{{_n2}}}}}
       = {hypo_w_se:.4f}$$

    $$t = \frac{{(\bar{{x}}_1 - \bar{{x}}_2) - \Delta_0}}{{SE}}
       = \frac{{({_x1:.3f} - {_x2:.3f}) - {_d0:.3f}}}{{{hypo_w_se:.4f}}}
       = {hypo_w_stat:.4f}$$

    **Grados de libertad (Welch–Satterthwaite):**
    $$df = \frac{{(s_1^2/n_1 + s_2^2/n_2)^2}}{{(s_1^2/n_1)^2/(n_1-1) + (s_2^2/n_2)^2/(n_2-1)}} \approx {hypo_w_df}$$

    **Región de rechazo ({_tail}):** ${_rej_str}$

    **Valor $p$:** ${hypo_w_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7e: χ² bondad de ajuste ——————
@app.cell
def _(mo):
    hypo_gof_k = mo.ui.slider(2, 12, value=6, step=1, label="$k$ (categorías)", show_value=True)
    hypo_gof_N = mo.ui.slider(10, 2000, value=300, step=10, label="$N$ (total)", show_value=True)
    hypo_gof_bias = mo.ui.slider(0.0, 1.0, value=0.2, step=0.02, label="Sesgo teórico (0=uniforme)", show_value=True)
    hypo_gof_seed = mo.ui.slider(0, 40, value=1, step=1, label="Semilla", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Bondad de ajuste χ²**"),
        hypo_gof_k, hypo_gof_N, hypo_gof_bias, hypo_gof_seed,
    ])
    return hypo_gof_N, hypo_gof_bias, hypo_gof_k, hypo_gof_seed


@app.cell
def _(C, hypo_alpha, hypo_gof_N, hypo_gof_bias, hypo_gof_k, hypo_gof_seed, new_ax, np, stats):
    _rng = np.random.default_rng(int(hypo_gof_seed.value))
    _k = int(hypo_gof_k.value); _N = int(hypo_gof_N.value); _bias = float(hypo_gof_bias.value)
    _alpha = float(hypo_alpha.value)

    _probs = np.ones(_k) / _k
    _tilt = np.linspace(1.0, 1.0 + 2.0 * _bias, _k)
    _probs = _tilt / _tilt.sum()
    _obs = _rng.multinomial(_N, _probs)
    _exp = np.full(_k, _N / _k)
    _chi2, _pval = stats.chisquare(_obs, _exp)
    _df = _k - 1
    _chi2_crit = stats.chi2.ppf(1 - _alpha, _df)
    _rej = _chi2 >= _chi2_crit

    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _idx = np.arange(1, _k + 1)
    ax.bar(_idx - 0.19, _obs, width=0.38, color=C["primary"], alpha=0.85, label="Observado $O_i$")
    ax.bar(_idx + 0.19, _exp, width=0.38, color=C["muted"], alpha=0.85, label="Esperado $E_i$")
    ax.set_xticks(_idx)
    ax.set_title(f"Bondad de ajuste χ² (g.l.={_df}) — Observado vs Esperado")
    ax.set_xlabel("categoría"); ax.set_ylabel("conteo"); ax._legend()

    hypo_gof_chi2 = _chi2; hypo_gof_pval = _pval; hypo_gof_crit = _chi2_crit; hypo_gof_reject = _rej; hypo_gof_df = _df; hypo_gof_obs = _obs; hypo_gof_exp = _exp
    _fig
    return hypo_gof_chi2, hypo_gof_crit, hypo_gof_df, hypo_gof_exp, hypo_gof_obs, hypo_gof_pval, hypo_gof_reject


@app.cell
def _(hypo_alpha, hypo_gof_N, hypo_gof_bias, hypo_gof_k, hypo_gof_chi2, hypo_gof_crit, hypo_gof_df, hypo_gof_exp, hypo_gof_obs, hypo_gof_pval, hypo_gof_reject, mo, np):
    _k = int(hypo_gof_k.value); _N = int(hypo_gof_N.value)
    _alpha = float(hypo_alpha.value)

    # Fórmula con valores (suma de (O-E)²/E)
    _terms = [(o, e, (o-e)**2/e) for o, e in zip(hypo_gof_obs, hypo_gof_exp)]
    _terms_str = " + ".join([f"({o:.1f}-{e:.1f})²/{e:.1f}={t:.3f}" for o, e, t in _terms])

    _decision = "🟢 **Se RECHAZA $H_0$** (la distribución observada difiere de la teórica)" if hypo_gof_reject else "🔴 **NO se rechaza $H_0$** (compatible con la distribución teórica)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel — χ² bondad de ajuste):**

    $$\\chi^2 = \\sum_{{i=1}}^{{k}} \\frac{{(O_i - E_i)^2}}{{E_i}}
       = {_terms_str}
       = {hypo_gof_chi2:.4f}$$

    **Grados de libertad:** $\\;df = k-1 = {hypo_gof_df}$

    **Valor crítico ($\\alpha={_alpha:.3f}$, cola derecha):** $\\chi^2_{{crit}} = {hypo_gof_crit:.3f}$

    **Valor $p$ (cola derecha):** ${hypo_gof_pval:.6f}$ &nbsp;|&nbsp; **$\\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7f: χ² independencia (2×2) ——————
@app.cell
def _(mo):
    hypo_chi2_a = mo.ui.slider(0, 200, value=50, step=1, label="$a$ (fila 1, col 1)", show_value=True)
    hypo_chi2_b = mo.ui.slider(0, 200, value=30, step=1, label="$b$ (fila 1, col 2)", show_value=True)
    hypo_chi2_c = mo.ui.slider(0, 200, value=20, step=1, label="$c$ (fila 2, col 1)", show_value=True)
    hypo_chi2_d = mo.ui.slider(0, 200, value=40, step=1, label="$d$ (fila 2, col 2)", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Independencia χ² (tabla 2×2)**"),
        mo.md("Tabla observada:"),
        mo.md("| | Col 1 | Col 2 | Total |"),
        mo.md("|---|---|---|---|"),
        mo.md(f"| Fila 1 | {hypo_chi2_a.value} | {hypo_chi2_b.value} | {hypo_chi2_a.value + hypo_chi2_b.value} |"),
        mo.md(f"| Fila 2 | {hypo_chi2_c.value} | {hypo_chi2_d.value} | {hypo_chi2_c.value + hypo_chi2_d.value} |"),
        mo.md(f"| Total | {hypo_chi2_a.value + hypo_chi2_c.value} | {hypo_chi2_b.value + hypo_chi2_d.value} | {hypo_chi2_a.value + hypo_chi2_b.value + hypo_chi2_c.value + hypo_chi2_d.value} |"),
        hypo_chi2_a, hypo_chi2_b, hypo_chi2_c, hypo_chi2_d,
    ])
    return hypo_chi2_a, hypo_chi2_b, hypo_chi2_c, hypo_chi2_d


@app.cell
def _(C, hypo_alpha, hypo_chi2_a, hypo_chi2_b, hypo_chi2_c, hypo_chi2_d, new_ax, np, stats):
    _a = int(hypo_chi2_a.value); _b = int(hypo_chi2_b.value)
    _c = int(hypo_chi2_c.value); _d = int(hypo_chi2_d.value)
    _alpha = float(hypo_alpha.value)

    _obs = np.array([[_a, _b], [_c, _d]])
    _chi2, _pval, _df, _exp = stats.chi2_contingency(_obs, correction=False)
    _chi2_crit = stats.chi2.ppf(1 - _alpha, _df)
    _rej = _chi2 >= _chi2_crit

    _fig, _ax = new_ax(_figsize=(7.0, 4.0))
    _labels = ["Col 1", "Col 2"]
    _x = np.arange(2); _w = 0.35
    ax.bar(_x - _w/2, _obs[0], _w, color=C["primary"], alpha=0.85, label="Fila 1 (obs)")
    ax.bar(_x + _w/2, _obs[1], _w, color=C["accent"], alpha=0.85, label="Fila 2 (obs)")
    ax.bar(_x - _w/2, _exp[0], _w, color=C["primary"], alpha=0.25, hatch="//", edgecolor=C["primary"], label="Esperado")
    ax.bar(_x + _w/2, _exp[1], _w, color=C["accent"], alpha=0.25, hatch="//", edgecolor=C["accent"])
    ax.set_xticks(_x); ax.set_xticklabels(_labels)
    ax.set_title("Tabla 2×2: Observado vs Esperado (independencia)")
    ax.set_ylabel("conteo"); ax._legend(fontsize=8)

    hypo_chi2_stat = _chi2; hypo_chi2_pval = _pval; hypo_chi2_crit = _chi2_crit; hypo_chi2_reject = _rej; hypo_chi2_df = _df; hypo_chi2_exp = _exp; hypo_chi2_obs = _obs
    _fig
    return hypo_chi2_crit, hypo_chi2_df, hypo_chi2_exp, hypo_chi2_obs, hypo_chi2_pval, hypo_chi2_reject, hypo_chi2_stat


@app.cell
def _(hypo_alpha, hypo_chi2_a, hypo_chi2_b, hypo_chi2_c, hypo_chi2_d, hypo_chi2_crit, hypo_chi2_df, hypo_chi2_exp, hypo_chi2_obs, hypo_chi2_pval, hypo_chi2_reject, hypo_chi2_stat, mo, np):
    _a = int(hypo_chi2_a.value); _b = int(hypo_chi2_b.value)
    _c = int(hypo_chi2_c.value); _d = int(hypo_chi2_d.value)
    _alpha = float(hypo_alpha.value)
    _N = _a + _b + _c + _d

    _r1 = _a + _b; _r2 = _c + _d
    _c1 = _a + _c; _c2 = _b + _d

    _terms = []
    for i in range(2):
        for j in range(2):
            o = hypo_chi2_obs[i, j]
            e = hypo_chi2_exp[i, j]
            _terms.append(f"({o:.1f}-{e:.1f})²/{e:.1f}={(o-e)**2/e:.3f}")
    _terms_str = " + ".join(_terms)

    _decision = "🟢 **Se RECHAZA $H_0$** (las variables **no** son independientes)" if hypo_chi2_reject else "🔴 **NO se rechaza $H_0$** (compatibles con independencia)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel — χ² independencia 2×2):**

    **Totales marginales:**
    $$R_1={_r1},\; R_2={_r2},\; C_1={_c1},\; C_2={_c2},\; N={_N}$$

    **Frecuencias esperadas:** $E_{{ij}} = \frac{{R_i C_j}}{{N}}$
    $$E_{{11}}=\frac{{{_r1}\times{_c1}}}{{{_N}}}={hypo_chi2_exp[0,0]:.2f},\quad
       E_{{12}}=\frac{{{_r1}\times{_c2}}}{{{_N}}}={hypo_chi2_exp[0,1]:.2f},\quad
       E_{{21}}=\frac{{{_r2}\times{_c1}}}{{{_N}}}={hypo_chi2_exp[1,0]:.2f},\quad
       E_{{22}}=\frac{{{_r2}\times{_c2}}}{{{_N}}}={hypo_chi2_exp[1,1]:.2f}$$

    $$\chi^2 = \sum \frac{{(O-E)^2}}{{E}}
       = {_terms_str}
       = {hypo_chi2_stat:.4f}$$

    **Grados de libertad:** $\;df = (2-1)(2-1) = {hypo_chi2_df}$

    **Valor crítico ($\alpha={_alpha:.3f}$):** $\chi^2_{{crit}} = {hypo_chi2_crit:.3f}$

    **Valor $p$:** ${hypo_chi2_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# —————— 7g: Prueba F varianzas ——————
@app.cell
def _(mo):
    hypo_f_n1 = mo.ui.slider(2, 200, value=25, step=1, label="$n_1$", show_value=True)
    hypo_f_n2 = mo.ui.slider(2, 200, value=30, step=1, label="$n_2$", show_value=True)
    hypo_f_v1 = mo.ui.slider(0.1, 10.0, value=2.0, step=0.1, label="$s_1^2$", show_value=True)
    hypo_f_v2 = mo.ui.slider(0.1, 10.0, value=1.0, step=0.1, label="$s_2^2$", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Prueba F para igualdad de varianzas**"),
        hypo_f_n1, hypo_f_n2, hypo_f_v1, hypo_f_v2,
    ])
    return hypo_f_n1, hypo_f_n2, hypo_f_v1, hypo_f_v2


@app.cell
def _(C, hypo_alpha, hypo_tail, hypo_f_n1, hypo_f_n2, hypo_f_v1, hypo_f_v2, new_ax, np, stats):
    _n1 = int(hypo_f_n1.value); _n2 = int(hypo_f_n2.value)
    _v1 = float(hypo_f_v1.value); _v2 = float(hypo_f_v2.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value
    _df1 = _n1 - 1; _df2 = _n2 - 1

    # F = varianza mayor / varianza menor (dos colas simétrica en log, pero convencional: max/min)
    if _v1 >= _v2:
        _F = _v1 / _v2
        _df_num, _df_den = _df1, _df2
    else:
        _F = _v2 / _v1
        _df_num, _df_den = _df2, _df1

    if _tail == "Dos colas":
        _p = 2 * min(stats.f.cdf(_F, _df_num, _df_den), stats.f.sf(_F, _df_num, _df_den))
        _Fc_low = stats.f.ppf(_alpha / 2, _df_num, _df_den)
        _Fc_high = stats.f.ppf(1 - _alpha / 2, _df_num, _df_den)
        _rej = (_F <= _Fc_low) or (_F >= _Fc_high)
    elif _tail == "Cola derecha (>)":
        _p = stats.f.sf(_F, _df_num, _df_den)
        _Fc = stats.f.ppf(1 - _alpha, _df_num, _df_den)
        _rej = _F >= _Fc
    else:
        _p = stats.f.cdf(_F, _df_num, _df_den)
        _Fc = stats.f.ppf(_alpha, _df_num, _df_den)
        _rej = _F <= _Fc

    _fig, _ax = new_ax(_figsize=(9.0, 4.0))
    _x = np.linspace(0, max(5, _F * 1.5), 800)
    _y = stats.f.pdf(_x, _df_num, _df_den)
    ax.plot(_x, _y, color=C["slate"], lw=2, label=fr"$H_0:\ F\sim F_{{{_df_num},{_df_den}}}$")
    if _tail == "Dos colas":
        _rej_mask = (_x <= _Fc_low) | (_x >= _Fc_high)
    elif _tail == "Cola derecha (>)":
        _rej_mask = _x >= _Fc
    else:
        _rej_mask = _x <= _Fc
    ax.fill_between(_x, _y, where=_rej_mask, color=C["danger"], alpha=0.35, label=fr"Región de rechazo ($\alpha={_alpha:.3f}$)")
    ax.axvline(_F, color=C["primary"], lw=2.5, label=fr"$F_{{obs}}={_F:.3f}$")
    for _v in ([_Fc_low, _Fc_high] if _tail == "Dos colas" else [_Fc]):
        ax.axvline(_v, color=C["danger"], ls="--", lw=1.5)
    ax.set_title(f"Distribución $F$ bajo $H_0$ (g.l.={_df_num},{_df_den}) — Prueba de varianzas")
    ax.set_xlabel("$F$"); ax.set_ylabel("densidad"); ax._legend(loc="upper right", fontsize=8.5)

    hypo_f_stat = _F; hypo_f_pval = _p; hypo_f_crit = (_Fc_low, _Fc_high) if _tail=="Dos colas" else _Fc
    hypo_f_reject = _rej; hypo_f_df1 = _df_num; hypo_f_df2 = _df_den
    _fig
    return hypo_f_crit, hypo_f_df1, hypo_f_df2, hypo_f_pval, hypo_f_reject, hypo_f_stat


@app.cell
def _(hypo_alpha, hypo_tail, hypo_f_n1, hypo_f_n2, hypo_f_v1, hypo_f_v2, hypo_f_crit, hypo_f_df1, hypo_f_df2, hypo_f_pval, hypo_f_reject, hypo_f_stat, mo):
    _n1 = int(hypo_f_n1.value); _n2 = int(hypo_f_n2.value)
    _v1 = float(hypo_f_v1.value); _v2 = float(hypo_f_v2.value)
    _alpha = float(hypo_alpha.value); _tail = hypo_tail.value
    _df1 = _n1 - 1; _df2 = _n2 - 1

    if _tail == "Dos colas":
        _crit_str = f"{hypo_f_crit[0]:.3f} (inf) / {hypo_f_crit[1]:.3f} (sup)"
    else:
        _crit_str = f"{hypo_f_crit:.3f}"

    _decision = "🟢 **Se RECHAZA $H_0$** (las varianzas son **diferentes**)" if hypo_f_reject else "🔴 **NO se rechaza $H_0$** (compatibles con varianzas iguales)"

    _formula = rf"""
    **Fórmula con tus valores (estilo Excel — Prueba F varianzas):**

    $$F = \frac{{\max(s_1^2, s_2^2)}}{{\min(s_1^2, s_2^2)}}
       = \frac{{{max(_v1, _v2):.3f}}}{{{min(_v1, _v2):.3f}}}
       = {hypo_f_stat:.4f}$$

    **Grados de libertad:** $\;df_1 = n_1-1 = {hypo_f_df1},\quad df_2 = n_2-1 = {hypo_f_df2}$

    **Región de rechazo ({_tail}):** valores críticos = {_crit_str}

    **Valor $p$:** ${hypo_f_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

    **Decisión:** {_decision}
    """
    mo.vstack([mo.md(_formula)])
    return


# ============================================================================
# MOSTRAR SOLO LA PRUEBA SELECCIONADA (renderizado condicional via markdown)
# ============================================================================
@app.cell
def _(hypo_test_type, mo):
    _sel = hypo_test_type.value
    _map = {
        "Prueba Z: media (σ conocida)": "🔹 **Prueba Z para la media** (σ conocida) — sliders arriba ↖️",
        "Prueba t: media (σ desconocida)": "🔹 **Prueba t de Student** para la media — sliders arriba ↖️",
        "Prueba Z: proporción": "🔹 **Prueba Z para proporción** — sliders arriba ↖️",
        "Prueba t: dos muestras (Welch)": "🔹 **Prueba t de dos muestras (Welch)** — sliders arriba ↖️",
        "Prueba χ²: bondad de ajuste": "🔹 **Prueba χ² bondad de ajuste** — sliders arriba ↖️",
        "Prueba χ²: independencia (2×2)": "🔹 **Prueba χ² independencia (2×2)** — sliders arriba ↖️",
        "Prueba F: varianzas (dos muestras)": "🔹 **Prueba F para varianzas** — sliders arriba ↖️",
    }
    mo.md(f"{_map.get(_sel, _sel)}\n\n*Cambia el **tipo de prueba** en el dropdown general para ver sus controles.*")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


# ============================================================================
# CIERRE: GLOSARIO Y REFERENCIAS
# ============================================================================
@app.cell
def _(mo):
    mo.accordion({
        "📖 Glosario ES / EN (términos técnicos)": mo.md(
            r"""
            | Español | English | Símbolo |
            |---|---|---|
            | Población / Muestra | Population / Sample | — |
            | Estimador | Estimator | $\hat\theta$ |
            | Error estándar | Standard error | $SE$ |
            | Teorema del límite central | Central limit theorem | TLC / CLT |
            | Hipótesis nula / alternativa | Null / Alternative hypothesis | $H_0,\ H_1$ |
            | Nivel de significancia | Significance level | $\alpha$ |
            | Valor p | p-value | $p$ |
            | Potencia | Power | $1-\beta$ |
            | Error Tipo I / II | Type I / II error | $\alpha,\ \beta$ |
            | Bondad de ajuste | Goodness of fit | $\chi^2$ |
            | Mínimos cuadrados | Least squares | OLS |
            | Coef. de determinación | Coefficient of determination | $R^2$ |
            | Razón de momios | Odds ratio | $e^{\beta}$ |
            | Confusor | Confounder | $Z$ |
            | Correlación parcial | Partial correlation | $r_{XY\cdot Z}$ |
            """
        ),
        "📚 Para profundizar": mo.md(
            r"""
            - Wasserman, *All of Statistics* — referencia compacta y rigurosa.
            - Downey, *Think Stats* — enfoque computacional (Python), gratuito.
            - Pearl & Mackenzie, *The Book of Why* — causalidad e inferencia.
            - Documentación de `scipy.stats` y de `marimo` para extender este cuaderno.
            """
        ),
    })
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### 🎯 Síntesis en una frase por tema
            - **Inferencia:** la muestra habla de la población, con un error que encoge como $1/\sqrt{n}$.
            - **Distribuciones:** cinco moldes de una misma familia unida por límites.
            - **Valor $p$ / $\alpha$:** cuánta sorpresa toleras antes de rechazar $H_0$.
            - **Pruebas:** la distribución + la pregunta eligen la herramienta.
            - **Regresión:** lineal predice cantidades; logística, probabilidades.
            - **Correlación ≠ causalidad:** sin controlar confusores, todo número miente.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
