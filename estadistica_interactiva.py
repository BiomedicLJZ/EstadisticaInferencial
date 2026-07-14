# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "scipy",
#     "plotly",
#     "ipywidgets",
# ]
# ///

import marimo as mo

__generated_with = "0.11.12"
app = mo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    from scipy import stats
    from scipy.stats import norm, t, chi2, f, binom, poisson, nct
    import numpy.random as rnd
    import warnings
    warnings.filterwarnings('ignore')

    # Configuración de estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12

    mo.md(r"""
    # 📊 **Estadística Inferencial Interactiva**

    Un cuaderno interactivo completo que cubre:
    - **Intervalos de Confianza** (IC)
    - **Valor p y Significancia Estadística**
    - **Tipos de Error** (Tipo I y II)
    - **Pruebas Estadísticas** (t, Z, χ², F, etc.)
    - **Pruebas de Hipótesis** (H₀ vs H₁)
    - **Inferencia Estadística**
    - **Simulador Interactivo Integral**

    ---
    """)
    return mo, np, pd, plt, sns, go, px, make_subplots, stats, norm, t, chi2, f, binom, poisson, nct, rnd, warnings


@app.cell
def _(mo):
    mo.md(r"""
    ## 📚 **Tabla de Contenidos Interactiva**

    Selecciona una sección para explorar:
    """)
    
    tabs = mo.ui.tabs({
        "📊 Intervalos de Confianza": "ic",
        "📈 Valor p y Significancia": "pval",
        "⚠️ Tipos de Error": "errores",
        "🧪 Pruebas Estadísticas": "pruebas",
        "🔬 Pruebas de Hipótesis": "hipotesis",
        "📊 Inferencia Estadística": "inferencia",
        "🎯 Simulador Integral": "simulador",
    })
    return tabs


# =============================================
# TAB 1: INTERVALOS DE CONFIANZA
# =============================================
@app.cell
def _(tabs):
    if tabs.value != "ic":
        mo.md("")
    mo.md(r"""
    ## 📊 **Intervalos de Confianza (IC)**

    Un **intervalo de confianza** es un rango de valores que probablemente contiene el parámetro poblacional verdadero con un cierto nivel de confianza (ej. 95%).

    ### 📐 **Fórmula General**
    $$IC = \text{estimador} \pm (\text{valor crítico}) \times (\text{error estándar})$$

    ### 📐 **Fórmulas Comunes**

    | Parámetro | Estimador | Error Estándar | Valor Crítico |
    |-----------|-----------|----------------|---------------|
    | Media (σ conocida) | $\bar{x}$ | $\sigma/\sqrt{n}$ | $Z_{\alpha/2}$ |
    | Media (σ desconocida) | $\bar{x}$ | $s/\sqrt{n}$ | $t_{\alpha/2, n-1}$ |
    | Proporción | $\hat{p}$ | $\sqrt{\hat{p}(1-\hat{p})/n}$ | $Z_{\alpha/2}$ |
    | Varianza | $s^2$ | - | $\chi^2_{\alpha/2, n-1}$ |
    | Diferencia de medias | $\bar{x}_1 - \bar{x}_2$ | $\sqrt{s_1^2/n_1 + s_2^2/n_2}$ | $t$ o $Z$ |

    ### 🎯 **Interpretación Correcta**
    > **"Estamos 95% seguros de que el intervalo [L, U] contiene el parámetro verdadero"**
    > ❌ NO: "Hay 95% de probabilidad de que el parámetro esté en [L, U]"
    """)
    
    # UI interactiva para IC
    mo.md("### 🎛️ **Simulador Interactivo de Intervalos de Confianza**")
    
    col1, col2, col3 = mo.ui.columns([1, 1, 1])
    with col1:
        n_ic = mo.ui.slider(10, 500, value=30, label="Tamaño de muestra (n)")
    with col2:
        conf_level = mo.ui.slider(0.80, 0.99, value=0.95, step=0.01, label="Nivel de confianza")
    with col3:
        pop_mean = mo.ui.slider(0, 100, value=50, label="Media poblacional real (μ)")
    
    col4, col5 = mo.ui.columns([1, 1])
    with col4:
        pop_std = mo.ui.slider(1, 50, value=15, label="Desv. estándar poblacional (σ)")
    with col5:
        n_sim = mo.ui.slider(10, 500, value=50, label="Número de simulaciones")
    
    return n_ic, conf_level, pop_mean, pop_std, n_sim


