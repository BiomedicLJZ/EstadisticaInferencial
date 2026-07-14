# Guía de Contribución — Estadística Inferencial (marimo)

Gracias por querer contribuir. Este es un **cuaderno pedagógico reactivo** hecho con [marimo](https://github.com/marimo-team/marimo): el código es **reactivo** (sin orden de celdas), las fórmulas LaTeX muestran **valores actuales** y cada simulador es **reactivo + visual + decisión automática**.

---

## 🚀 Puesta en marcha rápida

```bash
cd estadisticca
uv sync          # o: pip install -e .
marimo run main.py   # modo ejecución
marimo edit main.py  # modo edición (recomendado para contribuir)
```

**Requisitos**: Python ≥ 3.14, deps en `pyproject.toml` (marimo ≥ 0.23, numpy, scipy, matplotlib, statsmodels).

---

## 🧭 Cómo contribuir (flujo lazy pero correcto)

1. **Fork** → crea rama (`feature/nueva-distribucion`, `fix/typo-glosario`, etc.)
2. **Edita `main.py`** con `marimo edit main.py` (reactivo: guarda y ves cambios al instante)
3. **Verifica**:
   - `marimo run main.py` ejecuta sin errores
   - Fórmulas LaTeX muestran *tus valores* (f-strings), no símbolos abstractos
   - Sliders/inputs son reactivos (cambias uno → todo lo que depende se recalcula)
   - Colores respetan la paleta semántica `C` (celda 2: `primary`, `danger`, `success`, `accent`, `muted`, `slate`, `purple`)
4. **Commit** con mensaje claro (`feat: add Beta distribution to Section 2`)
5. **PR** → usa la plantilla `.github/pull_request_template.md`

---

## 🎯 Qué aportar (ideas bienvenidas)

| Qué quieres añadir | Dónde tocar en `main.py` |
|--------------------|---------------------------|
| Nueva distribución (Beta, Gamma, t-Student, etc.) | Sección 2: nuevo `elif` en celda de gráficos + slider en celda de controles |
| Nueva prueba estadística | Sección 4: copia el patrón Z-media → cambia estadístico, distribución, g.l. |
| Nueva visualización / quiz / trampa común | Sección correspondiente: copia patrón existente |
| Nuevo idioma en glosario | Acordeón final: duplica tabla ES/EN |
| Nueva paleta de colores | Celda 2: diccionario `C` (7 colores semánticos) |
| Corrección typo / mejora redacción | Busca el `mo.md` correspondiente |
| Exportar a HTML estático | `marimo export html main.py -o salida.html` (pierde reactividad) |

---

## 🧠 Principios de diseño (no los rompas sin razón)

| Principio | Por qué |
|-----------|---------|
| **Reactivo (marimo)** | Elimina "correr celdas en orden"; el alumno explora causa-efecto moviendo sliders. |
| **Fórmulas LaTeX con f-strings** | El alumno ve *sus* números (ej: `z = (0.532 - 0.500) / 0.049 = 0.653`). |
| **Simuladores, no solo teoría** | Cada prueba tiene generador de datos + visual + decisión automática. |
| **IRLS casero para logística** | Sin dependencia pesada; 15 líneas legibles muestran el algoritmo real. |
| **Estilo matplotlib dark + grid sutil** | Legible en proyector y pantalla; colores semánticos (rojo=α, verde=potencia). |
| **Quizzes socráticos** | Forzan confrontar intuición errónea (*p* ≠ P(H₀)). |
| **Sin framework de testing** | Es material didáctico; los checks visuales interactivos son el test. |

---

## 🎨 Estilo de código (ponytail: lazy pero correcto)

- **Sin abstracciones no pedidas**: no interface con una implementación, no factory para un producto.
- **Stdlib primero**: `f-strings`, `dataclasses`, `functools.lru_cache`, `itertools`, `statistics`.
- **Menos archivos posible**: todo en `main.py` (marimo es un solo archivo reactivo).
- **Comentarios `ponytail:`** = atajo deliberado con techo conocido:
  ```python
  # ponytail: global lock, per-account locks if throughput matters
  ```
- **Un check ejecutable**: `marimo run main.py` debe terminar sin errores.

---

## 📝 Convenciones de commit (lazy)

```
feat: add Beta distribution to Section 2
fix: fix Poisson PMF when lambda > 20
docs: fix typo in CLT quiz explanation
style: adjust grid alpha to 0.25
refactor: extract normal_pdf helper (used 3×)
```

---

## 🧪 Checklist antes de PR

- [ ] `marimo run main.py` termina sin errores
- [ ] Fórmulas LaTeX usan f-strings con valores actuales
- [ ] Colores usan `C["primary"]`, `C["danger"]`, etc. (no hex hardcoded)
- [ ] Sliders reactivos: cambiar uno actualiza gráficos/fórmulas/tablas dependientes
- [ ] Código sigue patrones existentes (copia-pega-adapta de secciones similares)
- [ ] README / CONTRIBUTING / glosario actualizados si toca

---

## 📄 Licencia

MIT — úsalo, modifícalo, compártelo. Si lo usas en clase, ¡mencióname o avísame!

---

> **Hecho con ❤️ para que la estadística inferencial se entienda moviendo sliders, no memorizando fórmulas.**