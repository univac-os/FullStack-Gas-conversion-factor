function getConversionFactors() {
    const fuel = document.getElementById("fuel").value;
    const gas = document.getElementById("gas").value;
    const liter = parseFloat(document.getElementById("liter").value);

    const url = gas && liter ? `http://127.0.0.1:5000/get_conversion_factors?fuel=${fuel}&gas=${gas}&liter=${liter}` :
                      `http://127.0.0.1:5000/get_conversion_factors_fuel_only?fuel=${fuel}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "";

            if (data.error) {
                resultDiv.textContent = data.error;
            } else {
                resultDiv.innerHTML = `<h2>Conversion Factors for Fuel: ${data.fuel}</h2>`;
                resultDiv.innerHTML += "<ul>";
                for (const [unit, factor] of Object.entries(data.conversion_factors)) {
                    resultDiv.innerHTML += `<li>${unit}: ${factor}</li>`;
                }
                resultDiv.innerHTML += "</ul>";
            }
        })
        .catch(error => {
            const resultDiv = document.getElementById("result");
            resultDiv.textContent = "An error occurred while fetching data.";
        });
}
