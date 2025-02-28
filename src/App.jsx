import { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import vocxiLogo from "./assets/vocxi_logo.png"; // Import the logo
import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  // State for frequency (Hz), voltage (V), and time (HH:MM:SS)
  const [frequency, setFrequency] = useState(100); // Default frequency in Hz
  const [voltage, setVoltage] = useState(100); // Default voltage in V
  const [time, setTime] = useState("00:00:00"); // Default time in HH:MM:SS
  const [graphData, setGraphData] = useState({
    labels: [], // X-axis: Voltage
    datasets: [
      {
        label: "Capacitance vs Voltage",
        data: [], // Y-axis: Capacitance
        borderColor: "rgba(75, 192, 192, 1)",
        fill: false,
      },
    ],
  });

  // Handle frequency change (slider or input)
  const handleFrequencyChange = (event) => {
    setFrequency(parseFloat(event.target.value));
  };

  // Handle voltage change
  const handleVoltageChange = (event) => {
    setVoltage(parseFloat(event.target.value));
  };

  // Handle time change
  const handleTimeChange = (event) => {
    const { value } = event.target;
    // Automatically jump between colons
    if (value.length === 2 || value.length === 5) {
      setTime(value + ":");
    } else {
      setTime(value);
    }
  };

  // Handle Start button click
  const handleStart = () => {
    // Validate inputs
    if (!frequency || !voltage || !time) {
      alert("Please fill in all fields.");
      return;
    }

    // Generate a range of voltage values (e.g., from 0 to 2 * voltage)
    const voltageRange = Array.from({ length: 20 }, (_, i) => (i * voltage) / 10); // 20 points from 0 to 2 * voltage
    const capacitanceRange = voltageRange.map((v) => v / frequency); // Calculate capacitance for each voltage

    // Update graph data
    setGraphData({
      labels: voltageRange, // X-axis: Voltage
      datasets: [
        {
          ...graphData.datasets[0],
          data: capacitanceRange, // Y-axis: Capacitance
        },
      ],
    });
  };

  return (
    <div className="App">
      {/* Blue Bar at the Top */}
      <div className="top-bar">
        {/* Logo on the Top Right */}
        <img src={vocxiLogo} alt="Vocxi Logo" className="logo" />
      </div>

      {/* Spacer for the Top Bar */}
      <div className="top-bar-spacer"></div>

      {/* Main Content */}
      <div className="content">
        {/* Left Side: Inputs and Controls */}
        <div className="left-panel">
          <h1>Capacitance vs Voltage</h1>

          {/* Light Blue Box */}
          <div className="input-box">
            <h2>Enter Voltage, Frequency, and Time</h2>
            <div className="input-container">
              {/* Frequency Slider */}
              <label htmlFor="frequency">Frequency (Hz): {frequency}</label>
              <input
                id="frequency"
                type="range"
                min="1"
                max="1000"
                step="1"
                value={frequency}
                onChange={handleFrequencyChange}
              />

              {/* Frequency Input (Optional) */}
              <input
                type="number"
                placeholder="Enter frequency in Hz"
                value={frequency}
                onChange={handleFrequencyChange}
              />

              {/* Voltage Input */}
              <label htmlFor="voltage">Voltage (V):</label>
              <input
                id="voltage"
                type="number"
                placeholder="Enter voltage in V"
                value={voltage}
                onChange={handleVoltageChange}
              />

              {/* Time Input */}
              <label htmlFor="time">Time (HH:MM:SS):</label>
              <input
                id="time"
                type="text"
                placeholder="00:00:00"
                value={time}
                onChange={handleTimeChange}
                maxLength={8} // HH:MM:SS
              />

              {/* Start Button */}
              <button onClick={handleStart}>Start</button>
            </div>
          </div>
        </div>

        {/* Right Side: Graph */}
        <div className="graph-container">
          <Line
            data={graphData}
            options={{
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Voltage (V)",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "Capacitance (F)",
                  },
                },
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default App;