@app.cell
def _(n_ic, conf_level, pop_mean, pop_std, n_sim, mo, np, pd, plt, sns, go, px, make_subplots, stats, norm, t, chi2, f, binom, poisson, nct, rnd, warnings):
    if n_ic is None or n_ic.value is None:
        mo.md("")
    else:
        n = n_ic.value
        conf = conf_level.value
        mu = pop_mean.value
        sigma = pop_std.value
        n_sims = n_sim.value
        
        alpha = 1 - conf
        z_crit = norm.ppf(1 - alpha/2)
        
        # Simular múltiples muestras
        np.random.seed(42)
        sample_means = np.random.normal(mu, sigma/np.sqrt(n), n_sims)
        sample_stds = np.array([np.std(np.random.normal(mu, sigma, n), ddof=1) for _ in range(n_sims)])
        
        # Calcular ICs (usando sigma conocida - Z)
        lower_z = sample_means - z_crit * sigma / np.sqrt(n)
        upper_z = sample_means + z_crit * sigma / np.sqrt(n)
        contains_mu_z = (lower_z <= mu) & (upper_z >= mu)
        coverage_z = contains_mu_z.mean() * 100
        
        # Calcular ICs (usando t con sigma muestral)
        t_crit = t.ppf(1 - alpha/2, n-1)
        lower_t = sample_means - t_crit * sample_stds / np.sqrt(n)
        upper_t = sample_means + t_crit * sample_stds / np.sqrt(n)
        contains_mu_t = (lower_t <= mu) & (upper_t >= mu)
        coverage_t = contains_mu_t.mean() * 100
        
        # Gráfico interactivo con Plotly
        fig = make_subplots(rows=2, cols=1, 
                            subplot_titles=(f'IC al {conf*100:.0f}% (Z, σ conocida) - Cobertura: {coverage_z:.1f}%',
                                            f'IC al {conf*100:.0f}% (t, σ muestral) - Cobertura: {coverage_t:.1f}%'),
                            vertical_spacing=0.15)
        
        colors_z = ['green' if c else 'red' for c in contains_mu_z]
        colors_t = ['green' if c else 'red' for c in contains_mu_t]
        
        for i in range(min(n_sims, 50)):
            fig.add_trace(go.Scatter(x=[lower_z[i], upper_z[i]], y=[i, i], 
                                     mode='lines', line=dict(color=colors_z[i], width=2),
                                     showlegend=False, hoverinfo='skip'), row=1, col=1)
            fig.add_trace(go.Scatter(x=[lower_t[i], upper_t[i]], y=[i, i], 
                                     mode='lines', line=dict(color=colors_t[i], width=2),
                                     showlegend=False, hoverinfo='skip'), row=2, col=1)
        
        # Línea de media poblacional
        fig.add_vline(x=mu, line=dict(color='red', dash='dash', width=2), 
                      annotation_text=f"μ = {mu}", annotation_position="top")
        
        fig.update_layout(height=700, showlegend=False, template='plotly_white')
        fig.update_xaxes(title_text="Valor del parámetro")
        fig.update_yaxes(title_text="Simulación #")
        
        mo.ui.plotly(fig)
        
        # Estadísticas resumen
        mo.md(f"""
        ### 📈 **Resultados de la Simulación**
        
        | Métrica | Z (σ conocida) | t (σ muestral) |
        |---------|----------------|----------------|
        | **Cobertura real** | {coverage_z:.1f}% | {coverage_t:.1f}% |
        | **Nivel nominal** | {conf*100:.0f}% | {conf*100:.0f}% |
        | **Ancho promedio IC** | {np.mean(upper_z - lower_z):.2f} | {np.mean(upper_t - lower_t):.2f} |
        | **ICs que contienen μ** | {contains_mu_z.sum()}/{n_sims} | {contains_mu_t.sum()}/{n_sims} |
        
        ---
        ### 📐 **Fórmula del IC para la Media (σ conocida)**
        $$IC_{{1-\\alpha}} = \\bar{x} \\pm Z_{{\\alpha/2}} \\frac{{\\sigma}}{{\\sqrt{{n}}}}$$
        
        - **Z_{{α/2}}** = {z_crit:.3f} (para confianza {conf*100:.0f}%)
        - **Error estándar** = σ/√n = {sigma:.2f}/√{n} = {sigma/np.sqrt(n):.3f}
        - **Margen de error** = {z_crit:.3f} × {sigma/np.sqrt(n):.3f} = {z_crit * sigma/np.sqrt(n):.3f}
        """)
        
        # Distribución de la media muestral
        mo.md("### 📊 **Distribución Muestral de la Media**")
        
        fig2 = go.Figure()
        x = np.linspace(mu - 4*sigma/np.sqrt(n), mu + 4*sigma/np.sqrt(n), 200)
        y = norm.pdf(x, mu, sigma/np.sqrt(n))
        
        fig2.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución teórica',
                                  line=dict(color='blue', width=2)))
        fig2.add_trace(go.Histogram(x=sample_means, nbinsx=30, name='Muestras simuladas',
                                    histnorm='probability density', opacity=0.5, marker_color='orange'))
        fig2.add_vline(x=mu, line_dash="dash", line_color="red", line_width=2,
                       annotation_text="μ poblacional")
        
        # Sombrear región de IC
        x_ic = np.linspace(mu - z_crit*sigma/np.sqrt(n), mu + z_crit*sigma/np.sqrt(n), 100)
        y_ic = norm.pdf(x_ic, mu, sigma/np.sqrt(n))
        fig2.add_trace(go.Scatter(x=np.concatenate([x_ic, x_ic[::-1]]), 
                                  y=np.concatenate([y_ic, np.zeros_like(y_ic)]),
                                  fill='toself', fillcolor='rgba(0,100,200,0.2)',
                                  line=dict(color='rgba(255,255,255,0)'),
                                  name=f'IC {conf*100:.0f}%', showlegend=True))
        
        fig2.update_layout(title=f'Distribución muestral de la media (n={n})', 
                           template='plotly_white', height=500)
        
        mo.ui.plotly(fig2)


# =============================================
# TAB 2: VALOR P Y SIGNIFICANCIA
# =============================================
@app.cell
def _(tabs):
    if tabs.value != "pval":
        mo.md("")
    mo.md(r"""
    ## 📈 **Valor p y Significancia Estadística**

    ### 📖 **Definición Formal**
    > **El valor p es la probabilidad de obtener un resultado al menos tan extremo como el observado, asumiendo que la hipótesis nula (H₀) es verdadera.**

    $$p\text{-value} = P(\text{datos} \mid H_0 \text{ es verdadera})$$

    ### 🎯 **Interpretación del Valor p**

    | Valor p | Interpretación | Decisión típica |
    |---------|----------------|-----------------|
    | p < 0.001 | Evidencia **muy fuerte** contra H₀ | Rechazar H₀ |
    | 0.001 ≤ p < 0.01 | Evidencia **fuerte** contra H₀ | Rechazar H₀ |
    | 0.01 ≤ p < 0.05 | Evidencia **moderada** contra H₀ | Rechazar H₀ (α=0.05) |
    | 0.05 ≤ p < 0.10 | Evidencia **débil** contra H₀ | No rechazar H₀ (o marginal) |
    | p ≥ 0.10 | **Poca o ninguna** evidencia contra H₀ | No rechazar H₀ |

    ### ⚠️ **Conceptos Erróneos Comunes**
    | ❌ **INCORRECTO** | ✅ **CORRECTO** |
    |-------------------|-----------------|
    | "p = 0.03 significa 3% de probabilidad que H₀ es verdadera" | "p = 0.03 significa 3% de probabilidad de ver estos datos (o más extremos) SI H₀ es verdadera" |
    | "p < 0.05 prueba que H₁ es verdadera" | "p < 0.05 da evidencia contra H₀, no prueba H₁" |
    | "p = 0.001 es 'más significativo' que p = 0.04" | "Ambos son significativos a α=0.05; p=0.001 es evidencia más fuerte" |
    | "Si p > 0.05, H₀ es verdadera" | "Si p > 0.05, no hay evidencia suficiente para rechazar H₀" |

    ### 📊 **Valor p vs Nivel de Significancia (α)**

    - **α (alfa)**: Umbral predefinido (típicamente 0.05, 0.01, 0.10)
    - **Decisión**: Rechazar H₀ si p ≤ α; No rechazar H₀ si p > α
    - **α = P(Error Tipo I)** = Probabilidad de rechazar H₀ siendo verdadera
    """)
    
    # UI Interactiva
    mo.md("### 🎛️ **Visualizador Interactivo de Valor p**")
    
    col1, col2, col3 = mo.ui.columns([1, 1, 1])
    with col1:
        test_type = mo.ui.dropdown(
            options=["Z-test (media, σ conocida)", "t-test (media, σ desconocida)", 
                     "Prueba de proporción", "Chi-cuadrado (varianza)"],
            value="t-test (media, σ desconocida)", label="Tipo de prueba")
    with col2:
        alpha_p = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α (nivel de significancia)")
    with col3:
        alternative = mo.ui.dropdown(
            options=["bilateral (≠)", "unilateral derecho (>)", "unilateral izquierdo (<)"],
            value="bilateral (≠)", label="Hipótesis alternativa")
    
    return test_type, alpha_p, alternative


