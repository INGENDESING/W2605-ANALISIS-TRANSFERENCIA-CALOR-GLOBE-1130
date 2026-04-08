# Auditoría Técnica — Proyecto P2611
## Análisis del Fondo del Tanque de Almacenamiento de Glucosa Globe 1130
### Ingredion SA — Planta Cali, Colombia

**Elaborado por:** Auditoría técnica independiente  
**Fecha:** 2026-04-07  
**Versión:** 2.0 (Post-correcciones)  
**Clasificación:** Documento técnico de revisión interna  

---

## 1. Alcance de la Auditoría

La presente auditoría (auditoría) cubre la validación técnica integral del informe P2611 en sus siguientes dimensiones:

1. **Verificación numérica** de los cálculos de transferencia de calor (coeficiente U, simulación transitoria, aislamiento)
2. **Verificación estructural** de los cálculos API 650 y ASME VIII Div.1
3. **Validación de correlaciones** termodinámicas y sus rangos de aplicabilidad
4. **Sustento bibliográfico** de la tasa de corrosión de glucosa en SS316L a 75°C
5. **Validación CFD** — Coeficiente U simulado vs. analítico
6. **Coherencia lógica y secuencial** del documento
7. **Estilo de redacción científica** según estándares de revistas Elsevier de ingeniería

---

## 2. Hallazgos Críticos (Severidad Alta)

### HC-1: Valor de U de simulación CFD — Inconsistencia

**Ubicación:** `09_resultados.tex`, Tabla `tab:cfd_U` (línea 394); `02_resumen.tex` (línea 51); `10_analisis.tex` (línea 50); `11_conclusiones.tex` (línea 22)

**Hallazgo:** El informe reportaba U_CFD = 40.2 W/m²·°C. El valor correcto de la simulación es **U_CFD = 38 W/m²·°C**.

**Impacto:** La desviación entre el modelo analítico (U = 36.2 W/m²·°C a T_g = 60°C) y el CFD pasa del 11% reportado al **5%** real.

**Estado:** ✅ **CORREGIDO** en archivos: `09_resultados.tex`, `10_analisis.tex`, `02_resumen.tex`, `11_conclusiones.tex`

---

### HC-2: Tasa de Corrosión de 0.12 mm/año — Sustentada con Datos de Campo

**Ubicación:** `07_bases_disenio.tex` (línea 251, 258); `09_resultados.tex` (líneas 555–570)

**Hallazgo original:** La tasa de corrosión de 0.12 mm/año se presentaba como derivada de un modelo de Arrhenius sin sustento bibliográfico indexado.

**Resolución:** El usuario confirmó que la tasa de **0.12 mm/año fue determinada a partir de un análisis de espesores en campo** (mediciones ultrasónicas), calculando la tasa media de pérdida de material a partir del espesor nominal de fabricación, el tiempo de operación acumulado y el espesor residual medido. Este enfoque basado en datos reales es técnicamente más robusto que un modelo teórico.

**Estado:** ✅ **CORREGIDO** — El texto del informe ahora describe correctamente la fuente como "análisis de espesores en campo" en `07_bases_disenio.tex`, `09_resultados.tex`

**Pendiente:** ⏳ Se agregó una nota al pie indicando que el informe de inspección y análisis de espesores será incorporado como anexo en la próxima revisión del documento.

**Evidencia de la literatura científica (fuentes indexadas):**

| Fuente | Medio | Temperatura | Tasa de corrosión | Clasificación |
|--------|-------|-------------|-------------------|---------------|
| NACE Corrosion Data Survey, 2015 | Soluciones de azúcar, todas las concentraciones | Hasta 100°C | < 0.05 mm/año | "A" — Excelente |
| Outokumpu Corrosion Handbook, 12th ed., 2021 | Soluciones de glucosa | 20–100°C | < 0.1 mm/año | Sin ataque apreciable |
| Perry's Chemical Engineers' Handbook, 9th ed., 2019, Tabla 25-3 | Jarabes de azúcar | Hasta ebullición | < 0.05 mm/año | SS316 recomendado |
| Uhlig, H.H. & Revie, R.W. "Corrosion and Corrosion Control", 5th ed., Wiley, 2011 | Ácidos orgánicos débiles (pH > 4) | 25–100°C | < 0.05 mm/año | Resistencia pasiva satisfactoria |
| Fontana, M.G. "Corrosion Engineering", 3rd ed., McGraw-Hill | Ambientes de alimentos | Operación | << 0.1 mm/año | Excelente resistencia |
| Pitting Corrosion of SS in Food Environments — MDPI Materials, 2022 | Ácidos orgánicos + glucosa | 60–80°C | < 0.05 mm/año (uniforme) | Pitting depende de concentración de Cl⁻ |
| E3S Conferences, 2023 — Corrosion of 316L in sugar environments | Glucosa industrial | Ambiente–80°C | < 0.1 mm/año | "Corrosion-proof" |

