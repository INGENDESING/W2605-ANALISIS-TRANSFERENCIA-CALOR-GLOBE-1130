# Auditoría crítica del informe térmico y de simulación GTTP-1004-DOC-MC-1-1 Rev.5 para el fondo del tanque de glucosa Tag 53A-90A-0056

## Resumen

Este documento presenta una auditoría crítica a nivel de maestría de la memoria de cálculo térmica y de simulación elaborada por un tercero para el fondo toriesférico del tanque de almacenamiento de glucosa Tag 53A-90A-0056 de Ingredion S.A. (informe GTTP-1004-DOC-MC-1-1 Rev.5, fecha 04/06/2026). La revisión contrasta las hipótesis, propiedades termofísicas, metodología de cálculo, resultados y conclusiones del informe con el estudio independiente desarrollado por DMV SAS dentro del proyecto W2605. El análisis identifica diferencias conceptuales y numéricas de magnitud tal que los resultados del informe de tercero no pueden considerarse representativos del comportamiento térmico real del sistema. Los hallazgos más relevantes son la subestimación de dos a tres órdenes de magnitud del coeficiente convectivo del lado de la glucosa, el uso de propiedades termofísicas inconsistentes con la ficha técnica del fabricante, la ausencia de cuantificación de pérdidas térmicas al ambiente y de requerimientos de aislamiento, y una documentación insuficiente de las simulaciones numéricas, que impide reproducir o validar los resultados presentados.

## 1. Objeto y alcance de la auditoría

El informe auditado tiene como propósito demostrar que el serpentín de media caña rectangular instalado en el fondo del tanque nuevo es capaz de mantener 24 m³ de glucosa Globe 1130 a 60 °C durante cinco despachos diarios. Para ello, el tercero presenta un cálculo térmico analítico, una estimación de caída de presión, un dimensionamiento mecánico simplificado de la chaqueta y resultados de simulación por elementos finitos (FEA) y dinámica de fluidos computacional (CFD). La presente auditoría evalúa la solidez técnica de cada uno de estos componentes mediante su comparación con el modelo desarrollado en el proyecto W2605, el cual utiliza correlaciones de transferencia de calor ampliamente aceptadas en ingeniería de proceso, propiedades termofísicas calibradas contra la ficha técnica Ingredion 011420 y una simulación CFD independiente en COMSOL Multiphysics 6.4.

## 2. Datos de entrada y bases de diseño

La Tabla 1 resume los datos de entrada más relevantes reportados por el tercero y los valores adoptados en el proyecto W2605.

**Tabla 1.** Comparación de datos de entrada y bases de diseño.

| Parámetro | Informe de tercero GTTP-1004 Rev.5 | Proyecto W2605 (DMV SAS) | Observación |
|---|---|---|---|
| Producto | Glucosa Globe 1130 | Glucosa Globe 1130 (ficha Ingredion 011420) | Coinciden en la identificaci\'on del producto. |
| Sólidos secos | 80,5–81,6 % | 79,7–81,5 % (nominal 80,6 %) | Coinciden en orden de magnitud. |
| Temperatura objetivo | 60 °C | 57–60 °C (operación oficial 60 °C) | Coinciden en la cota superior. |
| Material del fondo | SS316L, espesor 9 mm | SS316L, espesor 9 mm | Coinciden. |
| Diámetro interior del fondo | 5,263 m | 5,264 m | Coinciden. |
| Área de contacto de la chaqueta | 14,192 m² | 14,0 m² | El tercero reporta un valor ligeramente superior, probablemente por contorno externo del perfil. |
| Perfil de media caña | U150×50×4,5 mm | 141 mm × 45,5 mm × 4,5 mm | Dimensiones funcionales similares; el tercero emplea nomenclatura comercial. |
| Caudal de agua | 20,3 m³/h | 57,7 m³/h (escenarios 2/3, v = 2,5 m/s) | El tercero opera a una velocidad de ~1,0 m/s; W2605 usa 2,5 m/s como diseño. |
| Temperatura del agua | 65 °C | 75 °C (oficial); 65 °C (alternativo) | El tercero no evalúa 75 °C. |
| Ciclo de descarga | 5 cargues/día, 23–24 m³/cargue | 5 descargas/día, 24 ton (≈17 m³) | El tercero asume volumen mayor por descarga. |