@app.cell
def _(test_type, alpha_p, alternative, mo):
    if test_type is None or test_type.value is None:
        mo.md("")
    test = test_type.value
    alpha = alpha_p.value
    alt = alternative.value
    
    mo.md("### 🎛️ **Parámetros de la Muestra**")
    
    if "media" in test:
        col1, col2, col3, col4 = mo.ui.columns([1, 1, 1, 1])
        with col1:
            sample_mean = mo.ui.number(-100, 200, value=52, label="Media muestral (x̄)")
        with col2:
            hyp_mean = mo.ui.number(-100, 200, value=50, label="Media hipotética (μ₀)")
        with col3:
            if "σ conocida" in test:
                sample_std = mo.ui.number(0.1, 100, value=10, label="σ poblacional")
            else:
                sample_std = mo.ui.number(0.1, 100, value=10, label="Desv. estándar muestral (s)")
        with col4:
            sample_n = mo.ui.slider(2, 500, value=25, label="Tamaño muestra (n)")
    else:
        col1, col2, col3 = mo.ui.columns([1, 1, 1])
        with col1:
            sample_mean = mo.ui.number(0, 1, value=0.55, step=0.01, label="Proporción muestral (p̂)")
        with col2:
            hyp_mean = mo.ui.number(0, 1, value=0.5, step=0.01, label="Proporción hipotética (p₀)")
        with col3:
            sample_n = mo.ui.slider(10, 1000, value=100, label="Tamaño muestra (n)")
        sample_std = mo.ui.number(0.1, 100, value=1, label="No usado")
    
    return sample_mean, hyp_mean, sample_std, sample_n