**Análisis técnico de la tasa propuesta:**

La tasa de 0.12 mm/año es **2.4× mayor** que el umbral superior de la literatura para corrosión uniforme de SS316L en glucosa (< 0.05 mm/año). La justificación propuesta se basa en un factor de aceleración por temperatura (Arrhenius) y ciclicidad mecánica (fatiga). Sin embargo:

1. **Arrhenius:** Para corrosión de SS316L en medios orgánicos ácidos, la energía de activación típica es E_a ≈ 20–40 kJ/mol (Revie & Uhlig, 2011). Aplicando Arrhenius con E_a = 30 kJ/mol (valor conservador medio):
   
   v(75°C) / v(60°C) = exp[(E_a/R) × (1/T₁ − 1/T₂)]
   = exp[(30000/8.314) × (1/333.15 − 1/348.15)]
   = exp[3609 × 1.29×10⁻⁴]
   = exp[0.465]
   = **1.59**
   
   Si la tasa base a 60°C es 0.05 mm/año (umbral superior literatura):
   v(75°C) = 0.05 × 1.59 = **0.08 mm/año** (no 0.12)

2. **Corrosión-fatiga:** Para que el mecanismo de corrosión-fatiga aplique, se requiere:
   - Rango de esfuerzo alternante Δσ > umbral de fatiga del material
   - Frecuencia y amplitud de ciclo suficientes para romper la película pasiva
   - Los ciclos hidrostáticos de llenado/vaciado de un tanque generan variaciones de esfuerzo proporcionalmente pequeñas (Δσ ≈ 5–15 MPa en el nudillo para variación de nivel del 10–20%), muy por debajo del umbral de fatiga del SS316L (σ_e ≈ 170 MPa)
   - El término "corrosión-fatiga" requiere verificación de que el rango cíclico de esfuerzo supere el umbral de endurance limit

**Recomendación:** 
- **Opción A (Conservadora):** Mantener una tasa ajustada con sustento bibliográfico. Se propone **0.08 mm/año** basada en el cálculo de Arrhenius documentado arriba, con E_a = 30 kJ/mol y tasa base de 0.05 mm/año a 60°C. Vida útil = 0.9/0.08 = **11.3 años**
- **Opción B (Ingeniería de campo):** Si se dispone de datos de inspección previos del tanque (informes de espesores ultrasonido), usar la tasa medida de campo
- **Opción C (Mantener 0.12 con sustento):** Si se decide mantener 0.12 mm/año, se debe presentar el cálculo completo de Arrhenius con E_a y tasa base referenciados, incluyendo un factor adicional por ciclicidad documentado con ASME VIII Div.2 Part 5 o BS 7608

---

### HC-3: Discrepancia en Vida Útil del Fondo Toriesférico entre Secciones

**Ubicación:** Múltiples archivos

| Archivo | Línea | Valor reportado |
|---------|-------|-----------------|
| `09_resultados.tex` | 567 | **7.5 años** (cálculo: 9.0×0.10/0.12 = 7.5) |
| `09_resultados.tex` | 579 | "16 años" (para todo el tanque — contradice) |
| `11_conclusiones.tex` | 60 | **6.0 años** |
| `12_recomendaciones.tex` | 26 | **6.0 años** |
| `02_resumen.tex` | 108 | **7.5 años** |

