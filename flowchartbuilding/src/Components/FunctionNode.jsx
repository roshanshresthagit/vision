
import React, { useState, useEffect } from "react";
import { Handle, useUpdateNodeInternals } from "reactflow";


export default function FunctionNode({ id, data }) {
  const [activeInput, setActiveInput] = useState(null);
  const updateNodeInternals = useUpdateNodeInternals();
  const functionDict = data.functionDict;

  // Get config based on data.function, default to a basic config
  const config = functionDict[data.func] || {
    inputs: 1,
    outputs: 1,
    inputNames: ["input"],
    outputNames: ["output"],
  };

  // Update node internals when data.function changes
  useEffect(() => {
    updateNodeInternals(id); // Recalculate handle positions
  }, [data.func, id, updateNodeInternals]);

  const handleConnect = (handleId) => {
    setActiveInput(handleId);
  };

  // Calculate node height based on max handles
  const maxHandles = Math.max(config.inputs, config.outputs);
  const baseHeight = 60; // Minimum height for content
  const handleSpace = 20; // Extra space per handle
  const nodeHeight = baseHeight + maxHandles * handleSpace;

  // Calculate equal distance between handles based on node height
  const getHandlePosition = (index, total) => {
    if (total === 1) return nodeHeight / 2; // Center single handle
    const handleArea = nodeHeight - 20; // 10px padding top/bottom
    const step = handleArea / (total - 1 || 1); // Equal steps
    return 10 + index * step; // Start 10px from top
  };

  return (
    <div
      style={{
        padding: "10px",
        border: "1px solid #777",
        borderRadius: "5px",
        background: "#fff",
        minWidth: "200px", // Increased width for handle names
        height: `${nodeHeight}px`, // Dynamic height
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Dynamically created input handles with names */}
      <div style={{ position: "absolute", left: 0, top: 0 }}>
        {Array.from({ length: config.inputs }).map((_, index) => (
          <div
            key={`input-wrapper-${index}`}
            style={{
              position: "absolute",
              top: `${getHandlePosition(index, config.inputs)}px`,
              transform: "translateY(50%)", 
              display: "flex",
              alignItems: "center",
            }}
          >
            <Handle
              type="target"
              id={config.inputNames[index]}
              onConnect={() => handleConnect(config.inputNames[index])}
              style={{
                position: "absolute",
                left: "0px",   
                backgroundColor: activeInput === config.inputNames[index] ? "blue" : "gray",
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                transform: "translateX(-50%)", 
              }}
            />
            <span
              style={{
                position:"absolute",
                fontSize: "10px",
                color: "#333",
                left:"10px"
              }}
            >
              {config.inputNames[index]}
            </span>
          </div>
        ))}
      </div>

      {/* Node content */}
      <div style={{ textAlign: "center" }}>
        <div style={{ fontWeight: "bold" }}>{data.label || "Function Node"}</div>
        
      </div>

      {/* Dynamically created output handles with names */}
      <div style={{ position: "absolute", right:0, top: 0 }}>
        {Array.from({ length: config.outputs }).map((_, index) => (
          <div
            key={`output-wrapper-${index}`}
            style={{
              position: "absolute",
              top: `${getHandlePosition(index, config.outputs)}px`,
              transform: "translateY(50%)", // Center vertically
              display: "flex",
              alignItems: "left",
            }}
          >
            <span
              style={{
                position:"absolute",
                fontSize: "10px",
                color: "#333",
                right:"10px"
              }}
            >
              {config.outputNames[index]}
            </span>
            <Handle
              type="source"
              id={config.outputNames[index]}
              style={{
                position: "absolute",
                left:"0px",
                backgroundColor: "green",
                width: "10px",
                height: "10px",
                borderRadius: "-50%",
                transform: "translateX(-50%)", 
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}