La Tabla 1 evidencia que, si bien algunos parámetros geométricos y materiales son coincidentes, existen diferencias importantes en el caudal de agua, la temperatura de servicio y el volumen por descarga. Estas diferencias condicionan de manera directa la capacidad térmica calculada.

## 3. Propiedades termofísicas del fluido almacenado

El informe de tercero reporta las propiedades termofísicas de la glucosa Globe 1130 que se presentan en la Tabla 2.

**Tabla 2.** Propiedades termofísicas de la glucosa según el informe de tercero y el proyecto W2605.

| Propiedad | Informe de tercero (60 °C) | Proyecto W2605 (60 °C) | Desviación relativa |
|---|---|---|---|
| Densidad (kg/m³) | 1430 | 1403 | +1,9 % |
| Calor específico (J/kg·°C) | 837,36 | 2134 | –60,8 % |
| Conductividad térmica (W/m·°C) | 0,50 | 0,344 | +45,3 % |
| Viscosidad dinámica (Pa·s) | 5,0 | 2,06 | +142 % |
| Viscosidad cinemática (m²/s) | 0,0033 | 0,00147 | +124 % |
| Número de Prandtl | 15000 | ~13000 | +15 % |

El calor específico reportado por el tercero (837 J/kg·°C) es anormalmente bajo para un jarabe de glucosa concentrado. Para una solución acuosa con 80,6 % de sólidos, el calor específico esperado se obtiene mediante una regla de mezclas entre el agua y los carbohidratos, lo que arroja valores cercanos a 2100 J/kg·°C, consistentes con la correlación de Choi y Okos empleada en W2605. Un calor específico subestimado en un factor cercano a 2,5 implica que toda la energía requerida para calentar la glucosa está subestimada en el mismo factor, lo que invalida los tiempos de calentamiento y los balances energéticos presentados por el tercero.

La conductividad térmica de 0,50 W/m·°C también es superior a los valores reportados en literatura para jarabes de glucosa a alta concentración, que típicamente se ubican entre 0,30 y 0,38 W/m·°C en el rango de 20–60 °C. La viscosidad de 5 Pa·s (5000 cP) es comparable a la reportada por Ingredion a 48,9 °C (5400 cP), pero no a 60 °C, donde el modelo VFT calibrado a la ficha técnica arroja 2060 cP. El uso de una viscosidad más alta por parte del tercero, paradójicamente, no compensa el error en el calor específico ni en el coeficiente convectivo, dado que el mecanismo limitante del sistema sigue siendo la convección natural del producto.

## 4. Metodología de cálculo térmico

### 4.1 Coeficiente convectivo del lado del agua

El tercero emplea una correlación atribuida a Usman et al. (2019) para el diseño de un intercambiador de calor de serpentín helicoidal en una mini central termoeléctrica. Dicha referencia no es aplicable directamente a una media caña rectangular soldada sobre un fondo toriesférico, porque la geometría del canal, el patrón de flujo y el mecanismo de transferencia de calor difieren sustancialmente de un serpentín helicoidal circular. El proyecto W2605 utiliza en cambio la correlación de Sieder-Tate para flujo turbulento en conductos no circulares con diámetro hidráulico, lo cual es el estándar reconocido para media cañas rectangulares.

Los resultados del lado del agua son, no obstante, del mismo orden de magnitud en ambos estudios. El tercero reporta h_i = 4229 W/m²·°C para una velocidad de 1,5 m/s, mientras que W2605 obtiene h_i ≈ 11000 W/m²·°C para 2,5 m/s. La diferencia se explica principalmente por la velocidad, y ambos valores son consistentes con flujo turbulento de agua en un canal confinado.

