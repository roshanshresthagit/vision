import React from "react";
import { Handle, Position } from "reactflow";

const NumberInputNode = ({ data }) => {
  const handleChange = (e) => {
    const value = e.target.value;
    if (!isNaN(value) && value.trim() !== "") {
      data.setValue(Number(value)); // Store as a number if valid
    } else {
      data.setValue(""); // Clear if invalid
    }
  };

  return (
    <div className="input-node">
      <div className="node-content">
        <div className="node-label">Number Input</div>
        <input
          type="number"
          className="node-input"
          value={data.value || ""}
          onChange={handleChange}
        />
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default NumberInputNode;
