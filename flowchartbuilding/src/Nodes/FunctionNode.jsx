import React, { useState, useEffect } from "react";
import { Handle, useUpdateNodeInternals } from "reactflow";
import "./FunctionNode.css";

export default function FunctionNode({ id, data }) {
  console.log(data.functionDict);
  const [activeInput, setActiveInput] = useState(null);
  const updateNodeInternals = useUpdateNodeInternals();
  const functionDict = data.functionDict;

  const getFunctionConfig = (func, dict) => {
    for (const category in dict) {
      if (dict[category].methods && typeof dict[category].methods === 'object') {
        if (dict[category].methods[func]) return dict[category].methods[func];
      }
      if (dict[category].children && typeof dict[category].children === 'object') {
        const result = getFunctionConfig(func, dict[category].children);
        if (result) return result;
      }
    }
    return null;
  };

  const methodConfig = getFunctionConfig(data.func, functionDict) || {
    inputs: 1,
    outputs: 1,
    inputNames: { input: null },
    outputNames: ["output"],
  };

  const inputKeys = Object.keys(methodConfig.inputNames || {});
  const totalInputs = inputKeys.length;

  useEffect(() => {
    updateNodeInternals(id);
  }, [data.func, id, updateNodeInternals]);

  const handleConnect = (handleId) => {
    setActiveInput(handleId);
  };

  const maxHandles = Math.max(totalInputs, methodConfig.outputs || 0);
  const baseHeight = 10;
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
            {methodConfig.inputNames[key] == null && (
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
      {(methodConfig.outputNames || []).map((name, index) => (
        <div
          key={`output-wrapper-${index}`}
          className="output-wrapper"
          style={{ top: `${getHandlePosition(index, methodConfig.outputs)}px` }}
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