@app.cell
def _(sample_mean, hyp_mean, sample_std, sample_n, test_type, alpha_p, alternative, mo, np, pd, plt, sns, go, px, make_subplots, stats, norm, t, chi2, f, binom, poisson, nct, rnd, warnings):
    if sample_mean is None or sample_mean.value is None:
        mo.md("")
    else:
        x_bar = sample_mean.value
        mu_0 = hyp_mean.value
        s = sample_std.value
        n = sample_n.value
        alpha = alpha_p.value
        alt = alternative.value
        test = test_type.value
        
        # Calcular estadístico de prueba y p-valor
        if "Z-test" in test or "proporción" in test:
            if "proporción" in test:
                se = np.sqrt(mu_0 * (1 - mu_0) / n)
                z_stat = (x_bar - mu_0) / se
                if "bilateral" in alt:
                    p_val = 2 * (1 - norm.cdf(abs(z_stat)))
                elif "derecho" in alt:
                    p_val = 1 - norm.cdf(z_stat)
                else:
                    p_val = norm.cdf(z_stat)
                stat_name, stat_val = "Z", z_stat
                crit = norm.ppf(1 - alpha/2) if "bilateral" in alt else norm.ppf(1 - alpha)
            else:
                se = s / np.sqrt(n)
                z_stat = (x_bar - mu_0) / se
                if "bilateral" in alt:
                    p_val = 2 * (1 - norm.cdf(abs(z_stat)))
                elif "derecho" in alt:
                    p_val = 1 - norm.cdf(z_stat)
                else:
                    p_val = norm.cdf(z_stat)
                stat_name, stat_val = "Z", z_stat
                crit = norm.ppf(1 - alpha/2) if "bilateral" in alt else norm.ppf(1 - alpha)
        elif "t-test" in test:
            se = s / np.sqrt(n)
            t_stat = (x_bar - mu_0) / se
            df = n - 1
            if "bilateral" in alt:
                p_val = 2 * (1 - t.cdf(abs(t_stat), df))
            elif "derecho" in alt:
                p_val = 1 - t.cdf(t_stat, df)
            else:
                p_val = t.cdf(t_stat, df)
            stat_name, stat_val = "t", t_stat
            crit = t.ppf(1 - alpha/2, df) if "bilateral" in alt else t.ppf(1 - alpha, df)
        else:  # chi-cuadrado
            chi2_stat = (n - 1) * s**2 / mu_0**2
            df = n - 1
            if "bilateral" in alt:
                p_val = 2 * min(chi2.cdf(chi2_stat, df), 1 - chi2.cdf(chi2_stat, df))
            elif "derecho" in alt:
                p_val = 1 - chi2.cdf(chi2_stat, df)
            else:
                p_val = chi2.cdf(chi2_stat, df)
            stat_name, stat_val = "χ²", chi2_stat
            crit = chi2.ppf(1 - alpha/2, df) if "bilateral" in alt else chi2.ppf(1 - alpha, df)
        
        # Decisión
        decision = "✅ **RECHAZAR H₀**" if p_val <= alpha else "❌ **NO RECHAZAR H₀**"
        evidence = ("Muy fuerte" if p_val < 0.001 else 
                    "Fuerte" if p_val < 0.01 else 
                    "Moderada" if p_val < 0.05 else 
                    "Débil" if p_val < 0.10 else "Nula")
        
        mo.md(f"""
        ### 📊 **Resultados de la Prueba**
        
        | Estadístico | Valor |
        |-------------|-------|
        | **Estadístico de prueba ({stat_name})** | {stat_val:.4f} |
        | **Valor p** | **{p_val:.6f}** |
        | **Nivel α** | {alpha} |
        | **Valor crítico** | ±{crit:.4f} |
        | **Decisión (α={alpha})** | {decision} |
        | **Fuerza de evidencia** | {evidence} |
        
        **Hipótesis:**
        - H₀: μ = {mu_0} (o p = {mu_0})
        - H₁: μ {alt.replace('bilateral (≠)', '≠').replace('unilateral derecho (>)', '>').replace('unilateral izquierdo (<)', '<')} {mu_0}
        """)
        
        # Visualización interactiva
        mo.md("### 📊 **Visualización de la Distribución y Valor p**")
        
        if "χ²" in stat_name:
            x_min, x_max = 0, max(crit * 1.5, stat_val * 1.2)
            x = np.linspace(x_min, x_max, 500)
            y = chi2.pdf(x, df)
        else:
            x_min = min(-4, stat_val - 1, -crit - 1) if "bilateral" in alt else min(-4, stat_val - 1)
            x_max = max(4, stat_val + 1, crit + 1) if "bilateral" in alt else max(4, stat_val + 1)
            x = np.linspace(x_min, x_max, 500)
            if "t-" in stat_name:
                y = t.pdf(x, df)
            else:
                y = norm.pdf(x)
        
        fig = go.Figure()
        
        # Curva de distribución
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Distribución {stat_name}',
                                 line=dict(color='blue', width=2), fill='tozeroy', fillcolor='rgba(0,0,255,0.1)'))
        
        # Región crítica / valor p
        if "bilateral" in alt:
            if "χ²" in stat_name:
                x_crit_l = chi2.ppf(alpha/2, df)
                x_crit_u = chi2.ppf(1 - alpha/2, df)
                x_p_l = np.linspace(x_min, x_crit_l, 100)
                x_p_u = np.linspace(x_crit_u, x_max, 100)
                y_p_l = chi2.pdf(x_p_l, df)
                y_p_u = chi2.pdf(x_p_u, df)
                fig.add_trace(go.Scatter(x=np.concatenate([x_p_l, x_p_l[::-1]]), 
                                         y=np.concatenate([y_p_l, np.zeros_like(y_p_l)]),
                                         fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                         line=dict(color='rgba(255,255,255,0)'),
                                         name=f'Región crítica (α={alpha})'))
                fig.add_trace(go.Scatter(x=np.concatenate([x_p_u, x_p_u[::-1]]), 
                                         y=np.concatenate([y_p_u, np.zeros_like(y_p_u)]),
                                         fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                         line=dict(color='rgba(255,255,255,0)'),
                                         showlegend=False))
            else:
                x_crit_l = -crit
                x_crit_u = crit
                x_p_l = np.linspace(x_min, x_crit_l, 100)
                x_p_u = np.linspace(x_crit_u, x_max, 100)
                if "t-" in stat_name:
                    y_p_l = t.pdf(x_p_l, df)
                    y_p_u = t.pdf(x_p_u, df)
                else:
                    y_p_l = norm.pdf(x_p_l)
                    y_p_u = norm.pdf(x_p_u)
                fig.add_trace(go.Scatter(x=np.concatenate([x_p_l, x_p_l[::-1]]), 
                                         y=np.concatenate([y_p_l, np.zeros_like(y_p_l)]),
                                         fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                         line=dict(color='rgba(255,255,255,0)'),
                                         name=f'Región crítica (α={alpha})'))
                fig.add_trace(go.Scatter(x=np.concatenate([x_p_u, x_p_u[::-1]]), 
                                         y=np.concatenate([y_p_u, np.zeros_like(y_p_u)]),
                                         fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                         line=dict(color='rgba(255,255,255,0)'),
                                         showlegend=False))
        elif "derecho" in alt:
            if "χ²" in stat_name:
                x_p = np.linspace(crit, x_max, 100)
                y_p = chi2.pdf(x_p, df)
            else:
                x_p = np.linspace(crit, x_max, 100)
                y_p = t.pdf(x_p, df) if "t-" in stat_name else norm.pdf(x_p)
            fig.add_trace(go.Scatter(x=np.concatenate([x_p, x_p[::-1]]), 
                                     y=np.concatenate([y_p, np.zeros_like(y_p)]),
                                     fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                     line=dict(color='rgba(255,255,255,0)'),
                                     name=f'Región crítica (α={alpha})'))
        else:
            if "χ²" in stat_name:
                x_p = np.linspace(x_min, crit, 100)
                y_p = chi2.pdf(x_p, df)
            else:
                x_p = np.linspace(x_min, crit, 100)
                y_p = t.pdf(x_p, df) if "t-" in stat_name else norm.pdf(x_p)
            fig.add_trace(go.Scatter(x=np.concatenate([x_p, x_p[::-1]]), 
                                     y=np.concatenate([y_p, np.zeros_like(y_p)]),
                                     fill='toself', fillcolor='rgba(255,0,0,0.3)',
                                     line=dict(color='rgba(255,255,255,0)'),
                                     name=f'Región crítica (α={alpha})'))
        
        # Línea del estadístico observado
        fig.add_vline(x=stat_val, line=dict(color='orange', width=3, dash='solid'),
                      annotation_text=f"{stat_name} = {stat_val:.3f}", annotation_position="top")
        
        # Líneas críticas
        if "bilateral" in alt:
            fig.add_vline(x=crit, line=dict(color='red', width=2, dash='dash'),
                          annotation_text=f"±{crit:.3f}", annotation_position="top")
            fig.add_vline(x=-crit, line=dict(color='red', width=2, dash='dash'),
                          annotation_position="top")
        else:
            fig.add_vline(x=crit, line=dict(color='red', width=2, dash='dash'),
                          annotation_text=f"Crítico = {crit:.3f}", annotation_position="top")
        
        fig.update_layout(title=f'Distribución de {stat_name} bajo H₀ - Valor p = {p_val:.6f}',
                          template='plotly_white', height=500, showlegend=True)
        
        mo.ui.plotly(fig)
        
        # Gráfico de valor p vs alpha
        mo.md("### 📈 **Valor p vs Nivel de Significancia**")
        
        alphas = np.linspace(0.001, 0.2, 200)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=alphas, y=[p_val]*len(alphas), mode='lines',
                                  name=f'Valor p = {p_val:.4f}', line=dict(color='orange', width=3)))
        fig2.add_trace(go.Scatter(x=alphas, y=alphas, mode='lines',
                                  name='y = α (diagonal)', line=dict(color='blue', width=2, dash='dash')))
        fig2.add_vline(x=alpha, line=dict(color='red', width=2, dash='dot'),
                       annotation_text=f"α = {alpha}")
        fig2.add_hline(y=p_val, line=dict(color='orange', width=2, dash='dot'))
        
        # Colorear regiones
        fig2.add_trace(go.Scatter(x=np.concatenate([alphas, alphas[::-1]]),
                                  y=np.concatenate([alphas, np.zeros_like(alphas)]),
                                  fill='toself', fillcolor='rgba(255,0,0,0.1)',
                                  line=dict(color='rgba(255,255,255,0)'),
                                  name='Rechazar H₀ (p ≤ α)', showlegend=True))
        
        fig2.update_layout(title='Región de decisión: Rechazar H₀ cuando p ≤ α',
                           xaxis_title='Nivel de significancia (α)', yaxis_title='Valor p',
                           template='plotly_white', height=400)
        
        mo.ui.plotly(fig2)


