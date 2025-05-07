import React, { useState, useEffect } from "react";
import { Handle, Position } from "reactflow";

const ResultNode = ({ data }) => {
  const [imgWidth, setImgWidth] = useState("auto");
  const [parsedValue, setParsedValue] = useState(null);

  const isImage = typeof data.value === "string" && (
    data.value.startsWith("data:image/jpeg;base64") ||
    data.value.startsWith("data:image/png;base64")
  );

  const imageSrc = isImage ? data.value : null;

  useEffect(() => {
    if (!isImage && typeof data.value === "string") {
      try {
        const parsed = JSON.parse(data.value);
        setParsedValue(parsed);
      } catch {
        setParsedValue(null);
      }
    }
  }, [data.value, isImage]);

  useEffect(() => {
    if (isImage && imageSrc) {
      const img = new Image();
      img.src = imageSrc;
      img.onload = () => setImgWidth(img.width);
    }
  }, [imageSrc, isImage]);

  const renderList = (list) => (
    <ul style={{ paddingLeft: 20 }}>
      {list.map((item, index) => (
        <li key={index}>
          {Array.isArray(item)
            ? renderList(item)
            : typeof item === "object"
            ? JSON.stringify(item)
            : String(item)}
        </li>
      ))}
    </ul>
  );

  return (
    <div className="result-node" style={{ width: isImage ? imgWidth : "auto" }}>
      <Handle type="target" position={Position.Left} />
      <div className="node-content">
        <div className="node-label">Result</div>
        <div className="result-value" style={{ maxHeight: 300, overflow: "auto" }}>
          {isImage ? (
            <img src={imageSrc} alt="Result" style={{ width: "100%" }} />
          ) : parsedValue && Array.isArray(parsedValue) ? (
            renderList(parsedValue)
          ) : (
            <span>{parsedValue ?? String(data.value)}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultNode;
