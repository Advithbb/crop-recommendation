document.getElementById('cropForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const temperature = parseFloat(document.getElementById('temperature').value);
    const humidity = parseFloat(document.getElementById('humidity').value);
    const ph = parseFloat(document.getElementById('ph').value);
    const rainfall = parseFloat(document.getElementById('rainfall').value);

    // Validate the inputs
    if (isNaN(temperature) || temperature < -30 || temperature > 50) {
        alert('Please enter a valid temperature between -30 and 50.');
        return;
    }

    if (isNaN(humidity) || humidity < 0 || humidity > 100) {
        alert('Please enter a valid humidity percentage between 0 and 100.');
        return;
    }

    if (isNaN(ph) || ph < 0 || ph > 14) {
        alert('Please enter a valid pH level between 0 and 14.');
        return;
    }

    if (isNaN(rainfall) || rainfall < 0 || rainfall > 1000) {
        alert('Please enter a valid rainfall amount between 0 and 1000 mm.');
        return;
    }

    // Proceed with form submission if inputs are valid
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temperature: temperature,
            humidity: humidity,
            ph: ph,
            rainfall: rainfall
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').textContent = 'Error: ' + data.error;
        } else {
            document.getElementById('result').textContent = 'Recommended Crop: ' + data.crop;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Error: ' + error.message;
    });
});
