import React, { useRef } from "react";
import { Handle, Position } from "reactflow";
import "./ImageInputNode.css";

const ImageInputNode = ({ data }) => {
  const fileInputRef = useRef(null);

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

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="image-input-node">
      <div className="node-header">
        {/* <span className="node-icon">🖼️</span> */}
        <span className="node-title">Image Input</span>
      </div>

      {/* Image Preview Box (clickable) */}
      <div className="image-clickable" onClick={handleClick}>
        {data.value ? (
          <img src={data.value} alt="Uploaded" className="image-preview" />
        ) : (
          <div className="image-placeholder">Click to Upload</div>
        )}
      </div>

      {/* Hidden File Input */}
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        ref={fileInputRef}
        style={{ display: "none" }}
      />

      <Handle type="source" position={Position.Right} className="custom-handle" />
    </div>
  );
};

export default ImageInputNode;