# =============================================
# TAB 3: TIPOS DE ERROR
# =============================================
@app.cell
def _(tabs):
    if tabs.value != "errores":
        mo.md("")
    mo.md(r"""
    ## ⚠️ **Tipos de Error en Pruebas de Hipótesis**

    ### 📋 **Tabla de Decisiones vs Realidad**

    | | **H₀ Verdadera** | **H₀ Falsa (H₁ Verdadera)** |
    |---|---|---|
    | **Rechazar H₀** | **Error Tipo I (α)** - Falso Positivo | **Decisión Correcta (1-β)** - Poder |
    | **No Rechazar H₀** | **Decisión Correcta (1-α)** - Confianza | **Error Tipo II (β)** - Falso Negativo |

    ### 📐 **Definiciones Formales**

    | Error | Símbolo | Definición | Probabilidad |
    |-------|---------|------------|--------------|
    | **Tipo I** (Falso Positivo) | α | Rechazar H₀ siendo H₀ verdadera | α = P(Rechazar H₀ \| H₀ verdadera) |
    | **Tipo II** (Falso Negativo) | β | No rechazar H₀ siendo H₀ falsa | β = P(No rechazar H₀ \| H₀ falsa) |
    | **Poder Estadístico** | 1-β | Rechazar H₀ siendo H₀ falsa | 1-β = P(Rechazar H₀ \| H₀ falsa) |

    ### ⚖️ **Relación entre α, β y Poder**

    - **α ↓** → **β ↑** → **Poder ↓** (más conservador, menos falsos positivos, más falsos negativos)
    - **α ↑** → **β ↓** → **Poder ↑** (más liberal, más falsos positivos, menos falsos negativos)
    - **n ↑** → **β ↓** → **Poder ↑** (más datos = más poder)
    - **Tamaño del efecto ↑** → **β ↓** → **Poder ↑**

    ### 📊 **Niveles Comunes de α y su Interpretación**
    | α | Contexto típico | Interpretación |
    |---|-----------------|----------------|
    | 0.01 | Ensayos clínicos, seguridad | Muy conservador |
    | 0.05 | Ciencias sociales, biomedicina | Estándar |
    | 0.10 | Estudios exploratorios | Exploratorio |
    """)
    
    # UI Interactiva para Poder Estadístico
    mo.md("### 🎛️ **Calculadora Interactiva de Poder Estadístico**")
    
    col1, col2, col3 = mo.ui.columns([1, 1, 1])
    with col1:
        test_type_power = mo.ui.dropdown(
            options=["Z-test (1 muestra)", "t-test (1 muestra)", "Z-test (2 muestras)", "t-test (2 muestras)"],
            value="t-test (1 muestra)", label="Tipo de prueba")
    with col2:
        alpha_power = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
    with col3:
        alt_power = mo.ui.dropdown(options=["bilateral", "unilateral"], value="bilateral", label="Alternativa")
    
    col4, col5, col6 = mo.ui.columns([1, 1, 1])
    with col4:
        effect_size = mo.ui.slider(0.1, 3.0, value=0.5, step=0.1, label="Tamaño del efecto (d de Cohen)")
    with col5:
        n_power = mo.ui.slider(5, 500, value=30, label="Tamaño de muestra (n)")
    with col6:
        if "2 muestras" in test_type_power.value:
            n2_power = mo.ui.slider(5, 500, value=30, label="n₂")
        else:
            n2_power = mo.ui.text(value="", label="N/A (1 muestra)", disabled=True)
    
    return test_type_power, alpha_power, alt_power, effect_size, n_power, n2_power


