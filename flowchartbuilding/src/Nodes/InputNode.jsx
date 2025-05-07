import React from "react";
import { Handle, Position } from "reactflow";
import "./InputNode.css";

const InputNode = ({ data }) => {
  const handleChange = (e) => {
    const input = e.target.value;
    let parsedValue = input;

    try {
      parsedValue = JSON.parse(input);
    } catch {
      parsedValue = input;
    }

    data.setValue(parsedValue);
  };

  return (
    <div className="input-node">     
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