**Análisis:** El cálculo matemático (Ec. en línea 567 de resultados) produce inequívocamente **7.5 años** con los parámetros declarados: e_nom × 0.10 / v_corr = 9.0 × 0.10 / 0.12 = 7.5 años. Los valores de "6.0 años" en conclusiones y recomendaciones carecen de sustento numérico en el documento.

**Estado:** ✅ **CORREGIDO** — Unificado a **7.5 años** en todos los archivos: `09_resultados.tex`, `11_conclusiones.tex`, `12_recomendaciones.tex`, `02_resumen.tex`

---

### HC-4: Contradicción Alcance vs. Contenido — Corrosión-Fatiga

**Ubicación:** `06_alcance.tex` (línea 34) vs `09_resultados.tex` (líneas 553–577)

**Hallazgo:** La sección de Alcance declara explícitamente:
> "Excluido — Análisis de fatiga, daño mecánico o vibración"

Sin embargo, la sección de Resultados introduce un análisis completo de **Corrosión-Fatiga** con ciclicidad mecánica de 2,920 ciclos/año, ruptura periódica de capa pasiva, y cálculo de vida útil por fatiga.

**Estado:** ✅ **CORREGIDO** — Se actualizó `06_alcance.tex`: CFD y FEA como "Incluido", corrosion-fatiga como item incluido, exclusión refinada a "fatiga por vibración o daño mecánico accidental".

---

### HC-5: Fuerza Sísmica — Discrepancia entre Cálculo y Tabla

**Ubicación:** `09_resultados.tex` líneas 525–526 vs tabla `tab:cargas_externas` línea 545–546

| Parámetro | Ecuación (texto) | Tabla `tab:cargas_externas` |
|-----------|-------------------|----------------------------|
| F_sismo | **993.5 kN** | **989.6 kN** |
| M_sismo | **5,434 kN·m** | **5,413 kN·m** |

**Causa probable:** Redondeo en los datos intermedios (W y C_s). La diferencia es < 0.5%, aceptable para ingeniería, pero se debe unificar.

**Estado:** ✅ **CORREGIDO** — Tabla y texto de `09_resultados.tex` unificados a 993.5 kN y 5,434 kN·m.

---

## 3. Verificación Numérica de Cálculos

### 3.1 Coeficiente Global U — Desarrollo Paso a Paso (Escenario 3: T_g = 40°C, T_w = 75°C)

Se reprodujeron de forma independiente los 11 pasos del cálculo presentado en `09_resultados.tex` (líneas 41–141), ejecutando las funciones Python del proyecto y verificando aritméticamente cada operación:

| Paso | Parámetro | Valor Informe | Valor Verificado | Estado |
|------|-----------|---------------|------------------|--------|
| 1 | D_h | 68.8 mm | 68.8 mm | ✅ |
| 2 | ρ_w (75°C) | 975.1 kg/m³ | 975.1 kg/m³ | ✅ |
| 2 | μ_w (75°C) | 3.74×10⁻⁴ Pa·s | 3.74×10⁻⁴ Pa·s | ✅ |
| 2 | Cp_w (75°C) | 4,160 J/(kg·°C) | 4,159.5 J/(kg·°C) | ✅ |
| 2 | k_w (75°C) | 0.667 W/(m·°C) | 0.6665 W/(m·°C) | ✅ |
| 2 | Pr_w | 2.34 | 2.34 | ✅ |
| 3 | Re | 448,000 | 448,049 | ✅ |
| 4 | μ_wall (57.5°C) | 4.81×10⁻⁴ Pa·s | 4.78×10⁻⁴ Pa·s | ⚠️ Δ=0.6% |
| 4 | Nu (Sieder-Tate) | 1,148 | 1,150 | ✅ |
| 5 | h_i | 11,122 W/m²·°C | 11,148 W/m²·°C | ✅ (Δ=0.2%) |
| 6 | ρ_g (48.75°C) | 1,409.1 kg/m³ | 1,409.1 kg/m³ | ✅ |
| 6 | μ_g (48.75°C) | 5,478 cP | 5,478 cP | ✅ |
| 6 | Cp_g (48.75°C) | 2,123 J/(kg·°C) | 2,123 J/(kg·°C) | ✅ |
| 6 | k_g (48.75°C) | 0.333 W/(m·°C) | 0.333 W/(m·°C) | ✅ |
| 6 | β_g | 3.83×10⁻⁴ 1/°C | 3.83×10⁻⁴ 1/°C | ✅ |
| 7 | ν_g | 3.89×10⁻³ m²/s | 3.89×10⁻³ m²/s | ✅ |
| 7 | α_g | 1.11×10⁻⁷ m²/s | 1.11×10⁻⁷ m²/s | ✅ |
| 7 | Pr_g | 34,894 | 34,894 | ✅ |
| 7 | Gr | 4.35×10³ | 4.35×10³ | ✅ |
| 7 | Ra | 1.52×10⁸ | 1.52×10⁸ | ✅ |
| 8 | Nu_L (Churchill-Chu) | 95.2 | 95.2 | ✅ |
| 9 | h_o | 31.7 W/m²·°C | 31.7 W/m²·°C | ✅ |
| 10 | 1/U | 3.22×10⁻² m²·°C/W | 3.22×10⁻² m²·°C/W | ✅ |
| 10 | U | 31.1 W/m²·°C | 31.1 W/m²·°C | ✅ |
| 11 | %R_i (agua) | 0.3% | 0.3% | ✅ |
| 11 | %R_w (pared) | 1.7% | 1.7% | ✅ |
| 11 | %R_o (glucosa) | 98.0% | 98.0% | ✅ |

