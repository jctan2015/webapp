document.getElementById("greetBtn").addEventListener("click", async function () {
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
    }
});
