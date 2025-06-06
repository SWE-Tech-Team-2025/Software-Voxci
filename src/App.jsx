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
import * as XLSX from "xlsx"; // Import the xlsx library
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
  // State for frequency (Hz), voltage (V), and data history
  const [frequency, setFrequency] = useState(100); // Default frequency in Hz
  const [voltage, setVoltage] = useState(100); // Default voltage in V
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
  const [dataHistory, setDataHistory] = useState([]); // Store history of all runs

  // Handle frequency change (slider or input)
  const handleFrequencyChange = (event) => {
    setFrequency(parseFloat(event.target.value));
  };

  // Handle voltage change
  const handleVoltageChange = (event) => {
    setVoltage(parseFloat(event.target.value));
  };

  const handleStart = () => {
    if (!frequency || !voltage) {
      alert("Please fill in all fields.");
      return;
    }

    const voltageRange = Array.from({ length: 20 }, (_, i) => (i * voltage) / 10);
    const capacitanceRange = voltageRange.map((v) => v / frequency);

    const randomColor = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(
      Math.random() * 255
    )}, ${Math.floor(Math.random() * 255)}, 1)`;

    setGraphData({
      labels: voltageRange,
      datasets: [
        ...graphData.datasets,
        {
          label: `Run ${dataHistory.length + 1} (${frequency}Hz, ${voltage}V)`,
          data: capacitanceRange,
          borderColor: randomColor,
          backgroundColor: randomColor,
          fill: false,
          tension: 0.1,
        },
      ],
    });

    const timestamp = new Date().toLocaleString();
    const newRun = {
      timestamp,
      frequency,
      voltage,
      voltageRange,
      capacitanceRange,
      color: randomColor,
    };
    setDataHistory((prevHistory) => [...prevHistory, newRun]);
  };

  const handleViewExcel = () => {
    const excelData = dataHistory.map((run, index) => {
      return {
        "Run #": index + 1,
        Timestamp: run.timestamp,
        Frequency: run.frequency,
        Voltage: run.voltage,
        "Voltage Range": run.voltageRange.join(", "),
        "Capacitance Range": run.capacitanceRange.join(", "),
      };
    });

    const worksheet = XLSX.utils.json_to_sheet(excelData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Data History");
    XLSX.writeFile(workbook, "data_history.xlsx");
  };

  const handleClearGraph = () => {
    setGraphData({
      labels: [],
      datasets: [],
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
            <h2>Enter Voltage and Frequency</h2>
            <div className="input-container">
              {/* Frequency Slider */}
              <label htmlFor="frequency">Frequency (Hz): {frequency}</label>

              {/* Frequency Input (Optional) */}
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
              {/* Start Button! */}
              <button onClick={handleStart}>Start</button>

              {/* View Excel Button */}
              <button onClick={handleViewExcel}>View Excel</button>
              <button onClick={handleClearGraph}>Clear Graph</button>
            </div>
          </div>
        </div>

        {/* Right Side: Graph */}
        <div className="graph-container">
          <div className="graph-box">
            <Line
              data={graphData}
              options={{
                responsive: true,
                scales: {
                  x: {
                    title: {
                      display: true,
                      text: "Voltage (V)",
                    },
                    min: 0,
                    max: 200,
                  },
                  y: {
                    title: {
                      display: true,
                      text: "Capacitance (F)",
                    },
                    min: 0,
                    max: 2,
                  },
                },
              }}
            />
          
            <div className="table-container">
              <h2>Data History</h2>
              <table>
                <thead>
                  <tr>
                    <th>Run #</th>
                    <th>Timestamp</th>
                    <th>Frequency (Hz)</th>
                    <th>Voltage (V)</th>
                  </tr>
                </thead>
                <tbody>
                  {dataHistory.map((run, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{run.timestamp}</td>
                      <td>{run.frequency}</td>
                      <td>{run.voltage}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;