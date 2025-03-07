import React from "react";
import { Handle, Position } from "reactflow";

const InputNode = ({ data }) => {
  // Function to handle changes in input field
  const handleChange = (e) => {
    const { value } = e.target;
    if (!isNaN(value) && value.trim() !== "") {
      data.setValue(Number(value)); // Store as a number if valid
    } else {
      data.setValue(value); // Otherwise, store as a string
    }
  };

  // Function to handle image uploads
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        data.setValue(reader.result); // Store image as base64 string
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="input-node">
      <div className="node-content">
        <div className="node-label">Input</div>

        {/* String or Number Input */}
        {typeof data.value === "string" && data.value.startsWith("data:image") ? (
          <img src={data.value} alt="Uploaded" style={{ width: "100px", height: "100px" }} />
        ) : (
          <input
            type="text"
            className="node-input"
            value={data.value || ""}
            onChange={handleChange}
          />
        )}

        {/* Image Upload Input */}
        <input type="file" accept="image/*" onChange={handleImageUpload} />

      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default InputNode;

