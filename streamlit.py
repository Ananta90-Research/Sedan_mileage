import streamlit as st
from dataclasses import dataclass

# Constants
LHV = {'gasoline': 44_000_000, 'diesel': 42_500_000}  # J/kg
rho_f = {'gasoline': 0.745, 'diesel': 0.832}          # kg/L
eta = {'gasoline': 0.30, 'diesel': 0.35}              # engine efficiency
driving_eff = {'city_driving': 0.2, 'highway_cruising': 0.3, 'full_accelerator': 0.9}

@dataclass
class Car:
    fuel_type: str
    driving_mode: str
    max_power_kw: float
    hvac_power_w: float
    speed_kmh: float

    def fuel_consumption_lph(self):
        drive_power = self.max_power_kw * 1000 * driving_eff[self.driving_mode]
        total_power = drive_power + self.hvac_power_w
        m_dot = total_power / (eta[self.fuel_type] * LHV[self.fuel_type])
        v_dot = m_dot / rho_f[self.fuel_type]
        return v_dot * 3600

    def mileage_kpl(self):
        v_ms = self.speed_kmh / 3.6
        drive_power = self.max_power_kw * 1000 * driving_eff[self.driving_mode]
        total_power = drive_power + self.hvac_power_w
        m_dot = total_power / (eta[self.fuel_type] * LHV[self.fuel_type])
        v_dot = m_dot / rho_f[self.fuel_type]
        return v_ms / v_dot / 1000

# Streamlit App
st.set_page_config(page_title="Sedan Car Efficiency Calculator", page_icon="🚗")

st.title("🚗 Sedan Car Efficiency Calculator")

st.sidebar.header("Input Parameters")
fuel_type = st.sidebar.selectbox("Fuel Type", ["gasoline", "diesel"])
driving_mode = st.sidebar.selectbox("Driving Mode", ["city_driving", "highway_cruising", "full_accelerator"])
max_power_kw = st.sidebar.number_input("Max Engine Power (kW)", value=90)
hvac_power_w = st.sidebar.number_input("HVAC Power (W)", value=2000.0)
speed_kmh = st.sidebar.number_input("Speed (km/h)", value=50.0)

if st.sidebar.button("Calculate"):
    car = Car(fuel_type, driving_mode, max_power_kw, hvac_power_w, speed_kmh)
    fuel_consumption = car.fuel_consumption_lph()
    mileage = car.mileage_kpl()

    st.subheader("📊 Results")
    st.success(f"**Fuel Consumption:** {fuel_consumption:.2f} L/h")
    st.success(f"**Mileage:** {mileage:.2f} km/L")
