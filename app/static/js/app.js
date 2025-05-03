
async function fetchWeather(city) {
    try {
        const formData = new FormData();
        formData.append("city", city);

        const response = await fetch("/weather", {
            method: "POST",
            body: formData
        });

        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
    } catch (error) {
        console.error("Error fetching weather:", error);
        alert("Failed to fetch weather data. Please try again.");
    }
}