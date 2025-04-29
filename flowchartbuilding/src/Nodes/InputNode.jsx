import React from "react";
import { Handle, Position } from "reactflow";
import "./InputNode.css";

const InputNode = ({ data }) => {
  const handleChange = (e) => {
    const { value } = e.target;
    if (!isNaN(value) && value.trim() !== "") {
      data.setValue(Number(value)); 
    } else {
      data.setValue(value); 
    }
  };

  return (
    <div className="input-node">
      <div className="node-header">Input Node</div>

      <div className="node-content">
        <input
          type="text"
          className="text-input"
          placeholder="Enter value"
          value={data.value || ""}
          onChange={handleChange}
        />
      </div>

      <Handle type="source" position={Position.Right} className="custom-handle" />
    </div>
  );
};

export default InputNode;
