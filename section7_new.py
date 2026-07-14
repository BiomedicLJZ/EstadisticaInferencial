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
        return mo.vstack([
            mo.md("**Parámetros — Prueba Z para la media (σ conocida)**"),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$ (media poblacional bajo nula)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.5, step=0.1, label=r"$\sigma$ (desv. estándar poblacional conocida)", show_value=True),
            mo.ui.slider(1, 500, value=30, step=1, label="$n$ (tamaño de muestra)", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.5, step=0.1, label=r"$\bar{x}$ (media muestral observada)", show_value=True),
        ])
    elif _sel == "Prueba t: media (σ desconocida)":
        return mo.vstack([
            mo.md("**Parámetros — Prueba t de Student para la media**"),
            mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$", show_value=True),
            mo.ui.slider(1, 200, value=25, step=1, label="$n$", show_value=True),
            mo.ui.slider(-10.0, 10.0, value=0.6, step=0.1, label=r"$\bar{x}$ (media muestral)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.2, step=0.1, label="$s$ (desv. estándar muestral)", show_value=True),
        ])
    elif _sel == "Prueba Z: proporción":
        return mo.vstack([
            mo.md("**Parámetros — Prueba Z para proporción**"),
            mo.ui.slider(0.01, 0.99, value=0.5, step=0.01, label=r"$H_0:\ p_0$ (proporción bajo nula)", show_value=True),
            mo.ui.slider(10, 1000, value=100, step=5, label="$n$ (ensayos)", show_value=True),
            mo.ui.slider(0, 1000, value=60, step=1, label="$k$ (éxitos observados)", show_value=True),
        ])
    elif _sel == "Prueba t: dos muestras (Welch)":
        return mo.vstack([
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
        return mo.vstack([
            mo.md("**Parámetros — Bondad de ajuste χ² (multinomial vs teórica)**"),
            mo.ui.slider(2, 12, value=6, step=1, label="$k$ (número de categorías)", show_value=True),
            mo.ui.slider(10, 2000, value=300, step=10, label="$N$ (tamaño total)", show_value=True),
            mo.ui.slider(0.0, 1.0, value=0.2, step=0.02, label="Sesgo en probabilidades teóricas (0=uniforme)", show_value=True),
            mo.ui.slider(0, 40, value=1, step=1, label="Semilla (re-muestrear observados)", show_value=True),
        ])
    elif _sel == "Prueba χ²: independencia (2×2)":
        return mo.vstack([
            mo.md("**Parámetros — Independencia χ² (tabla 2×2)**"),
            mo.ui.slider(0, 200, value=50, step=1, label="$a$ (fila 1, col 1)", show_value=True),
            mo.ui.slider(0, 200, value=30, step=1, label="$b$ (fila 1, col 2)", show_value=True),
            mo.ui.slider(0, 200, value=20, step=1, label="$c$ (fila 2, col 1)", show_value=True),
            mo.ui.slider(0, 200, value=40, step=1, label="$d$ (fila 2, col 2)", show_value=True),
        ])
    else:  # Prueba F: varianzas
        return mo.vstack([
            mo.md("**Parámetros — Prueba F para igualdad de varianzas**"),
            mo.ui.slider(2, 200, value=25, step=1, label="$n_1$", show_value=True),
            mo.ui.slider(2, 200, value=30, step=1, label="$n_2$", show_value=True),
            mo.ui.slider(0.1, 10.0, value=2.0, step=0.1, label="$s_1^2$ (varianza muestra 1)", show_value=True),
            mo.ui.slider(0.1, 10.0, value=1.0, step=0.1, label="$s_2^2$ (varianza muestra 2)", show_value=True),
        ])


# —————— 7a: Z-test media (σ conocida) ——————
@app.cell
def _(mo):
    hypo_z_mu0 = mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label=r"$H_0:\ \mu_0$", show_value=True)
    hypo_z_sigma = mo.ui.slider(0.1, 10.0, value=1.5, step=0.1, label=r"$\sigma$ (poblacional)", show_value=True)
    hypo_z_n = mo.ui.slider(1, 500, value=30, step=1, label="$n$", show_value=True)
    hypo_z_xbar = mo.ui.slider(-10.0, 10.0, value=0.5, step=0.1, label=r"$\bar{x}$ (observada)", show_value=True)
    mo.vstack([
        mo.md("**Parámetros — Prueba Z para la media (σ conocida)**"),
        hypo_z_mu0, hypo_z_sigma, hypo_z_n, hypo_z_xbar,
    ])
    return hypo_z_mu0, hypo_z_n, hypo_z_sigma, hypo_z_xbar


@app.cell
def _(C, hypo_alpha, hypo_tail, hypo_z_mu0, hypo_z_n, hypo_z_sigma, hypo_z_xbar, new_ax, np, stats):
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
        _rej = (_z <= -_zc) or (_z >= _zc)
    elif _tail == "Cola derecha (>)":
        _p = stats.norm.sf(_z)
        _zc = stats.norm.ppf(1 - _alpha)
        _rej = _z >= _zc
    else:  # Cola izquierda
        _p = stats.norm.cdf(_z)
        _zc = stats.norm.ppf(_alpha)
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
        _rej_str = "z \\geq " + f"{hypo_p_crit:.3f}"
    elif _tail == "Cola izquierda (<)":
        _rej_str = "z \\leq " + f"{hypo_p_crit:.3f}"
    else:
        _rej_str = "z \\notin [ -" + f"{hypo_p_crit:.3f}" + ", " + f"{hypo_p_crit:.3f}" + " ]"

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

    $$\chi^2 = \sum_{{i=1}}^{{k}} \frac{{(O_i - E_i)^2}}{{E_i}}
       = {_terms_str}
       = {hypo_gof_chi2:.4f}$$

    **Grados de libertad:** $\;df = k-1 = {hypo_gof_df}$

    **Valor crítico ($\alpha={_alpha:.3f}$, cola derecha):** $\chi^2_{{crit}} = {hypo_gof_crit:.3f}$

    **Valor $p$ (cola derecha):** ${hypo_gof_pval:.6f}$ &nbsp;|&nbsp; **$\alpha$:** ${_alpha:.3f}$

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