@app.cell
def _(test_type_power, alpha_power, alt_power, effect_size, n_power, n2_power, mo, np, pd, plt, sns, go, px, make_subplots, stats, norm, t, chi2, f, binom, poisson, nct, rnd, warnings):
    if test_type_power is None or test_type_power.value is None:
        mo.md("")
    else:
        test = test_type_power.value
        alpha = alpha_power.value
        alt = alt_power.value
        d = effect_size.value
        n1 = n_power.value
        
        # Calcular poder usando aproximación normal o exacta
        if "Z-test" in test:
            if "2 muestras" in test:
                n2 = n2_power.value
                df = n1 + n2 - 2
                se = np.sqrt(1/n1 + 1/n2)
                ncp = d / se
                z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                power = 1 - norm.cdf(z_crit - ncp) + norm.cdf(-z_crit - ncp) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp)
            else:
                se = 1/np.sqrt(n1)
                ncp = d / se
                z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                power = 1 - norm.cdf(z_crit - ncp) + norm.cdf(-z_crit - ncp) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp)
            df_label = "∞ (Normal)"
        else:  # t-test
            if "2 muestras" in test:
                n2 = n2_power.value
                df = n1 + n2 - 2
                ncp = d * np.sqrt(n1 * n2 / (n1 + n2))
            else:
                df = n1 - 1
                ncp = d * np.sqrt(n1)
            
            t_crit = t.ppf(1 - alpha/2, df) if alt == "bilateral" else t.ppf(1 - alpha, df)
            power = 1 - nct.cdf(t_crit, df, ncp) + nct.cdf(-t_crit, df, ncp) if alt == "bilateral" else 1 - nct.cdf(t_crit, df, ncp)
            df_label = f"{df}"
        
        beta = 1 - power
        
        mo.md(f"""
        ### 📊 **Resultados del Análisis de Poder**
        
        | Parámetro | Valor |
        |-----------|-------|
        | **Poder (1-β)** | **{power:.4f} ({power*100:.1f}%)** |
        | **Error Tipo II (β)** | {beta:.4f} ({beta*100:.1f}%) |
        | **Error Tipo I (α)** | {alpha} ({alpha*100:.1f}%) |
        | **Tamaño del efecto (d)** | {d} |
        | **n₁** | {n1} |
        | **n₂** | {n2_power.value if hasattr(n2_power, 'value') else 'N/A'} |
        | **Grados de libertad** | {df_label} |
        | **Parámetro no-centralidad** | {ncp:.3f} |
        | **Valor crítico** | {t_crit if 't_crit' in locals() else z_crit:.3f} |
        """)
        
        # Curva de poder vs tamaño de muestra
        mo.md("### 📈 **Curva de Poder vs Tamaño de Muestra**")
        
        n_range = np.arange(5, 301, 5)
        powers = []
        
        for n in n_range:
            if "Z-test" in test:
                if "2 muestras" in test:
                    se = np.sqrt(1/n + 1/n)
                    ncp_n = d / se
                    z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                    p = 1 - norm.cdf(z_crit - ncp_n) + norm.cdf(-z_crit - ncp_n) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp_n)
                else:
                    se = 1/np.sqrt(n)
                    ncp_n = d / se
                    z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                    p = 1 - norm.cdf(z_crit - ncp_n) + norm.cdf(-z_crit - ncp_n) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp_n)
            else:
                if "2 muestras" in test:
                    df_n = 2*n - 2
                    ncp_n = d * np.sqrt(n/2)
                else:
                    df_n = n - 1
                    ncp_n = d * np.sqrt(n)
                t_crit_n = t.ppf(1 - alpha/2, df_n) if alt == "bilateral" else t.ppf(1 - alpha, df_n)
                p = 1 - nct.cdf(t_crit_n, df_n, ncp_n) + nct.cdf(-t_crit_n, df_n, ncp_n) if alt == "bilateral" else 1 - nct.cdf(t_crit_n, df_n, ncp_n)
            powers.append(p)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=n_range, y=powers, mode='lines', name='Poder',
                                 line=dict(color='blue', width=3)))
        fig.add_hline(y=0.8, line_dash="dash", line_color="green", 
                      annotation_text="Poder = 0.80 (estándar)", annotation_position="right")
        fig.add_hline(y=0.9, line_dash="dash", line_color="darkgreen", 
                      annotation_text="Poder = 0.90 (alto)", annotation_position="right")
        fig.add_vline(x=n1, line_dash="dash", line_color="red",
                      annotation_text=f"n = {n1}", annotation_position="top")
        fig.add_trace(go.Scatter(x=[n1], y=[power], mode='markers', 
                                 marker=dict(size=12, color='red'), name='Actual'))
        
        fig.update_layout(title=f'Curva de Poder - {test} (d={d}, α={alpha}, {alt})',
                          xaxis_title='Tamaño de muestra (n)', yaxis_title='Poder (1-β)',
                          template='plotly_white', height=450)
        
        mo.ui.plotly(fig)
        
        # Curva de poder vs tamaño del efecto
        mo.md("### 📈 **Curva de Poder vs Tamaño del Efecto**")
        
        d_range = np.linspace(0.1, 2.0, 100)
        powers_d = []
        
        for d_val in d_range:
            if "Z-test" in test:
                if "2 muestras" in test:
                    se = np.sqrt(1/n1 + 1/n1)
                    ncp_n = d_val / se
                    z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                    p = 1 - norm.cdf(z_crit - ncp_n) + norm.cdf(-z_crit - ncp_n) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp_n)
                else:
                    se = 1/np.sqrt(n1)
                    ncp_n = d_val / se
                    z_crit = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
                    p = 1 - norm.cdf(z_crit - ncp_n) + norm.cdf(-z_crit - ncp_n) if alt == "bilateral" else 1 - norm.cdf(z_crit - ncp_n)
            else:
                if "2 muestras" in test:
                    df_n = n1 + n1 - 2
                    ncp_n = d_val * np.sqrt(n1/2)
                else:
                    df_n = n1 - 1
                    ncp_n = d_val * np.sqrt(n1)
                t_crit_n = t.ppf(1 - alpha/2, df_n) if alt == "bilateral" else t.ppf(1 - alpha, df_n)
                p = 1 - nct.cdf(t_crit_n, df_n, ncp_n) + nct.cdf(-t_crit_n, df_n, ncp_n) if alt == "bilateral" else 1 - nct.cdf(t_crit_n, df_n, ncp_n)
            powers_d.append(p)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=d_range, y=powers_d, mode='lines', name='Poder',
                                  line=dict(color='purple', width=3)))
        fig2.add_vline(x=d, line_dash="dash", line_color="red",
                       annotation_text=f"d = {d}", annotation_position="top")
        fig2.add_hline(y=0.8, line_dash="dash", line_color="green",
                       annotation_text="Poder = 0.80", annotation_position="right")
        fig2.add_trace(go.Scatter(x=[d], y=[power], mode='markers',
                                  marker=dict(size=12, color='red'), name='Actual'))
        
        fig2.update_layout(title=f'Poder vs Tamaño del Efecto (n={n1}, α={alpha}, {alt})',
                           xaxis_title="Tamaño del efecto (d de Cohen)", yaxis_title="Poder (1-β)",
                           template='plotly_white', height=450)
        
        mo.ui.plotly(fig2)
        
        # Visualización de distribuciones H₀ vs H₁
        mo.md("### 📊 **Distribuciones bajo H₀ y H₁ (Visualización del Poder)**")
        
        if "Z-test" in test:
            x = np.linspace(-4, 4 + ncp, 500)
            y0 = norm.pdf(x)
            y1 = norm.pdf(x, ncp, 1)
            crit_val = norm.ppf(1 - alpha/2) if alt == "bilateral" else norm.ppf(1 - alpha)
        else:
            x = np.linspace(-4, 4 + ncp, 500)
            y0 = t.pdf(x, df)
            y1 = nct.pdf(x, df, ncp)
            crit_val = t.ppf(1 - alpha/2, df) if alt == "bilateral" else t.ppf(1 - alpha, df)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x, y=y0, mode='lines', name='H₀ (nula)', 
                                  line=dict(color='blue', width=2), fill='tozeroy', fillcolor='rgba(0,0,255,0.1)'))
        fig3.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='H₁ (alternativa)', 
                                  line=dict(color='orange', width=2), fill='tozeroy', fillcolor='rgba(255,165,0,0.1)'))
        
        # Región de rechazo
        if alt == "bilateral":
            x_rej_l = np.linspace(x.min(), -crit_val, 100)
            x_rej_u = np.linspace(crit_val, x.max(), 100)
            y_rej_l = t.pdf(x_rej_l, df) if "t-" in test else norm.pdf(x_rej_l)
            y_rej_u = t.pdf(x_rej_u, df) if "t-" in test else norm.pdf(x_rej_u)
            fig3.add_trace(go.Scatter(x=np.concatenate([x_rej_l, x_rej_l[::-1]]),
                                      y=np.concatenate([y_rej_l, np.zeros_like(y_rej_l)]),
                                      fill='toself', fillcolor='rgba(255,0,0,0.2)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      name=f'Región de rechazo (α={alpha})'))
            fig3.add_trace(go.Scatter(x=np.concatenate([x_rej_u, x_rej_u[::-1]]),
                                      y=np.concatenate([y_rej_u, np.zeros_like(y_rej_u)]),
                                      fill='toself', fillcolor='rgba(255,0,0,0.2)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      showlegend=False))
        elif alt == "unilateral":
            x_rej = np.linspace(crit_val, x.max(), 100)
            y_rej = t.pdf(x_rej, df) if "t-" in test else norm.pdf(x_rej)
            fig3.add_trace(go.Scatter(x=np.concatenate([x_rej, x_rej[::-1]]),
                                      y=np.concatenate([y_rej, np.zeros_like(y_rej)]),
                                      fill='toself', fillcolor='rgba(255,0,0,0.2)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      name=f'Región de rechazo (α={alpha})'))
        
        # Poder = área bajo H₁ en región de rechazo
        if alt == "bilateral":
            x_pow_l = np.linspace(x.min(), -crit_val, 100)
            x_pow_u = np.linspace(crit_val, x.max(), 100)
            y_pow_l = nct.pdf(x_pow_l, df, ncp) if "t-" in test else norm.pdf(x_pow_l, ncp, 1)
            y_pow_u = nct.pdf(x_pow_u, df, ncp) if "t-" in test else norm.pdf(x_pow_u, ncp, 1)
            fig3.add_trace(go.Scatter(x=np.concatenate([x_pow_l, x_pow_l[::-1]]),
                                      y=np.concatenate([y_pow_l, np.zeros_like(y_pow_l)]),
                                      fill='toself', fillcolor='rgba(0,255,0,0.3)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      name=f'Poder = {power:.3f}'))
            fig3.add_trace(go.Scatter(x=np.concatenate([x_pow_u, x_pow_u[::-1]]),
                                      y=np.concatenate([y_pow_u, np.zeros_like(y_pow_u)]),
                                      fill='toself', fillcolor='rgba(0,255,0,0.3)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      showlegend=False))
        else:
            x_pow = np.linspace(crit_val, x.max(), 100)
            y_pow = nct.pdf(x_pow, df, ncp) if "t-" in test else norm.pdf(x_pow, ncp, 1)
            fig3.add_trace(go.Scatter(x=np.concatenate([x_pow, x_pow[::-1]]),
                                      y=np.concatenate([y_pow, np.zeros_like(y_pow)]),
                                      fill='toself', fillcolor='rgba(0,255,0,0.3)',
                                      line=dict(color='rgba(255,255,255,0)'),
                                      name=f'Poder = {power:.3f}'))
        
        fig3.add_vline(x=crit_val, line=dict(color='red', dash='dash', width=2),
                       annotation_text=f"Crítico = {crit_val:.3f}")
        if alt == "bilateral":
            fig3.add_vline(x=-crit_val, line=dict(color='red', dash='dash', width=2))
        fig3.add_vline(x=ncp, line=dict(color='orange', dash='dot', width=2),
                       annotation_text=f"Centro H₁ = {ncp:.3f}")
        
        fig3.update_layout(title=f'Distribuciones bajo H₀ y H₁ - Área verde = Poder ({power:.3f})',
                           template='plotly_white', height=500)
        
        mo.ui.plotly(fig3)
        
        # Tabla de referencia: tamaños de efecto de Cohen
        mo.md(r"""
        ---
        ### 📏 **Guía de Tamaños de Efecto (d de Cohen)**
        
        | Tamaño | d de Cohen | Interpretación |
        |--------|------------|----------------|
        | **Muy pequeño** | 0.01 | Casi imperceptible |
        | **Pequeño** | 0.20 | Efecto pequeño pero detectable |
        | **Mediano** | 0.50 | Efecto moderado, visible |
        | **Grande** | 0.80 | Efecto grande, obvio |
        | **Muy grande** | 1.20+ | Efecto muy grande |
        | **Enorme** | 2.00+ | Efecto masivo |
        
        ### 🎯 **Reglas Prácticas de Poder**
        - **Poder ≥ 0.80**: Estándar mínimo aceptable
        - **Poder ≥ 0.90**: Recomendado para estudios confirmatorios
        - **Poder < 0.50**: Estudio "subpotente" - alto riesgo de Error Tipo II
        """)


# =============================================
# TAB 4: PRUEBAS ESTADÍSTICAS
# =============================================
@app.cell
def _(tabs):
    if tabs.value != "pruebas":
        mo.md("")
    mo.md(r"""
    ## 🧪 **Pruebas Estadísticas Comunes**

    ### 📋 **Resumen de Pruebas Paramétricas**

    | Prueba | Parámetro | Supuestos | Estadístico | Distribución |
    |--------|-----------|-----------|-------------|--------------|
    | **Z-test (1 muestra)** | Media μ | σ conocida, n≥30 o Normal | $Z = \frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}$ | Normal estándar |
    | **t-test (1 muestra)** | Media μ | σ desconocida, Normal | $t = \frac{\bar{x}-\mu_0}{s/\sqrt{n}}$ | t-Student (n-1 gl) |
    | **t-test (2 muestras ind.)** | μ₁-μ₂ | Independientes, Normal, σ iguales | $t = \frac{\bar{x}_1-\bar{x}_2}{s_p\sqrt{1/n_1+1/n_2}}$ | t-Student (n₁+n₂-2 gl) |
    | **t-test (pareadas)** | μ_d | Diferencias normales | $t = \frac{\bar{d}-\mu_{d0}}{s_d/\sqrt{n}}$ | t-Student (n-1 gl) |
    | **Z-test (proporción)** | Proporción p | n·p≥10, n(1-p)≥10 | $Z = \frac{\hat{p}-p_0}{\sqrt{p_0(1-p_0)/n}}$ | Normal estándar |
    | **Chi-cuadrado (varianza)** | Varianza σ² | Normalidad | $\chi^2 = \frac{(n-1)s^2}{\sigma_0^2}$ | χ² (n-1 gl) |
    | **F-test (varianzas)** | σ₁²/σ₂² | Normalidad, independencia | $F = \frac{s_1^2}{s_2^2}$ | F (n₁-1, n₂-1 gl) |
    | **ANOVA (1 factor)** | Medias k grupos | Normal, homocedasticidad, indep. | $F = \frac{MS_{between}}{MS_{within}}$ | F (k-1, N-k gl) |

    ### 📋 **Pruebas No Paramétricas (Alternativas)**

    | Prueba Paramétrica | Alternativa No Paramétrica | Uso |
    |-------------------|---------------------------|-----|
    | t-test 1 muestra | **Wilcoxon signed-rank** | Mediana ≠ valor |
    | t-test 2 muestras ind. | **Mann-Whitney U** | Distribuciones distintas |
    | t-test pareadas | **Wilcoxon signed-rank** | Diferencias pareadas |
    | ANOVA 1 factor | **Kruskal-Wallis** | k grupos independientes |
    | Correlación Pearson | **Spearman / Kendall** | Asociación monotona |
    | Chi-cuadrado independencia | **Fisher exacto** | Tablas 2×2 pequeñas |

    ### 🔍 **Supuestos Clave y Cómo Verificarlos**
    """)
    
    # Selector de prueba
    test_selector = mo.ui.dropdown(
        options=["t-test 1 muestra", "t-test 2 muestras independientes", "t-test pareadas",
                 "Z-test proporción", "Chi-cuadrado varianza", "F-test varianzas", 
                 "ANOVA 1 factor", "Correlación Pearson"],
        value="t-test 1 muestra", label="Seleccionar prueba")
    
    return test_selector


@app.cell
def _(test_selector, mo):
    if test_selector is None or test_selector.value is None:
        mo.md("")
    else:
        test = test_selector.value
        
        mo.md(f"### 🧪 **{test} - Calculadora Interactiva**")
        
        # Generar UI específica para cada prueba
        if test == "t-test 1 muestra":
            mo.md("#### 📝 **Prueba t de una muestra**\nH₀: μ = μ₀  vs  H₁: μ ≠ μ₀ (o unilateral)")
            col1, col2, col3, col4 = mo.ui.columns([1,1,1,1])
            with col1: x_bar = mo.ui.number(-100, 100, value=52, label="x̄ (media muestral)")
            with col2: mu_0 = mo.ui.number(-100, 100, value=50, label="μ₀ (media hipotética)")
            with col3: s = mo.ui.number(0.1, 100, value=10, label="s (desv. estándar muestral)")
            with col4: n = mo.ui.slider(2, 200, value=25, label="n")
            col5, col6 = mo.ui.columns([1,1])
            with col5: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            with col6: alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return x_bar, mu_0, s, n, alpha, alt, None, None, None, None
        
        elif test == "t-test 2 muestras independientes":
            mo.md("#### 📝 **Prueba t de dos muestras independientes**\nH₀: μ₁ = μ₂  vs  H₁: μ₁ ≠ μ₂")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: x1 = mo.ui.number(-100, 100, value=52, label="x̄₁")
            with col2: x2 = mo.ui.number(-100, 100, value=48, label="x̄₂")
            with col3: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            col4, col5, col6 = mo.ui.columns([1,1,1])
            with col4: s1 = mo.ui.number(0.1, 100, value=10, label="s₁")
            with col5: s2 = mo.ui.number(0.1, 100, value=12, label="s₂")
            with col6: equal_var = mo.ui.checkbox(label="Varianzas iguales (pooled)", value=True)
            col7, col8 = mo.ui.columns([1,1])
            with col7: n1 = mo.ui.slider(2, 200, value=30, label="n₁")
            with col8: n2 = mo.ui.slider(2, 200, value=30, label="n₂")
            alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return x1, x2, s1, s2, n1, n2, alpha, equal_var, alt, None
        
        elif test == "t-test pareadas":
            mo.md("#### 📝 **Prueba t de muestras pareadas**\nH₀: μ_d = 0  vs  H₁: μ_d ≠ 0")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: d_bar = mo.ui.number(-50, 50, value=2.5, label="d̄ (media diferencias)")
            with col2: s_d = mo.ui.number(0.1, 50, value=5, label="s_d (desv. dif.)")
            with col3: n = mo.ui.slider(2, 200, value=20, label="n (pares)")
            col4, col5 = mo.ui.columns([1,1])
            with col4: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            with col5: alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return d_bar, s_d, n, alpha, alt, None, None, None, None, None
        
        elif test == "Z-test proporción":
            mo.md("#### 📝 **Prueba Z de proporción**\nH₀: p = p₀  vs  H₁: p ≠ p₀")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: p_hat = mo.ui.number(0, 1, value=0.55, step=0.01, label="p̂ (proporción muestral)")
            with col2: p_0 = mo.ui.number(0, 1, value=0.5, step=0.01, label="p₀ (proporción hipotética)")
            with col3: n = mo.ui.slider(10, 1000, value=100, label="n")
            col4, col5 = mo.ui.columns([1,1])
            with col4: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            with col5: alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return p_hat, p_0, n, alpha, alt, None, None, None, None, None
        
        elif test == "Chi-cuadrado varianza":
            mo.md("#### 📝 **Prueba Chi-cuadrado para varianza**\nH₀: σ² = σ₀²  vs  H₁: σ² ≠ σ₀²")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: s2 = mo.ui.number(0.1, 500, value=25, label="s² (varianza muestral)")
            with col2: sigma2_0 = mo.ui.number(0.1, 500, value=16, label="σ₀² (varianza hipotética)")
            with col3: n = mo.ui.slider(2, 200, value=25, label="n")
            col4, col5 = mo.ui.columns([1,1])
            with col4: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            with col5: alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return s2, sigma2_0, n, alpha, alt, None, None, None, None, None
        
        elif test == "F-test varianzas":
            mo.md("#### 📝 **Prueba F para igualdad de varianzas**\nH₀: σ₁² = σ₂²  vs  H₁: σ₁² ≠ σ₂²")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: s1_2 = mo.ui.number(0.1, 500, value=25, label="s₁²")
            with col2: s2_2 = mo.ui.number(0.1, 500, value=16, label="s₂²")
            with col3: alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            col4, col5 = mo.ui.columns([1,1])
            with col4: n1 = mo.ui.slider(2, 200, value=30, label="n₁")
            with col5: n2 = mo.ui.slider(2, 200, value=30, label="n₂")
            alt = mo.ui.dropdown(["≠ (bilateral)", "> (unilateral der)", "< (unilateral izq)"], value="≠ (bilateral)", label="H₁")
            
            return s1_2, s2_2, n1, n2, alpha, alt, None, None, None, None
        
        elif test == "ANOVA 1 factor":
            mo.md("#### 📝 **ANOVA de un factor**\nH₀: μ₁ = μ₂ = ... = μₖ  vs  H₁: al menos una media difiere")
            k = mo.ui.slider(2, 6, value=3, label="Número de grupos (k)")
            mo.md("Ingrese datos para cada grupo (medias, desv. estándar, tamaños):")
            
            groups_data = []
            for i in range(k.value):
                col1, col2, col3 = mo.ui.columns([1,1,1])
                with col1: mean_g = mo.ui.number(-100, 100, value=50+i*3, label=f"Grupo {i+1} - Media")
                with col2: std_g = mo.ui.number(0.1, 50, value=10, label=f"Grupo {i+1} - Desv. std")
                with col3: n_g = mo.ui.slider(2, 100, value=20, label=f"Grupo {i+1} - n")
                groups_data.append((mean_g, std_g, n_g))
            
            alpha = mo.ui.slider(0.01, 0.10, value=0.05, step=0.01, label="α")
            
            return groups_data, alpha, k, None, None, None, None, None, None, None
        
        elif test == "Correlación Pearson":
            mo.md("#### 📝 **Correlación de Pearson**\nH₀: ρ = 0  vs  H₁: ρ ≠ 0")
            col1, col2, col3 = mo.ui.columns([1,1,1])
            with col1: r = mo.ui.number(-1, 1, value=0.5, step=0.01, label="r (correlación muestral)")