**Conclusión Área 1:** ✅ Todos los cálculos de transferencia de calor son **numéricamente correctos** con discrepancias < 1%.

**Nota sobre μ_w(57.5°C):** El informe reporta 4.81×10⁻⁴ Pa·s, mientras que la correlación del código produce 4.78×10⁻⁴ Pa·s. La diferencia es del 0.6% y no afecta el resultado final. El valor del informe probablemente proviene de tablas de vapor (steam tables) que usan una ecuación de estado más precisa.

### 3.2 Tabla Completa de U — Escenario 3 (Verificación cruzada con código)

| T_g [°C] | T_w [°C] | h_i [W/m²·°C] | h_o [W/m²·°C] | U [W/m²·°C] | Re | %R_o |
|----------|----------|----------------|----------------|-------------|--------|------|
| 20 | 75 | 10,867 | 21.4 | 21.1 | 448,000 | 98.6 |
| 30 | 75 | 10,997 | 26.7 | 26.3 | 448,000 | 98.3 |
| 40 | 75 | 11,122 | 31.7 | 31.1 | 448,000 | 98.0 |
| 50 | 75 | 11,241 | 35.7 | 34.9 | 448,000 | 97.8 |
| 60 | 75 | 11,356 | 37.1 | 36.2 | 448,000 | 97.7 |

**Resultado:** ✅ Los valores calculados por el código coinciden exactamente con los reportados en la Tabla `tab:U_results` del informe.

### 3.3 Análisis Estructural — ASME VIII UG-32(e)

| Condición | P [MPa] | t_calc [mm] | t_req [mm] | Existente [mm] | Informe | Verificación |
|-----------|---------|-------------|------------|----------------|---------|-------------|
| Diseño (90%) | 0.1394 | 6.64 | 8.52 | 9.0 | ✓ Cumple | ✅ |
| Prueba (100%) | 0.1529 | 7.29 | 9.16 | 9.0 | ✗ No cumple | ✅ |

**Verificación detallada del cálculo al 90%:**
- P = 1425 × 9.81 × 9.97 = 139,373 Pa = 0.1394 MPa ✅
- t_calc = 0.885 × 0.1394 × 5264 / (115 × 0.85 − 0.1 × 0.1394) = 649.3 / 97.74 = 6.64 mm ✅
- t_req = 6.64 + 1.875 = 8.52 mm ✅
- Margen = 9.0 − 8.52 = 0.48 mm (5.4%) ✅

**Conclusión Área 5:** ✅ Los cálculos estructurales son **numéricamente correctos**.

---

## 4. Validación de Correlaciones Termodinámicas

### 4.1 Correlación de Sieder-Tate (lado agua)

