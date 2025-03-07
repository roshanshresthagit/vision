import { useState, useRef } from "react";

export default function CanvasFeedbackPage() {
  const [status, setStatus] = useState(null);
  const canvasRef = useRef(null);

  return (
    <div className="h-screen flex flex-col">
      {/* Top Bar */}
      <div className="flex justify-between p-4 bg-gray-800 text-white">
        <div className="space-x-2">
          <button onClick={() => setStatus("Good")} className="px-4 py-2 bg-green-500 text-white rounded">Mark Good</button>
          <button onClick={() => setStatus("Not Good")} className="px-4 py-2 bg-red-500 text-white rounded">Mark Not Good</button>
          <button onClick={() => setStatus(null)} className="px-4 py-2 bg-gray-500 text-white rounded">Reset</button>
          <button onClick={() => console.log("Find Camera")} className="px-4 py-2 bg-blue-500 text-white rounded">Find Camera</button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-grow p-4">
        {/* Canvas */}
        <div
          className={`flex-1 border border-gray-400 rounded-lg bg-white relative overflow-hidden`}
        >
          <canvas ref={canvasRef} className="w-full h-full"></canvas>
          {status === "Good" && (
            <div className="absolute inset-0 rounded-lg" style={{
              background: "radial-gradient(circle, rgba(34, 197, 94, 0) 0%, rgba(34, 197, 94, 0.2) 80%)"
            }}></div>
          )}
          {status === "Not Good" && (
            <div className="absolute inset-0 rounded-lg" style={{
              background: "radial-gradient(circle, rgba(239, 68, 68, 0) 0%, rgba(239, 68, 68, 0.2) 80%)"
            }}></div>
          )}
        </div>

        {/* Status Display on Right */}
        <div className="w-1/4 flex items-center justify-center text-2xl font-bold ml-4">
          {status === "Good" && <span className="text-green-600">Good ✅</span>}
          {status === "Not Good" && <span className="text-red-600">Not Good ❌</span>}
        </div>
      </div>
    </div>
  );
}