### 4.2 Coeficiente convectivo del lado de la glucosa

Este es el punto más crítico de la metodología del tercero. El informe reporta un coeficiente convectivo externo h_o = 3300 W/m²·°C para la glucosa en convección natural. Sin embargo, para un fluido con viscosidad del orden de 10³–10⁴ cP, la convección natural en una superficie calentada desde abajo produce coeficientes típicamente entre 10 y 100 W/m²·°C. El proyecto W2605, empleando la correlación de Churchill-Chu con propiedades evaluadas a la temperatura de película, obtiene h_o entre 18 y 37 W/m²·°C en el rango de 25–60 °C.

La discrepancia de dos órdenes de magnitud en h_o no tiene sustento físico. El tercero calcula un número de Grashof de 8,0 × 10⁹ y un número de Prandtl de 15000, lo que produce un número de Rayleigh de aproximadamente 1,2 × 10¹⁴. Aunque este valor es elevado, la correlación de Churchill-Chu para placas verticales en ese rango de Ra produciría un Nusselt del orden de 100, no de 4000 como implícitamente requiere h_o = 3300 W/m²·°C con k = 0,50 W/m·°C. Además, el tercero clasifica el régimen como laminar (Gr < 10⁹), lo cual contradice su propio cálculo de Gr = 8,0 × 10⁹. Esta inconsistencia conceptual invalida el coeficiente externo adoptado.

### 4.3 Coeficiente global de transferencia de calor

Como consecuencia del error en h_o, el tercero reporta U = 783 W/m²·°C, valor comparable al de intercambiadores de calor de placas con fluidos de baja viscosidad y alta turbulencia. El proyecto W2605 obtiene U entre 21 y 36 W/m²·°C para las mismas condiciones geométricas, con el 97,7–98,8 % de la resistencia térmica concentrada en el lado de la glucosa. La diferencia de aproximadamente 25 veces en U conduce a tiempos de calentamiento y potencias térmicas igualmente irreales.

La Tabla 3 resume la distribución de resistencias térmicas en ambos estudios.

**Tabla 3.** Comparación del coeficiente global y distribución de resistencias.

| Parámetro | Informe de tercero | Proyecto W2605 (T_g = 40 °C, T_w = 75 °C) |
|---|---|---|
| h_i (W/m²·°C) | 4229 | 11122 |
| h_o (W/m²·°C) | 3300 | 31,7 |
| U (W/m²·°C) | 783 | 31,1 |
| R_i / R_total (%) | ~44 | 0,3 |
| R_w / R_total (%) | ~12 | 1,7 |
| R_o / R_total (%) | ~44 | 98,0 |

La distribución de resistencias del tercero asigna contribuciones comparables al agua y a la glucosa, lo cual es incompatible con la física del problema. En un sistema de media caña sin agitación mecánica y con un producto altamente viscoso, la resistencia del lado del producto debe dominar abrumadoramente.

### 4.4 Cálculo de la carga térmica y del tiempo de calentamiento

El tercero presenta dos estimaciones del tiempo necesario para calentar 24 m³ de glucosa desde 40 °C hasta 60 °C. La primera, basada en un balance transitorio con Q = 76,2 kW, arroja 4 h; la segunda, basada en Q = 393 898 Btu/h (115,4 kW) y una carga total de 1 503 295 Btu (1,586 × 10⁹ J), arroja 3,82 h. Ambos valores son inconsistentes con la energía real requerida.

Usando las propiedades correctas del proyecto W2605 (ρ = 1403 kg/m³, Cp = 2134 J/kg·°C) para 24 m³ de glucosa, la energía necesaria para elevar la temperatura 20 °C es:

Q_total = ρ V Cp ΔT = 1403 × 24 × 2134 × 20 = 1,44 × 10⁹ J.

