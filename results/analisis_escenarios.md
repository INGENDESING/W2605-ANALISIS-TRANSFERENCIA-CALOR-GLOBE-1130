# Analisis de Escenarios - Proyecto W2605
## Sistema de Almacenamiento y Carga de Glucosa

### Condiciones de Operacion Base
- **Flujo de glucosa:** 8,000 kg/h
- **Perdidas termicas del tanque:** 3 C (equivalente a 51,144 kJ/h)
- **Chaqueta de calentamiento:** Area = 14 m2, Agua @ 65 C, 30.9 m3/h
- **Coeficiente global U:** ~30 W/(m2.K)
- **Capacidad de transferencia chaqueta:** ~10,700 kJ/h
- **Temperatura minima para carga:** 57 C

---

## Tabla de Escenarios

| T Entrada (C) | T Salida (C) | Q Perdida (MJ/h) | Q Chaqueta (MJ/h) | Delta vs Min | Estado | Observaciones |
|:-------------:|:------------:|:----------------:|:-----------------:|:------------:|:------:|:--------------|
| 60 | 57.6 | 51.1 | 9.7 | +0.6C | ✓ ACEPTABLE | Cumple minimo |
| 59 | 56.6 | 51.1 | 10.3 | -0.4C | ✗ RECHAZADO | 0.4C bajo minimo |
| 58 | 55.6 | 51.1 | 10.9 | -1.4C | ✗ RECHAZADO | 1.4C bajo minimo |
| 57 | 54.7 | 51.1 | 11.5 | -2.3C | ✗ RECHAZADO | 2.3C bajo minimo |
| 56 | 53.7 | 51.1 | 12.1 | -3.3C | ✗ RECHAZADO | 3.3C bajo minimo |
| 55 | 52.7 | 51.1 | 12.7 | -4.3C | ✗ RECHAZADO | 4.3C bajo minimo |
| 54 | 51.8 | 51.1 | 13.2 | -5.2C | ✗ RECHAZADO | 5.2C bajo minimo |
| 53 | 50.8 | 51.1 | 13.8 | -6.2C | ✗ RECHAZADO | 6.2C bajo minimo |


---

## Analisis de Viabilidad

### Caso Base (Entrada a 57C)

**Balance Energetico:**
```
Glucosa Entrada:  H = 971.7 MJ/h @ 57.0C
Perdidas:        -Q = 51.1 MJ/h (3C)
Chaqueta:        +Q = 11.5 MJ/h (U=30 W/m2K, A=14m2)
--------------------------------------------------------------------------------
Glucosa Salida:  H = 932.1 MJ/h @ 54.7C
```

**Agua de Chaqueta:**
```
Agua Entrada:    H = 8.24 GJ/h @ 65.0C
Transferido:     -Q = 11.5 MJ/h
Agua Salida:     H = 8.22 GJ/h @ 64.9C
```

### Conclusion Critica

**SOLO es viable cargar a carrotanque si la glucosa entra a 60C o superior.**

Con las condiciones actuales:
- Las perdidas termicas (51,144 kJ/h) son ~5x mayores que el aporte de la chaqueta (11506 kJ/h)
- El sistema opera con deficit energetico de ~40,000 kJ/h
- La glucosa sale -2.3C por debajo del minimo requerido

### Recomendaciones para Operar con Entrada a 57C

Para poder cargar glucosa a 57C y mantener la temperatura de salida >=57C, se requiere **AL MENOS UNA** de las siguientes modificaciones:

1. **Aumentar area de chaqueta:**
   - Area requerida: ~65-70 m2 (actual: 14 m2)
   - Incremento: 5x el area actual

2. **Subir temperatura del agua:**
   - Temperatura requerida: ~80C (actual: 65C)
   - Incremento: +15C

3. **Reducir perdidas termicas del tanque:**
   - Mejorar aislamiento o reducir a ~0.5C de perdida
   - Requiere aislamiento adicional o reparacion

4. **Combinacion de medidas:**
   - Agua a 75C + Area 25 m2 + Mejor aislamiento

---

## Propiedades de las Corrientes

### Glucosa Globe 1130 (~80.6 Brix)
| Propiedad | Valor @ 55C | Unidad |
|-----------|-------------|--------|
| Cp | 2.131 | kJ/(kg.C) |
| Densidad | 1405 | kg/m3 |
| Viscosidad | 3500 | cP |
| Conductividad | 0.38 | W/(m.K) |

### Agua de Chaqueta
| Propiedad | Valor @ 65C | Unidad |
|-----------|-------------|--------|
| Cp | 4.184 | kJ/(kg.C) |
| Densidad | 980 | kg/m3 |
| Viscosidad | 0.432 | cP |

---

*Documento generado automaticamente - Proyecto W2605*
*Fecha: 2026-04-10*
