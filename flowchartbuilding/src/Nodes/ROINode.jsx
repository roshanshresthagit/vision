import React, { useRef, useState, useEffect } from "react";
import { Handle, Position } from "reactflow";
import "./HandleStyles.css";

const RoiInputNode = ({ data, selected }) => {
  const canvasRef = useRef(null);
  const imageRef = useRef(null);
  const [imgDimensions, setImgDimensions] = useState({ width: 0, height: 0 });
  const [roi, setRoi] = useState(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPos, setStartPos] = useState(null);

  const isImage = typeof data.value === "string" && (
    data.value.startsWith("data:image/jpeg;base64") ||
    data.value.startsWith("data:image/png;base64")
  );

  useEffect(() => {
    if (isImage && imageRef.current) {
      const img = imageRef.current;
      img.onload = () => {
        setImgDimensions({ width: img.naturalWidth, height: img.naturalHeight });
        const canvas = canvasRef.current;
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
      };
    }
  }, [data.value, isImage]);

  const drawRect = (ctx, rect) => {
    if (!rect) return;
    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
  };

  const handleMouseDown = (e) => {
    setIsDrawing(true);
    const rect = canvasRef.current.getBoundingClientRect();
    setStartPos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  const handleMouseUp = (e) => {
    if (!isDrawing || !startPos) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const endX = e.clientX - rect.left;
    const endY = e.clientY - rect.top;
    const newRoi = {
      x: Math.min(startPos.x, endX),
      y: Math.min(startPos.y, endY),
      width: Math.abs(endX - startPos.x),
      height: Math.abs(endY - startPos.y)
    };
    setRoi(newRoi);
    setIsDrawing(false);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing || !startPos) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const ctx = canvasRef.current.getContext("2d");
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;
    const width = canvasRef.current.width;
    const height = canvasRef.current.height;

    ctx.clearRect(0, 0, width, height);
    drawRect(ctx, {
      x: Math.min(startPos.x, currentX),
      y: Math.min(startPos.y, currentY),
      width: Math.abs(currentX - startPos.x),
      height: Math.abs(currentY - startPos.y)
    });
  };

  useEffect(() => {
    if (canvasRef.current && roi) {
      const ctx = canvasRef.current.getContext("2d");
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      drawRect(ctx, roi);
    }
  }, [roi]);

  return (
    <div className={`node ${selected ? "selected" : ""}`}>
      <div className="node-header">ROI Input</div>
      <div className="node-body">
        {isImage && (
          <canvas
            ref={canvasRef}
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onMouseMove={handleMouseMove}
            style={{ border: "1px solid black", cursor: isDrawing ? "crosshair" : "default" }}
          />
        )}
        {isImage && <img ref={imageRef} src={data.value} alt="Input" style={{ display: "none" }} />}
        {roi && (
          <div>
            ROI: {roi.x}, {roi.y}, {roi.width}, {roi.height}
          </div>
        )}
      </div>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
    
  );
};

export default RoiInputNode;