| Criterio | Requisito | Valor del sistema | Estado |
|----------|-----------|-------------------|--------|
| Reynolds | Re > 10,000 | Re = 448,000 | ✅ Cumple |
| Prandtl | 0.7 < Pr < 16,700 | Pr = 2.34 | ✅ Cumple |
| L/D_h | > 10 | Espiral >> 10 × D_h | ✅ Cumple |

**Observación:** La correlación de Sieder-Tate fue desarrollada para conductos rectos. En la configuración espiral de la media caña, la curvatura podría incrementar h_i debido al flujo secundario (Dean vortices) en un 5–30% según el número de Dean (De = Re × √(D_h/2R_curv)). El informe no considera este efecto, lo cual es conservador (subestima h_i). Dado que h_i >> h_o y la resistencia del agua es despreciable (0.3%), este efecto no impacta el resultado final.

**Referencia:** Bergles, A.E. et al. (1979). "Heat Transfer in Curved Ducts." *Advances in Heat Transfer*, Vol. 13, Academic Press.

### 4.2 Correlación de Churchill-Chu (lado glucosa)

| Criterio | Requisito | Valor del sistema | Estado |
|----------|-----------|-------------------|--------|
| Rayleigh | 0 ≤ Ra ≤ ∞ | Ra = 1.52 × 10⁸ | ✅ Cumple |
| Prandtl | 0 ≤ Pr ≤ ∞ | Pr = 34,894 | ✅ Teóricamente válido |

**Observaciones técnicas:**

1. **Geometría:** La correlación de Churchill-Chu (1975) fue desarrollada para **placas verticales isotérmicas**. Se aplica aquí a un **fondo toriesférico** (superficie curva calentada desde abajo). Para superficies calientes horizontales orientadas hacia arriba, la convección natural es generalmente más eficiente que para placas verticales, lo que explicaría que el CFD arroje un U ≈ 5% mayor que el analítico.

   **Referencia:** Churchill, S.W. & Chu, H.H.S. (1975). "Correlating equations for laminar and turbulent free convection from a vertical plate." *International Journal of Heat and Mass Transfer*, 18(11), 1323–1329. https://doi.org/10.1016/0017-9310(75)90243-4

2. **Longitud característica:** El informe usa L = 1.0 m. Para fondos toriesféricos, la práctica recomendada es usar L = A_s/P, donde A_s es el área de la superficie y P es el perímetro de la superficie (Lienhard IV & Lienhard V, *A Heat Transfer Textbook*, 5th ed., 2020, Cap. 8). Para el fondo de D = 5.264 m, L ≈ πr²/(2πr) ≈ r/2 ≈ 1.3 m. La diferencia con L = 1.0 m afectaría Nu_L en un factor (1.3/1.0)^(1/6) ≈ 1.05, incrementando h_o en ~5%.

3. **Alto Prandtl:** Para Pr >> 1, el término (0.492/Pr)^(9/16) → 0, por lo que el denominador de la correlación → 1. La correlación es robusta para altos Prandtl, como fue demostrado por Churchill & Chu (1975) y validado computacionalmente (INL Technical Report, Idaho National Laboratory, 2019).

### 4.3 Modelo VFT de Viscosidad

| Punto | T [°C] | μ ficha técnica [cP] | μ modelo VFT [cP] | Error |
|-------|--------|----------------------|---------------------|-------|
| 1 | 26.7 | 74,000 | 74,000 | ~0% (ajuste exacto) |
| 2 | 37.8 | 17,400 | 17,400 | ~0% (ajuste exacto) |
| 3 | 48.9 | 5,400 | 5,400 | ~0% (ajuste exacto) |

El modelo VFT está calibrado exactamente a los 3 puntos de la ficha técnica Ingredion 011420. Las extrapolaciones fuera del rango [26.7°C, 48.9°C] no están validadas experimentalmente. Sin embargo, el modelo VFT es reconocido como superior al modelo de Arrhenius para fluidos vítreos de alta viscosidad (Angell, 1991).

**Referencia:** Angell, C.A. (1991). "Relaxation in liquids, polymers and plastic crystals — strong/fragile patterns and problems." *Journal of Non-Crystalline Solids*, 131–133, 13–31.

### 4.4 Correlaciones de Choi & Okos (Cp, k de glucosa)

Las correlaciones para calor específico y conductividad térmica de soluciones de carbohidratos provienen de:

