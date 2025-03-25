import React, { useState, useEffect } from "react";
import { Handle, useUpdateNodeInternals } from "reactflow";
import "./FunctionNode.css";

export default function FunctionNode({ id, data }) {
  const [activeInput, setActiveInput] = useState(null);
  const updateNodeInternals = useUpdateNodeInternals();
  const functionDict = data.functionDict;

  const config = functionDict?.[data.func] || {
    inputs: 1,
    outputs: 1,
    inputNames: { input: null },
    outputNames: ["output"],
  };

  const inputKeys = Object.keys(config.inputNames || {});
  const totalInputs = inputKeys.length;

  useEffect(() => {
    updateNodeInternals(id);
  }, [data.func, id, updateNodeInternals]);

  const handleConnect = (handleId) => {
    setActiveInput(handleId);
  };

  const maxHandles = Math.max(totalInputs, config.outputs || 0);
  const baseHeight = 60;
  const handleSpace = 25;
  const nodeHeight = baseHeight + maxHandles * handleSpace;

  const getHandlePosition = (index, total) => {
    if (total === 1) return nodeHeight / 2;
    const handleArea = nodeHeight - 20;
    const step = handleArea / (total - 1 || 1);
    return 10 + index * step;
  };

  return (
    <div className="node-container" style={{ height: `${nodeHeight}px` }}>
      {/* Input Handles */}
      {inputKeys.map((key, index) => (
        <div
          key={`input-wrapper-${index}`}
          className="input-wrapper"
          style={{ top: `${getHandlePosition(index, totalInputs)}px` }}
        >
          <Handle
            type="target"
            id={key}
            onConnect={() => handleConnect(key)}
            className="custom-handle input-handle"
            style={{
              backgroundColor: activeInput === key ? "blue" : "gray",
            }}
          />
          <span className="handle-label input-handle-label">
            {key}
            {config.inputNames[key] == null && (
              <span className="red-star">*</span>
            )}
          </span>
        </div>
      ))}
      {/* Node Content */}
      <div className="node-content">
        <div className="node-title">{data.label || "Function Node"}</div>
      </div>

      {/* Output Handles */}
      {(config.outputNames || []).map((name, index) => (
        <div
          key={`output-wrapper-${index}`}
          className="output-wrapper"
          style={{ top: `${getHandlePosition(index, config.outputs)}px` }}
        >
          <span className="handle-label output-handle-label">{name}</span>
          <Handle
            type="source"
            id={name}
            className="custom-handle output-handle"
          />
        </div>
      ))}
    </div>
  );
}
