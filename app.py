from flask import Flask, request, jsonify
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load data from "data.csv" file into a dictionary for quick access
emission_factors = {}
with open("data.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fuel = row["Fuel"]
        unit = row["Unit"]
        emission_factors[(fuel, unit)] = {
            "Total": float(row["Total kg CO2e per unit"]),
            "CO2": float(row["kg CO2e of CO2 per unit"]),
            "CH4": float(row["kg CO2e of CH4 per unit"]),
            "N2O": float(row["kg CO2e of N2O per unit"]),
        }

def calculate_conversion_factors(fuel, gas=None, liter=1.0):
    conversion_factors = {}
    if (fuel, "litres") in emission_factors:
        litres_data = emission_factors[(fuel, "litres")]
        for unit in ["kWh (Net CV)", "kWh (Gross CV)"]:
            if (fuel, unit) in emission_factors:
                unit_data = emission_factors[(fuel, unit)]
                if gas and (fuel, unit) in emission_factors:
                    # Calculate the x-percent biodiesel blend based on the provided gas
                    x_percent_biodiesel_blend = (emission_factors[(fuel, unit)][gas] / emission_factors[(fuel, "tonnes")][gas])
                else:
                    # Calculate the x-percent biodiesel blend based on total values
                    x_percent_biodiesel_blend = (emission_factors[(fuel, unit)]["Total"] / emission_factors[(fuel, "tonnes")]["Total"])
                # Calculate the conversion factors for the unit
                conversion_factors[unit] = (x_percent_biodiesel_blend * 0.168) + ((1 - x_percent_biodiesel_blend) * 2.706)
            else:
                conversion_factors[unit] = None
        if gas:
            # Calculate the conversion factor for gas liters
            conversion_factors["litres"] = litres_data[gas] * liter
        else:
            # Calculate the conversion factor for total liters
            conversion_factors["litres"] = litres_data["Total"] * liter
    return conversion_factors

@app.route("/get_conversion_factors", methods=["GET"])
def get_conversion_factors():
    fuel = request.args.get("fuel")
    gas = request.args.get("gas").upper()
    liter = float(request.args.get("liter", 1.0))

    if liter <= 0:
        return jsonify({"error": "Invalid liter value. It must be greater than 0."}), 400

    # Calculate the conversion factors based on the provided information
    conversion_factors = calculate_conversion_factors(fuel, gas, liter)

    if conversion_factors:
        return jsonify({"fuel": fuel, "gas": gas, "liter": liter, "conversion_factors": conversion_factors})
    else:
        return jsonify({"error": "Fuel or gas not found or conversion factors not applicable."}), 400

@app.route("/get_conversion_factors_fuel_only", methods=["GET"])
def get_conversion_factors_fuel_only():
    fuel = request.args.get('fuel')

    if not fuel:
        return jsonify({'error': 'Fuel parameter is missing'}), 400

    # Calculate the conversion factors based on the provided fuel only
    conversion_factors = calculate_conversion_factors(fuel, None, liter=1.0)

    if not conversion_factors:
        return jsonify({'error': 'Invalid fuel'}), 400

    return jsonify({
        'conversion_factors': conversion_factors,
        'fuel': fuel
    })

if __name__ == "__main__":
    app.run(debug=True)
