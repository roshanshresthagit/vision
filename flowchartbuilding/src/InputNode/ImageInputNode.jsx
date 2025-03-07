import React from "react";
import { Handle, Position } from "reactflow";

const ImageInputNode = ({ data }) => {
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
        <div className="node-label">Image Upload</div>
        {data.value && data.value.startsWith("data:image") ? (
          <img
            src={data.value}
            alt="Uploaded"
            style={{ width: "100px", height: "100px" }}
          />
        ) : (
          <p>No image uploaded</p>
        )}
        <input type="file" accept="image/*" onChange={handleImageUpload} />
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default ImageInputNode;
