/**
 * Motor de cálculos — cliente JavaScript
 * Envía datos al API Flask y muestra resultados
 */

const API = "";  // mismo origen que Flask

async function post(endpoint, body) {
    const res = await fetch(`${API}/api/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    return res.json();
}

function showResult(elementId, data, unit = "") {
    const el = document.getElementById(elementId);
    if (data.error) {
        el.innerHTML = `<span class="error">Error: ${data.error}</span>`;
    } else {
        const entries = Object.entries(data)
            .map(([k, v]) => `<b>${k}</b>: ${v} ${unit}`)
            .join(" &nbsp;|&nbsp; ");
        el.innerHTML = entries;
    }
}

async function calcReynolds() {
    const data = await post("reynolds", {
        rho: document.getElementById("re-rho").value,
        v:   document.getElementById("re-v").value,
        D:   document.getElementById("re-D").value,
        mu:  document.getElementById("re-mu").value,
    });
    showResult("re-result", data);
}

async function calcLMTD() {
    const data = await post("lmtd", {
        T_hot_in:  document.getElementById("lm-Thi").value,
        T_hot_out: document.getElementById("lm-Tho").value,
        T_cold_in: document.getElementById("lm-Tci").value,
        T_cold_out:document.getElementById("lm-Tco").value,
    });
    showResult("lm-result", data, "K");
}

async function calcFriction() {
    const data = await post("friction", {
        Re:       document.getElementById("fr-Re").value,
        epsilon_D:document.getElementById("fr-eD").value,
    });
    showResult("fr-result", data);
}
