

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