Con una potencia térmica efectiva de 76 kW, el tiempo mínimo teórico sería de aproximadamente 5,3 h, y con 115 kW sería de 3,5 h. Sin embargo, estos cálculos suponen una transferencia instantánea y uniforme, ignorando que la temperatura del agua disminuye a lo largo de la chaqueta y que el coeficiente U varía fuertemente con la temperatura de la glucosa. El proyecto W2605 resuelve numéricamente el balance transitorio y obtiene un tiempo de calentamiento de aproximadamente 110 h para llevar 24 m³ desde 25 °C hasta 60 °C con agua a 65 °C, debido a la dominancia de la resistencia del lado del producto. Aunque el tercero parte de 40 °C, su resultado de 3,82 h permanece inalcanzable con el U real del sistema.

## 5. Caída de presión en la media caña

El tercero reporta una caída de presión de 7350 Pa para una velocidad de 1,0 m/s, longitud de 90 m, diámetro de 0,12 m y factor de fricción f = 0,02. El cálculo es aritméticamente correcto, pero opera con una velocidad significativamente menor que la de diseño del proyecto W2605 (2,5 m/s). Escalando linealmente con el cuadrado de la velocidad, la caída de presión a 2,5 m/s sería aproximadamente 46 kPa, valor que debe considerarse en la selección de la bomba de recirculación. El informe de tercero no evalúa esta condición de diseño, lo cual constituye una omisión relevante para la especificación del equipo auxiliar.

## 6. Análisis estructural y simulación numérica

### 6.1 Dimensionamiento mecánico

El informe de tercero presenta un dimensionamiento simplificado de la carcasa y la chaqueta según ASME VIII División 1, obteniendo espesores mínimos muy pequeños (0,082 in para la carcasa y 0,0025 in para la chaqueta) y una presión permisible de 334 psi para la chaqueta. Si bien los cálculos parecen seguir las fórmulas del código, la presentación mezcla unidades (pulgadas, milímetros, psi, bar) sin conversión explícita, lo que dificulta la verificación. Además, no se presentan cálculos de soldadura, ni de la unión fondo-cilindro, ni de los efectos de la presión interna sobre el fondo toriesférico, aspectos que son críticos en un recipiente de estas dimensiones.

### 6.2 Simulación FEA

El tercero reporta una simulación por elementos finitos de la chaqueta con CalculiX, con desplazamiento máximo de 0,1 mm y esfuerzo máximo de 37 MPa a una presión de diseño de 2 bar. No obstante, el informe no incluye detalles de la malla (más allá de un tamaño mínimo de 1,5 mm), del tipo de elementos, de las condiciones de frontera exactas ni de una validación de independencia de malla. La carcasa se modela con un espesor de 7 mm, cuando el plano indica 9 mm. Estas omisiones impiden reproducir o auditar independientemente los resultados estructurales.

### 6.3 Simulación CFD

La sección de CFD del informe de tercero es especialmente escasa en detalle metodológico. Se mencionan cinco modelos con diferentes temperaturas y coeficientes de convección impuestos en el lado del tanque, arrojando potencias de 312 kW, 88 kW, 234 kW, 38 kW y 11 kW. No se especifica el software utilizado, el modelo de turbulencia, las propiedades constantes o variables, el esquema de discretización, los criterios de convergencia ni la independencia de malla. Los resultados son inconsistentes entre sí: por ejemplo, el Modelo 1 (T = 40 °C) reporta 312 kW, mientras que el Modelo 3 (h = 3000 W/m²·°C, T = 40 °C) reporta 234 kW, a pesar de que el segundo debería transferir más calor al imponer un coeficiente convectivo superior al que surge de la física del problema.

