// static/js/app.js
async function getWeather() {
    const response = await fetch('http://127.0.0.1:8000/weather/');
    const data = await response.json();
    console.log(data);
}

async function postWeather() {
    const weatherData = {
        temperature: 25.5,
        humidity: 60,
        date: "2025-04-26"
    };
    const response = await fetch('http://127.0.0.1:8000/weather/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(weatherData)
    });
    const result = await response.json();
    console.log(result);
}

getWeather();
