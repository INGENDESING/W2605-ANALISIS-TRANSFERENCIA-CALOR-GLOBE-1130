"""
Backend Flask — Motor de cálculos de ingeniería química
API REST que expone cálculos como endpoints JSON
"""
from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy.optimize import fsolve

app = Flask(__name__)


# ─── Motor de cálculos ────────────────────────────────────────────────────────

def reynolds(rho, v, D, mu):
    """Re = ρ·v·D / μ"""
    return (rho * v * D) / mu


def lmtd(T_hot_in, T_hot_out, T_cold_in, T_cold_out):
    """Diferencia de temperatura media logarítmica [K]"""
    dT1 = T_hot_in - T_cold_out
    dT2 = T_hot_out - T_cold_in
    if dT1 == dT2:
        return dT1
    return (dT1 - dT2) / np.log(dT1 / dT2)


def colebrook(Re, epsilon_D):
    """Factor de fricción de Darcy-Weisbach (Colebrook-White)"""
    def eq(f):
        return (1 / np.sqrt(f[0]) +
                2 * np.log10(epsilon_D / 3.7 + 2.51 / (Re * np.sqrt(f[0]))))
    f0 = [0.02]
    sol = fsolve(eq, f0, full_output=True)
    return float(sol[0][0])


# ─── Endpoints API ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reynolds", methods=["POST"])
def api_reynolds():
    data = request.get_json()
    try:
        Re = reynolds(
            rho=float(data["rho"]),
            v=float(data["v"]),
            D=float(data["D"]),
            mu=float(data["mu"])
        )
        regimen = "turbulento" if Re > 4000 else "laminar" if Re < 2100 else "transición"
        return jsonify({"Re": round(Re, 2), "regimen": regimen})
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/lmtd", methods=["POST"])
def api_lmtd():
    data = request.get_json()
    try:
        DT = lmtd(
            T_hot_in=float(data["T_hot_in"]),
            T_hot_out=float(data["T_hot_out"]),
            T_cold_in=float(data["T_cold_in"]),
            T_cold_out=float(data["T_cold_out"])
        )
        return jsonify({"LMTD_K": round(DT, 4)})
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/friction", methods=["POST"])
def api_friction():
    data = request.get_json()
    try:
        f = colebrook(
            Re=float(data["Re"]),
            epsilon_D=float(data["epsilon_D"])
        )
        return jsonify({"f_darcy": round(f, 6)})
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
