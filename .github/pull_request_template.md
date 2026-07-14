# Pull Request Template

## Descripción del cambio
Breve descripción de qué cambia y por qué.

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad (nueva distribución, prueba, visualización, etc.)
- [ ] Mejora de documentación / README / glosario
- [ ] Refactor / estilo / limpieza
- [ ] Actualización de dependencias

## Sección del notebook afectada
- [ ] Sección 1: Inferencia & TLC
- [ ] Sección 2: Distribuciones
- [ ] Sección 3: Significancia, p, α
- [ ] Sección 4: Pruebas estadísticas (7 simuladores)
- [ ] Sección 5: Regresión (Lineal / Logística)
- [ ] Sección 6: Correlación ≠ Causalidad
- [ ] Glosario / Bibliografía / Cierre
- [ ] Config global / estilo / utilidades

## Cómo probar
1. `uv sync` (o `pip install -e .`)
2. `marimo run main.py` o `marimo edit main.py`
3. Pasos para verificar el cambio:

## Capturas / evidencia visual (si aplica)
Arrastra capturas aquí.

## Checklist
- [ ] El notebook se ejecuta sin errores (`marimo run main.py`)
- [ ] Las fórmulas LaTeX muestran valores actuales (no símbolos abstractos)
- [ ] Los colores respetan la paleta semántica (`C` dict en celda 2)
- [ ] Los sliders/inputs son reactivos (marimo reactivo, sin orden de celdas)
- [ ] Código sigue el estilo del proyecto (matplotlib dark, f-strings LaTeX, simuladores reactivos)
- [ ] Documentación actualizada (README / CONTRIBUTING / glosario si aplica)

## Referencias / Issues relacionados
Closes #<issue-number>