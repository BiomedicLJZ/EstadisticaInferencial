# 📊 Estadística Inferencial — Cuaderno Interactivo (marimo)

Un cuaderno **reactivo** para entender inferencia estadística **tocándola**: mueves un control y las fórmulas, gráficas y decisiones se recalculan al instante. Hecho con **[marimo](https://github.com/marimo-team/marimo)**, NumPy, SciPy y Matplotlib.

> **Pedagogía**: cada tema motiva al siguiente. Fórmulas en LaTeX muestran **tus valores actuales**, no símbolos abstractos. Incluye 🧠 *intuición*, ⚠️ *trampas comunes*, ❓ *preguntas socráticas* y mini-quizzes.

---

## 📋 Tabla de contenidos

| Sección | Tema | Qué verás |
|---------|------|-----------|
| 1 | **Inferencia & TLC** | De la muestra a la población; TL Central en vivo (Uniforme, Exponencial, Binomial sesgada, Normal). |
| 2 | **Distribuciones** | Bernoulli, Binomial, Poisson, Uniforme, Normal — PMF/PDF + CDF con tus parámetros, fórmulas LaTeX vivas. |
| 3 | **Significancia, *p* y α** | Errores Tipo I/II, potencia, curva de poder; valor *p* como área en colas; quiz de interpretación. |
| 4 | **Pruebas estadísticas** | 7 simuladores: Z (media σ conocida), *t* (media), Z (proporción), *t* de Welch (2 medias), χ² bondad de ajuste, χ² independencia 2×2, *F* (varianzas). Fórmulas estilo Excel + decisión automática. |
| 5 | **Regresión** | Lineal (OLS) con residuos + *R²*; Logística (Newton-Raphson/IRLS) con matriz de confusión y *odds ratio*. |
| 6 | **Correlación ≠ Causalidad** | Generador de correlación *r* objetivo; visualización de confundidores. |

---

## 🚀 Instalación y ejecución

```bash
# 1. Clona / entra al directorio
cd estadisticca

# 2. (Recomendado) Entorno virtual con uv
uv sync          # instala deps de pyproject.toml
# o con pip: pip install -e .

# 3. Ejecuta el cuaderno reactivo
marimo run main.py
# o modo edición:
marimo edit main.py
```

**Requisitos**: Python ≥ 3.14, dependencias en `pyproject.toml` (marimo ≥ 0.23, numpy, scipy, matplotlib, statsmodels).

---

## 🎯 Cómo usar el cuaderno

| Acción | Qué pasa |
|--------|----------|
| Mueves un *slider* / *dropdown* | Todo lo que depende de él se recalcula **al instante** (marimo es reactivo, no hay que “correr celdas en orden”). |
| Cambias la semilla | Re-muestreos para ver variabilidad muestral. |
| Lees la fórmula LaTeX | Muestra **tus números actuales** (p. ej. `z = (0.532 - 0.500) / 0.049 = 0.653`). |
| Respondes un quiz | Feedback inmediato ✅/❌ con explicación. |
| Abres un acordeón (🔗 / 📚) | Contenido extra: conexiones entre distribuciones, glosario ES/EN, bibliografía. |

---

## 🧩 Estructura del código (`main.py`)

```text
main.py
├─ Config global (estilo matplotlib, paleta C, helper new_ax)
├─ Sección 1: Inferencia & TLC
│  ├─ Controles: población, n, réplicas, semilla
│  ├─ Gráfico: población + distribución muestral de x̄ + curva Normal teórica
│  ├─ Tabla: teórico vs simulado (media, SE)
│  └─ Quiz: “¿qué hago con n para reducir SE a la mitad?”
├─ Sección 2: Distribuciones
│  ├─ Dropdown: Bernoulli / Binomial / Poisson / Uniforme / Normal
│  ├─ Sliders condicionales por distribución
│  ├─ Gráfico: PMF/PDF + CDF
│  ├─ Fórmulas LaTeX con tus parámetros + tabla media/var/sd
│  └─ Acordeón: conexiones (Bernoulli → Binomial → Poisson → Normal)
├─ Sección 3: Significancia, p, α
│  ├─ Controles: d (efecto), n, α, z_obs
│  ├─ Curvas H₀ vs H₁ con áreas α / β / potencia
│  ├─ Valor p visual + decisión automática
│  ├─ Callout “trampa del p-valor”
│  └─ Quiz interpretación de p=0.03
├─ Sección 4: Pruebas (7 simuladores)
│  ├─ Controles globales: α, tipo de cola (2 colas / > / <)
│  ├─ Cada prueba: sliders específicos → gráfico → fórmula Excel → decisión
│  └─ Tipos: Z-media, t-media, Z-proporción, t-Welch 2-muestras, χ² GOF, χ² 2×2, F-varianzas
├─ Sección 5: Regresión
│  ├─ 5a Lineal: datos sintéticos + OLS closed-form → gráfico + residuos + R²
│  └─ 5b Logística: Newton-Raphson (IRLS) propio → sigmoide + matriz confusión + odds ratio
├─ Sección 6: Correlación ≠ Causalidad
│  ├─ Genera (X,Y) con r objetivo via transformación de Cholesky
│  └─ Visual de confundidor
└─ Cierre: glosario ES/EN, bibliografía, síntesis en 1 frase por tema
```

---

## 🎨 Paleta de colores (consistente en todo el notebook)

```python
C = {
    "primary":  "#2563eb",  # azul principal
    "accent":   "#f59e0b",  # ámbar
    "danger":   "#dc2626",  # rojo (rechazo / α)
    "success":  "#16a34a",  # verde (potencia / H₁)
    "purple":   "#7c3aed",
    "slate":    "#334155",  # H₀ / neutro
    "muted":    "#94a3b8",  # esperado / secundario
}
```

---

## 🧠 Decisiones de diseño (ponytail: lazy pero correcto)

| Decisión | Por qué |
|----------|---------|
| **marimo reactivo** | Elimina “correr celdas en orden”; el estudiante explora causa-efecto moviendo sliders. |
| **Fórmulas LaTeX con f-strings** | El alumno ve *sus* números, no símbolos abstractos. |
| **Simuladores, no solo teoría** | Cada prueba tiene su generador de datos + visual + decisión. |
| **IRLS casero para logística** | Sin dependencia pesada; 15 líneas legibles muestran el algoritmo real. |
| **Estilo matplotlib dark + grid sutil** | Legible en proyector y pantalla; colores semánticos (rojo=α, verde=potencia). |
| **Quizzes socráticos** | Forzan confrontar la intuición errónea (*p* ≠ P(H₀)). |
| **Sin framework de testing** | Es material didáctico; los checks visuales interactivos son el test. |

---

## 📚 Referencias rápidas (glosario incluido en el notebook)

| ES | EN | Símbolo |
|---|---|---|
| Error estándar | Standard error | $SE$ |
| Teorema límite central | Central limit theorem | TLC / CLT |
| Hipótesis nula / alternativa | Null / Alternative hypothesis | $H_0, H_1$ |
| Nivel de significancia | Significance level | $\alpha$ |
| Valor p | p-value | $p$ |
| Potencia | Power | $1-\beta$ |
| Bondad de ajuste | Goodness of fit | $\chi^2$ |
| Mínimos cuadrados | Least squares | OLS |
| Coef. determinación | Coefficient of determination | $R^2$ |
| Razón de momios | Odds ratio | $e^\beta$ |
| Confusor | Confounder | $Z$ |

---

## 📖 Bibliografía sugerida (en el notebook)

- **Wasserman**, *All of Statistics* — referencia compacta y rigurosa.
- **Downey**, *Think Stats* — enfoque computacional (Python), gratuito.
- **Pearl & Mackenzie**, *The Book of Why* — causalidad e inferencia.
- Docs de `scipy.stats` y `marimo` para extender el cuaderno.

---

## 🛠️ Extender / personalizar

| Qué quieres | Dónde tocar |
|-------------|-------------|
| Añadir otra distribución | Sección 2: nuevo `elif` en la celda de gráficos + slider en celda de controles. |
| Nueva prueba estadística | Sección 4: copia el patrón Z-media → cambia estadístico, distribución, g.l. |
| Cambiar paleta | Celda 2: dict `C` (7 colores semánticos). |
| Añadir idioma | Acordeón final: duplica la tabla glosario. |
| Exportar a HTML estático | `marimo export html main.py -o salida.html` (pierde reactividad). |

---

## 📄 Licencia

MIT — úsalo, modifícalo, compártelo. Si lo usas en clase, ¡mencióname o avísame!

---

> **Hecho con ❤️ para que la estadística inferencial se entienda moviendo sliders, no memorizando fórmulas.**