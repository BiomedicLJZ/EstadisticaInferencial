# Política de Seguridad — Estadística Inferencial (marimo)

## Versiones soportadas

| Versión | Soportada |
|---------|-----------|
| main (última) | ✅ Sí |

Este es un proyecto educativo de un solo archivo (`main.py`) sin dependencias de red, sin backend, sin autenticación y sin datos de usuario. No hay versiones LTS ni backports de seguridad.

---

## Reportar una vulnerabilidad

Si descubres un problema de seguridad real (p. ej. ejecución de código arbitrario vía input malicioso en un widget, inyección en f-strings LaTeX, etc.):

1. **NO abras un issue público**.
2. Envía un correo a: **seguridad@tu-dominio.tu** (o abre un *Security Advisory* privado en GitHub: Security → Report a vulnerability).
3. Incluye:
   - Descripción del vector de ataque
   - Pasos para reproducir (mínimos, en `marimo edit main.py`)
   - Impacto estimado
   - Versión de Python / marimo / dependencias

Responderemos en **≤ 7 días** y coordinaremos la corrección y divulgación.

---

## Modelo de amenazas (realista para este proyecto)

| Vector | Riesgo | Mitigación actual |
|--------|--------|-------------------|
| Input en sliders / dropdowns | Bajo: marimo sanitiza widgets; solo números/strings controlados | Validación de rangos en sliders (`min`, `max`, `step`) |
| f-strings LaTeX con valores de usuario | Bajo: valores son `float`/`int` formateados con `:.2f`/`:.3f` | No `eval`/`exec`; solo formateo numérico |
| `np.random.default_rng(seed)` con seed de usuario | Bajo: seed es `int(0..40)`; determinista | Rango acotado en slider |
| Dependencias (numpy, scipy, matplotlib, marimo, statsmodels) | Medio: supply chain | `uv lock` / `pip-audit` periódico; versiones fijadas en `pyproject.toml` |
| Export HTML estático (`marimo export html`) | Bajo: HTML estático sin JS dinámico usuario | Sin ejecución de código usuario en export |

**No hay**: autenticación, base de datos, API, webhooks, secrets, cookies, CORS, CSP, rate-limiting, file upload, subprocess, `eval`, `exec`, `pickle`, `yaml.load(unsafe)`.

---

## Divulgación responsable

- Coordinaremos un fix en `main` y publicaremos un *Security Advisory* en GitHub.
- No hay CVE reservado para proyectos educativos de un solo archivo sin superficie de ataque remota.
- Agradecemos el reporte responsable y acreditamos al reportero (si lo desea) en el advisory.

---

## Contacto de seguridad

**seguridad@tu-dominio.tu** — o usa *Security Advisories* en la pestaña Security del repo.

---

*Política minimalista acorde al alcance del proyecto: un cuaderno marimo educativo sin superficie de ataque real.*