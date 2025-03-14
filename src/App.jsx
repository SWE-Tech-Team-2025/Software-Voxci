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
  const [hours, setHours] = useState("00"); // Default hours
  const [minutes, setMinutes] = useState("00"); // Default minutes
  const [seconds, setSeconds] = useState("00"); // Default seconds
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

  // Handle hours change
  const handleHoursChange = (event) => {
    setHours(event.target.value);
  };

  // Handle minutes change
  const handleMinutesChange = (event) => {
    setMinutes(event.target.value);
  };

  // Handle seconds change
  const handleSecondsChange = (event) => {
    setSeconds(event.target.value);
  };

  // Handle Start button click
  const handleStart = () => {
    // Validate inputs
    if (!frequency || !voltage || !hours || !minutes || !seconds) {
      alert("Please fill in all fields.");
      return;
    }

    // Combine hours, minutes, and seconds into a single time string
    const time = `${hours}:${minutes}:${seconds}`;

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

    // Log the selected time for debugging
    console.log("Selected Time:", time);
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
              <div className="time-picker">
                <select id="hours" value={hours} onChange={handleHoursChange}>
                  {/* Options for hours (00 to 23) */}
                  {Array.from({ length: 24 }, (_, i) => (
                    <option key={i} value={String(i).padStart(2, "0")}>
                      {String(i).padStart(2, "0")}
                    </option>
                  ))}
                </select>
                <span>:</span>
                <select id="minutes" value={minutes} onChange={handleMinutesChange}>
                  {/* Options for minutes (00 to 59) */}
                  {Array.from({ length: 60 }, (_, i) => (
                    <option key={i} value={String(i).padStart(2, "0")}>
                      {String(i).padStart(2, "0")}
                    </option>
                  ))}
                </select>
                <span>:</span>
                <select id="seconds" value={seconds} onChange={handleSecondsChange}>
                  {/* Options for seconds (00 to 59) */}
                  {Array.from({ length: 60 }, (_, i) => (
                    <option key={i} value={String(i).padStart(2, "0")}>
                      {String(i).padStart(2, "0")}
                    </option>
                  ))}
                </select>
              </div>

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