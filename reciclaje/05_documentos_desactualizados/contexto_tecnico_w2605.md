# Contexto Técnico — Proyecto W2605
## Datos oficiales para W2605PRINF001 e W2605PRINF002

**Fecha:** 13 de junio de 2026  
**Empresa:** DMV SAS  
**Cliente:** Ingredion S.A.  
**Tag:** 53A-90A-0056  
**Ubicación:** Planta Ingredion, Cali, Colombia

---

## 1. Ciclo operativo oficial

| Parámetro | Valor |
|---|---|
| Descargas por día | 5 |
| Capacidad del carrotanque | 24 ton |
| Producción diaria | 120 ton/día |
| Duración de cada descarga | 2 h |
| Flujo de descarga | 12 ton/h |
| Intervalo entre inicios de descarga | 4,8 h |
| Tiempo de calentamiento entre descargas | 2,8 h |
| Flujo medio de glucosa | 5.000 kg/h |
| Temperatura de suministro de glucosa al tanque | 55–60 °C |
| Temperatura objetivo de despacho | 57–60 °C |

El tiempo no utilizado en descarga se destina a **calentamiento continuo**. No existe tiempo muerto.

---

## 2. Sistema de calentamiento

| Parámetro | Valor |
|---|---|
| Tipo de chaqueta | Media caña rectangular en espiral |
| Área de transferencia de calor | 13 m² |
| Perfil interno | 141 mm × 45,5 mm |
| Espesor de lámmina | 4,5 mm |
| Material | SS316L |
| Configuración hidráulica | Doble entrada de agua caliente (45 % zona central, 55 % zona periférica); salida común de agua fría al 45 % del área |
| Temperatura del agua (caso base) | 65 °C |
| Temperatura del agua (caso optimizado) | 75 °C |
| Caudal de agua (caso base) | 30,9 m³/h |
| Caudal de agua (caso optimizado) | 57,7 m³/h (v = 2,5 m/s) |

---

## 3. Geometría del tanque (contexto térmico)

| Parámetro | Valor |
|---|---|
| Diámetro interior | 5.264 m |
| Altura del cilindro | 9.670 m |
| Capacidad total (100 %) | 222,8 m³ |
| Material | SS316L |
| Espesor del fondo | 9 mm |
| Espesor del cuerpo cilíndrico | 6 mm |

**Nota:** se elimina el análisis estructural. La geometría se usa únicamente como contexto del sistema de calentamiento.

---

## 4. Propiedades termofísicas de la glucosa Globe 42 DE

| Propiedad | Valor / correlación |
|---|---|
| Densidad | $\rho_g = 1435{,}4 - 0{,}540 \times T$ [kg/m³] |
| Viscosidad (VFT) | $\mu_g = \exp(-9{,}350 + 1278{,}0/(T+66{,}90))$ [Pa·s] |
| Calor específico | Correlación de Choi & Okos |
| Conductividad térmica | Correlación de Choi & Okos |
| Fracción de sólidos | 49 % (80,6 °Brix) |
| Viscosidad a 25 °C | ~212.000 cP |
| Viscosidad a 57 °C | ~2.600 cP |

---

## 5. Resultados térmicos clave

| Resultado | Valor |
|---|---|
| Coeficiente global $U$ (Escenario 3, 75 °C, 40 °C glucosa) | ~31 W/(m²·°C) |
| Resistencia del lado glucosa | ~98 % del total |
| Calor disponible en chaqueta (Esc. 3) | ~30 MJ/h |
| Pérdidas térmicas sin aislamiento (valor adoptado) | 51,1 MJ/h |
| Pérdidas térmicas con aislamiento de 50,8 mm | ~4,6 MJ/h |
| Reducción de pérdidas con aislamiento | ~91 % |
| Tiempo de calentamiento 25 → 57 °C (75 °C, 13 m²) | ~415 h |
| Tiempo de calentamiento 25 → 57 °C (65 °C, 13 m²) | ~773 h |
| Flujo máximo 54 → 57 °C | 5,1 ton/h |
| Flujo máximo 55 → 57 °C | 7,5 ton/h |

---

## 6. Escenarios de operación

| Escenario | Descripción |
|---|---|
| Escenario 1 | Descarga continua con alimentación simultánea (calentamiento por reemplazo de masa) |
| Escenario 2 | Calentamiento desde 25 °C con agua a 65 °C |
| Escenario 3 | Calentamiento desde 25 °C con agua a 75 °C |
| Escenario 4 | Capacidad operativa diaria: 5 descargas de 24 ton |
| Escenario 5 | Ciclo de 5 descargas con recalentamiento entre descargas |

---

## 7. Recomendaciones ejecutivas

1. Implementar aislamiento térmico de 50,8 mm (2") de lana mineral sobre el fondo y el cuerpo cilíndrico.
2. Operar el sistema de agua caliente a 75 °C para reducir los tiempos de recalentamiento.
3. Mantener el límite de 5 descargas/día con carrotanques de 24 ton.
4. Instrumentar un lazo de control de temperatura del agua de calentamiento para mantener la glucosa de salida entre 57 y 60 °C.
5. Programar el mantenimiento del aislamiento para evitar degradación térmica.

---

## 8. Qué eliminar

- Análisis FEA y resultados estructurales.
- Cálculos de espesores mínimos y vida útil por corrosión.
- Factores de seguridad estructural y restricciones de llenado.
- Cargas de viento, sismo, anclajes y NSR-10.
- Tablas de proyección de corrosión, espesores, zonas críticas FEA.
- Figuras de resultados estructurales.
- Referencias a P2611.
- Referencias a 6, 7 u 8 descargas diarias.
