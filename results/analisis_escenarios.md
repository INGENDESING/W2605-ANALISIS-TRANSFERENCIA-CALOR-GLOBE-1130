# Analisis de Escenarios - Proyecto W2605
## Sistema de Almacenamiento y Carga de Glucosa

### Condiciones de Operacion Base
- **Flujo de glucosa:** 8,000 kg/h
- **Perdidas termicas del tanque:** 3 C (equivalente a 51,144 kJ/h)
- **Chaqueta de calentamiento:** Area = 13 m2, Agua @ 65 C, 30.9 m3/h
- **Coeficiente global U:** ~30 W/(m2.K)
- **Capacidad de transferencia chaqueta:** ~10,700 kJ/h
- **Temperatura minima para carga:** 57 C

---

## Tabla de Escenarios

| T Entrada (C) | T Salida (C) | Q Perdida (MJ/h) | Q Chaqueta (MJ/h) | Delta vs Min | Estado | Observaciones |
|:-------------:|:------------:|:----------------:|:-----------------:|:------------:|:------:|:--------------|
| 60 | 57.5 | 51.1 | 9.0 | +0.5C | ✓ ACEPTABLE | Cumple minimo |
| 59 | 56.6 | 51.1 | 9.6 | -0.4C | ✗ RECHAZADO | 0.4C bajo minimo |
| 58 | 55.6 | 51.1 | 10.1 | -1.4C | ✗ RECHAZADO | 1.4C bajo minimo |
| 57 | 54.6 | 51.1 | 10.7 | -2.4C | ✗ RECHAZADO | 2.4C bajo minimo |
| 56 | 53.7 | 51.1 | 11.2 | -3.3C | ✗ RECHAZADO | 3.3C bajo minimo |
| 55 | 52.7 | 51.1 | 11.8 | -4.3C | ✗ RECHAZADO | 4.3C bajo minimo |
| 54 | 51.7 | 51.1 | 12.3 | -5.3C | ✗ RECHAZADO | 5.3C bajo minimo |
| 53 | 50.7 | 51.1 | 12.8 | -6.3C | ✗ RECHAZADO | 6.3C bajo minimo |


---

## Analisis de Viabilidad

### Caso Base (Entrada a 57C)

**Balance Energetico:**
```
Glucosa Entrada:  H = 971.7 MJ/h @ 57.0C
Perdidas:        -Q = 51.1 MJ/h (3C)
Chaqueta:        +Q = 10.7 MJ/h (U=30 W/m2K, A=13m2)
--------------------------------------------------------------------------------
Glucosa Salida:  H = 931.3 MJ/h @ 54.6C
```

**Agua de Chaqueta:**
```
Agua Entrada:    H = 8.24 GJ/h @ 65.0C
Transferido:     -Q = 10.7 MJ/h
Agua Salida:     H = 8.22 GJ/h @ 64.9C
```

### Conclusion Critica

**SOLO es viable cargar a carrotanque si la glucosa entra a 60C o superior.**

Con las condiciones actuales:
- Las perdidas termicas (51,144 kJ/h) son ~5x mayores que el aporte de la chaqueta (10684 kJ/h)
- El sistema opera con deficit energetico de ~40,000 kJ/h
- La glucosa sale -2.4C por debajo del minimo requerido

### Recomendaciones para Operar con Entrada a 57C

Para poder cargar glucosa a 57C y mantener la temperatura de salida >=57C, se requiere **AL MENOS UNA** de las siguientes modificaciones:

1. **Aumentar area de chaqueta:**
   - Area requerida: ~65-70 m2 (actual: 13 m2)
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

### Glucosa Globe 42 DE (~80.6 Brix)
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
