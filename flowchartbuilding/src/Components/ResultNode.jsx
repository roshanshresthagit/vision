import React from "react";
import { Handle, Position } from "reactflow";

const ResultNode = ({ data }) => {
  // Check if data.value is a Base64 string that doesn't have the "data:image" prefix
  const isImage = typeof data.value === "string" && (data.value.startsWith("/9j/") || data.value.startsWith("iVBORw0KGgo"));

  // If it's a Base64 string without the "data:image" prefix, add it
  const imageSrc = isImage ? `data:image/jpeg;base64,${data.value}` : data.value;

  return (
    <div className="result-node">
      <Handle type="target" position={Position.Left} />
      <div className="node-content">
        <div className="node-label">Result</div>
        <div className="result-value">
          {isImage ? (
            <img src={imageSrc} alt="Result" style={{ maxWidth: "100%" }} /> // Render Base64 image
          ) : (
            data.value // Render the value (string or number)
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultNode;