El proyecto W2605 realiza una simulación CFD en COMSOL Multiphysics 6.4 del Escenario 3 (T_g = 25 °C, T_w = 75 °C, v = 2,5 m/s), obteniendo U_CFD = 38 W/m²·°C, valor que concuerda en un 5 % con el modelo analítico (36 W/m²·°C a 60 °C). Esta concordancia valida el modelo de convección natural de Churchill-Chu empleado en W2605 y confirma que el U = 783 W/m²·°C del tercero no es físicamente plausible.

## 7. Pérdidas térmicas al ambiente y aislamiento

El informe de tercero no incluye una estimación de las pérdidas térmicas al ambiente ni un dimensionamiento de aislamiento. Solamente se menciona, de forma incidental, que las pérdidas por radiación y convección no superan los 23 kW, sin indicar el área considerada, la temperatura ambiente, el espesor de aislamiento ni la metodología de cálculo. El proyecto W2605 cuantifica las pérdidas térmicas del tanque completo considerando el área real expuesta al ambiente (149,7 m²), un aislamiento de lana mineral de 50,8 mm y coeficientes convectivos interno y externo coherentes. Los resultados se resumen en la Tabla 4.

**Tabla 4.** Comparación de pérdidas térmicas y aislamiento.

| Condición | Informe de tercero | Proyecto W2605 |
|---|---|---|
| Área expuesta considerada | No especificada | 149,7 m² |
| Espesor de aislamiento | No especificado | 50,8 mm (lana mineral) |
| Pérdidas sin aislamiento a 60 °C | No calculadas | 48,7 kW (175,4 MJ/h) |
| Pérdidas con aislamiento a 60 °C | "No superan 23 kW" | 4,1 kW (14,7 MJ/h) |
| Temperatura superficial exterior | No calculada | 28,3 °C |

La omisión del tercero es relevante porque, en ausencia de aislamiento, las pérdidas térmicas del tanque completo (48,7 kW) son comparables o superiores a la capacidad de calentamiento disponible en algunas condiciones, lo que afectaría la viabilidad operativa del ciclo de cinco descargas diarias.

## 8. Conclusiones del informe de tercero

El informe concluye que el serpentín puede calentar 34320 kg de glucosa con agua a 65 °C y 20,3 m³/h, y que el tiempo de calentamiento de 24 m³ desde 40 °C hasta 60 °C es de aproximadamente 3,82 h. Estas conclusiones descansan sobre un coeficiente global U = 783 W/m²·°C que no es consistente con la física del sistema ni con la simulación CFD independiente realizada en el proyecto W2605 (U_CFD = 38 W/m²·°C). En consecuencia, las conclusiones operativas del tercero son excesivamente optimistas y no deben utilizarse para la toma de decisiones sin una revisión técnica independiente.

Por el contrario, el proyecto W2605 demuestra que el sistema de media caña de 14 m² es técnicamente capaz de sostener cinco descargas diarias de 24 toneladas, pero únicamente si se cumplen simultáneamente las siguientes condiciones: la glucosa de alimentación ingresa al tanque en el rango de 57–60 °C, el agua de calentamiento opera a 75 °C, el tanque cuenta con aislamiento térmico de 50,8 mm de lana mineral, y la operación se basa en el mantenimiento de un inventario caliente, dado que el arranque desde frío del tanque completo requiere tiempos del orden de semanas.

## 9. Hallazgos críticos

La Tabla 5 consolida los hallazgos críticos identificados durante la auditoría.

**Tabla 5.** Hallazgos críticos de la auditoría.

