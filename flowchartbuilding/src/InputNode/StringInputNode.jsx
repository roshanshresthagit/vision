import React from "react";
import { Handle, Position } from "reactflow";

const StringInputNode = ({ data }) => {
  const handleChange = (e) => {
    data.setValue(e.target.value); // Store as a string
  };

  return (
    <div className="input-node">
      <div className="node-content">
        <div className="node-label">String Input</div>
        <input
          type="text"
          className="node-input"
          value={data.value || ""}
          onChange={handleChange}
        />
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default StringInputNode;
