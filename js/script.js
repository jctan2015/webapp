async function loadStats() {
    const res = await fetch("/stats");
    const data = await res.json();
    const tbody = document.getElementById("statsTable").querySelector("tbody");
    tbody.innerHTML = "";
    data.forEach(entry => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${entry.name}</td><td>${entry.count}</td>`;
        tbody.appendChild(row);
    });
}

loadStats();

async function greet() {
    const name = document.getElementById("nameInput").value.trim();
    if (!name) return;

    const response = await fetch("/greet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("greeting").textContent = data.message;
        document.getElementById("counter").textContent = `You have been greeted ${data.count} times.`;
        loadStats();
    }
}

document.getElementById("greetBtn").addEventListener("click", greet);
document.getElementById("nameInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        greet();
    }
});