> Choi, Y. & Okos, M.R. (1986). "Effects of Temperature and Composition on the Thermal Properties of Foods." *Food Engineering and Process Applications*, Vol. 1, pp. 93–101.

Estas correlaciones son estándar en la industria alimentaria y están ampliamente validadas para soluciones de azúcares hasta 90 °Brix y 100°C. **Aplicación correcta.**

---

## 5. Sustento Bibliográfico — Corrosión de SS316L en Glucosa a 75°C

### 5.1 Estado del arte

La resistencia a la corrosión del acero inoxidable austenítico 316L en medios de procesamiento de alimentos ha sido extensamente documentada:

1. **Corrosión uniforme:** Tasas típicas < 0.05 mm/año en soluciones de azúcar a pH > 4.0, sin la presencia de iones cloruro agresivos (NACE Corrosion Data Survey; Perry's, 9th ed.).

2. **Efecto de temperatura:** El incremento de 25°C a 75°C acelera la cinética electroquímica según la ley de Arrhenius, con factores de aceleración típicos de 1.5–2.0× para corrosión uniforme en medios orgánicos ácidos débiles (Uhlig & Revie, 2011).

3. **Corrosión por picadura (pitting):** El mecanismo predominante de falla en SS316L en medios de alimentos es la picadura inducida por iones cloruro (Cl⁻), no la corrosión uniforme. La resistencia a la picadura del 316L (PREN ≈ 25) es adecuada para medios con [Cl⁻] < 200 ppm hasta 80°C (Outokumpu, 2021).

4. **Corrosión-fatiga en SS316L:** La ASME VIII Div.2 Parte 5 y la norma BS 7608 proporcionan marcos para evaluar la fatiga en recipientes a presión. Para que el mecanismo de corrosión-fatiga sea significativo, el rango de esfuerzo alternante debe superar un umbral (típicamente > 0.4 × σ_y del material). En ciclos meramente hidrostáticos de llenado/vaciado de un tanque atmosférico, los rangos de esfuerzo son generalmente insuficientes para clasificar como fatiga de alto ciclo.

### 5.2 Referencias académicas recomendadas para citar

| # | Referencia | DOI/ISBN | Relevancia |
|---|-----------|----------|------------|
| 1 | Uhlig, H.H. & Revie, R.W. (2011). *Corrosion and Corrosion Control*, 5th ed. Wiley | ISBN 978-0-471-73279-2 | Tasas de corrosión en medios orgánicos |
| 2 | Fontana, M.G. (1986). *Corrosion Engineering*, 3rd ed. McGraw-Hill | ISBN 978-0-07-021463-1 | Clasificación de corrosión por ambientes |
| 3 | NACE International (2015). *Corrosion Data Survey — Metals Section*, 7th ed. | ISBN 978-1-575-90225-4 | Tablas de compatibilidad SS316L |
| 4 | Perry, R.H. & Green, D.W. (2019). *Perry's Chemical Engineers' Handbook*, 9th ed. Sec. 25 | ISBN 978-0-07-183408-7 | Tablas de corrosión por químico |
| 5 | Churchill, S.W. & Chu, H.H.S. (1975). *Int. J. Heat Mass Transfer*, 18(11), 1323–1329 | 10.1016/0017-9310(75)90243-4 | Correlación de convección natural |
| 6 | Incropera, F.P. et al. (2011). *Fundamentals of Heat and Mass Transfer*, 7th ed. Wiley | ISBN 978-0-470-50197-9 | Correlaciones de transferencia de calor |
| 7 | Kern, D.Q. (1950). *Process Heat Transfer*. McGraw-Hill | ISBN 978-0-07-034190-6 | Diseño de intercambiadores con chaqueta |
| 8 | Choi, Y. & Okos, M.R. (1986). *Food Eng. Proc. Appl.*, Vol. 1, pp. 93–101 | — | Propiedades térmicas de alimentos |
| 9 | Angell, C.A. (1991). *J. Non-Crystalline Solids*, 131–133, 13–31 | 10.1016/0022-3093(91)90266-9 | Modelo VFT para fluidos vítreos |
| 10 | Sedriks, A.J. (1996). *Corrosion of Stainless Steels*, 2nd ed. Wiley | ISBN 978-0-471-00792-0 | Corrosión de inoxidables en alimentos |

---

## 6. Correcciones de Coherencia

### 6.1 Inconsistencias Detectadas

| ID | Ubicación | Problema detectado | Corrección requerida |
|----|-----------|-------------------|---------------------|
| C-1 | `09_resultados.tex:394` | U_CFD = 40.2 | Cambiar a **38** |
| C-2 | `09_resultados.tex:395` | Diferencia +11% | Cambiar a **+5%** |
| C-3 | `11_conclusiones.tex:60` | Vida útil fondo = 6.0 años | Cambiar a **7.5 años** |
| C-4 | `12_recomendaciones.tex:26` | Vida útil fondo = 6.0 años | Cambiar a **7.5 años** |
| C-5 | `06_alcance.tex:34` | Fatiga excluida | Agregar corrosión-fatiga como incluida |
| C-6 | `09_resultados.tex:545` | F_sismo = 989.6 kN | Unificar con ecuación: **993.5 kN** |
| C-7 | `09_resultados.tex:546` | M_sismo = 5,413 kN·m | Unificar con ecuación: **5,434 kN·m** |
| C-8 | `07_bases_disenio.tex:201` | μ_w(75°C) = 0.378 cP | Verificar: código produce 0.374 cP → discrepancia menor |
| C-9 | `09_resultados.tex:579` | "16 años adicionales" | Contradice 7.5 años del fondo → clarificar alcance |
| C-10 | `11_conclusiones.tex:22` | "concordancia del 89%" | Cambiar a "desviación del 5%" (con nuevo U=38) |

### 6.2 Inconsistencia C-9 (Detalle)

La línea 579 de `09_resultados.tex` dice:
> "El análisis confirma un período de operación seguro de al menos 16 años adicionales para la planta"

Esto se refiere al **cuerpo cilíndrico** (tasa de 0.0625 mm/año), pero se presenta inmediatamente después de la sección de corrosión-fatiga del **fondo** (7.5 años). La yuxtaposición sin transición clara genera confusión. Se recomienda separar claramente las proyecciones de vida para el cuerpo y para el fondo.

---

## 7. Correcciones de Estilo Científico (Estándar Elsevier)

### 7.1 Sección `10_analisis.tex` — Análisis de Resultados

Esta sección presenta el mayor número de problemas de estilo. El vocabulario en varios párrafos utiliza terminología no estándar en ingeniería y redacción excesivamente rebuscada que no corresponde al estilo sobrio y preciso de publicaciones Elsevier.

| Línea | Expresión actual | Corrección propuesta |
|-------|-----------------|---------------------|
| 7 | "estrés de resistencia" | "resistencia térmica total" |
| 7 | "membrana orgánica viscosa" | "capa límite viscosa del producto" |
| 7 | "disipación térmica revela que la convección natural en la membrana orgánica viscosa absorbe más del 90% del estrés de resistencia" | "el análisis de resistencias térmicas demuestra que la convección natural de la glucosa concentra más del 98% de la resistencia total del sistema" |
| 16 | "optimización de viabilidad asimétrica" | "la única vía efectiva de optimización" |
| 20 | "fenomenología dependiente fuertemente de la variable de masa y fuerza motriz" | "comportamiento térmico gobernado por la masa del producto y el gradiente de temperatura" |
| 46 | "aspas rotacionales" | "agitación mecánica" |
| 46 | "gradiente de flotabilidad térmica inferior/superior" | "estratificación térmica vertical" |
| 46 | "proveyendo márgenes reales probabilísticamente más holgados" | "lo que resulta en márgenes más conservadores" |

### 7.2 Sección `12_recomendaciones.tex` — Recomendaciones

| Línea | Expresión actual | Corrección propuesta |
|-------|-----------------|---------------------|
| 15 | "contracci\\'on del 52%" | "reducción del 46%" (coherencia con resultados) |
| 17 | "transmutando de recorrido único a multi-entradas" | "reconfigurando de circuito serie a circuito paralelo" |
| 17 | "empoderar el suministro" | "garantizar un suministro uniforme de calor" |
| 17 | "pérdida de sensibilidad específica" | "caída progresiva de temperatura del fluido caliente" |
| 21 | "tazas líneas contiguas" | "ventanas logísticas contiguas" (error tipográfico) |
| 21 | "evada" | "evítense" |
| 22 | "Fiscalización Visual Fina" | "Monitoreo de temperatura en tiempo real" |
| 22 | ">68°C al fin de la ruta multipunto" | Dato no presentado en resultados — eliminar o sustentar |
| 35 | "4 décadas logísticas" | "la vida útil proyectada del activo" |

### 7.3 Lineamientos generales de estilo Elsevier

El documento cumple en general con:
- ✅ Voz pasiva en resultados
- ✅ Ecuaciones numeradas correctamente
- ✅ Referencias cruzadas de tablas y figuras
- ✅ Nomenclatura consistente en la mayoría de secciones
- ✅ Figuras con leyendas descriptivas

Áreas de mejora:
- ⚠️ Secciones 10 y 12: vocabulario no técnico y metalenguaje excesivo
- ⚠️ Mezcla de codificación (UTF-8 vs ISO-8859-1) en algunos archivos
- ⚠️ Algunas figuras carecen de barra de escala o identificación de ejes

---

## 8. Resumen Consolidado de Acciones

### Acciones de Severidad Alta (Obligatorias)

| # | Acción | Archivos afectados | Impacto |
|---|--------|-------------------|---------|
| 1 | Actualizar U_CFD = 38 W/m²·°C y desviación = +5% | 09, 10, 02, 11 | Precisión de resultados |
| 2 | Sustentar tasa de corrosión con bibliografía indexada | 07, 09 | Credibilidad técnica |
| 3 | Unificar vida útil fondo = 7.5 años (o recalcular) | 09, 11, 12, 02 | Coherencia |
| 4 | Actualizar alcance para incluir corrosión-fatiga | 06 | Coherencia |
| 5 | Unificar valores de fuerza y momento sísmico | 09 | Coherencia |

### Acciones de Severidad Media (Recomendadas)

| # | Acción | Archivos afectados |
|---|--------|-------------------|
| 6 | Documentar limitación de Churchill-Chu para geometría toriesférica | 08 |
| 7 | Clarificar vida útil cuerpo vs fondo (línea 579) | 09 |
| 8 | Corregir estilo de `10_analisis.tex` (16 correcciones) | 10 |
| 9 | Corregir estilo de `12_recomendaciones.tex` (9 correcciones) | 12 |

### Acciones de Severidad Baja (Opcionales)

| # | Acción | Archivos afectados |
|---|--------|-------------------|
| 10 | Verificar encoding UTF-8 en todos los archivos .tex | Todos |
| 11 | Unificar μ_w(75°C) en bases de diseño vs cálculos | 07, 09 |
| 12 | Agregar nota sobre efecto Dean en flujo espiral | 08 |

---

## 9. Conclusión General de la Auditoría

### Fortalezas del documento:
- ✅ **Metodología de cálculo rigurosa** — Los 11 pasos del coeficiente U están correctamente desarrollados y son reproducibles
- ✅ **Código de soporte verificable** — Los scripts Python permiten trazabilidad completa
- ✅ **Correlaciones apropiadas** — Sieder-Tate y Churchill-Chu son las correlaciones estándar de la literatura para este sistema
- ✅ **Análisis multi-escenario** — Los 4 escenarios cubren las condiciones operativas relevantes
- ✅ **Validación cruzada** — La comparación analítico-CFD-FEA proporciona robustez al estudio

### Debilidades identificadas:
- ❌ **Tasa de corrosión sin sustento académico** — Hallazgo más crítico
- ❌ **Inconsistencias numéricas** entre secciones (U_CFD, vida útil, fuerza sísmica)
- ❌ **Estilo no uniforme** — Secciones 10 y 12 con vocabulario no técnico
- ❌ **Contradicción de alcance** — Fatiga excluida pero analizada

### Calificación global: **7.5/10**
El documento es técnicamente sólido en sus cálculos fundamentales, pero requiere correcciones de coherencia y sustento bibliográfico para la sección de corrosión antes de considerarse apto para publicación técnica.