| Hallazgo | Severidad | Descripción técnica | Impacto |
|---|---|---|---|
| Subestimación de h_o | Crítica | El coeficiente convectivo del lado de la glucosa (3300 W/m²·°C) es dos órdenes de magnitud superior al valor físicamente esperado. | Invalida el coeficiente global U y los tiempos de calentamiento del informe de tercero. |
| Propiedades termofísicas inconsistentes | Crítica | El calor específico de 837 J/kg·°C es aproximadamente 2,5 veces menor que el valor esperado para un jarabe de glucosa 80,6 Brix. | Subestima la energía requerida y distorsiona los balances energéticos. |
| Inconsistencia interna en el número de Grashof | Alta | El tercero clasifica el régimen como laminar (Gr < 10⁹) pero reporta Gr = 8,0 × 10⁹. | Pone en duda la aplicación correcta de la correlación de convección natural. |
| Ausencia de cuantificación de pérdidas térmicas | Alta | No se calcula el área expuesta ni el espesor de aislamiento requerido. | Impide evaluar la viabilidad del ciclo diario y la eficiencia energética. |
| Simulaciones numéricas poco documentadas | Alta | FEA y CFD carecen de detalles de malla, convergencia, propiedades y validación. | Los resultados no son reproducibles ni auditables. |
| Conclusiones operativas optimistas | Alta | Se afirma que 24 m³ se calientan en 3,82 h con agua 65 °C, sin considerar la inercia térmica real. | Puede inducir a errores en la planificación operativa y en la especificación de equipos. |

## 10. Fortalezas observadas

A pesar de las deficiencias señaladas, el informe de tercero presenta algunos elementos positivos que deben reconocerse. Incluye un análisis estructural por elementos finitos de la chaqueta, reconoce explícitamente la utilidad de la simulación CFD como herramienta de verificación y consigna de forma clara los datos de entrada proporcionados por el cliente. Además, la estructura general del documento sigue el formato típico de una memoria de cálculo, con secciones de propiedades, cálculo térmico, diseño mecánico y simulación.

## 11. Recomendaciones

La Tabla 6 presenta las recomendaciones derivadas de la auditoría.

**Tabla 6.** Recomendaciones de la auditoría.

| Recomendación | Justificación técnica | Prioridad |
|---|---|---|
| No utilizar los valores de U ni los tiempos de calentamiento del informe de tercero sin revisión independiente. | El coeficiente global y los tiempos descansan sobre h_o físicamente inconsistente. | Alta |
| Reemplazar las propiedades termofísicas por valores calibrados contra la ficha técnica oficial. | El calor específico y la conductividad térmica reportados distorsionan el balance energético. | Alta |
| Rehacer el modelo térmico con correlaciones de convección natural validadas para fluidos de alta viscosidad. | Se requiere h_o en el rango de 10–100 W/m²·°C y verificación del número de Rayleigh. | Alta |
| Cuantificar las pérdidas térmicas al ambiente para el área real expuesta y dimensionar el aislamiento. | Sin este análisis no es posible evaluar la viabilidad del ciclo operativo. | Alta |
| Documentar con detalle las simulaciones FEA y CFD, incluyendo malla, convergencia y validación. | La reproducibilidad y auditabilidad son requisitos mínimos de un informe de ingeniería. | Media |
| Considerar el proyecto W2605 como referencia principal para la operación del tanque. | Sus resultados han sido validados mediante CFD y son consistentes con la física del sistema. | Media |

## 12. Referencias

DMV SAS. Proyecto W2605 — Análisis térmico del fondo del tanque de glucosa Tag 53A-90A-0056. Documentos W2605PRINF001 y W2605PRINF002, junio 2026.

Ingredion. Ficha técnica Globe 1130 Corn Syrup/Glucose 011420, 2017.

Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. Fundamentals of Heat and Mass Transfer, 7th ed. John Wiley & Sons, 2011.

Choi, Y., & Okos, M. R. Effects of Temperature and Composition on the Thermal Properties of Foods. Food Engineering and Process Applications, Vol. 1, 1986, pp. 93–101.

Usman, M. S., et al. Design of Helical Coil Heat Exchanger for a mini powerplant. International Journal of Scientific and Engineering Research, Vol. 10, 2019, pp. 303–313.

Tercero. GTTP-1004-DOC-MC-1-1 Rev.5, Memoria de cálculo tanque - glucosa - Ingredion: Térmica y simulación, 04/06/2026.
