import { useState, useEffect, useRef } from "react";
import { Handle, Position } from "reactflow";
import "./HandleStyles.css";

const RoiInputNode = ({ data }) => {
  console.log("ROI Input Node Data:", data);
  const [imgWidth, setImgWidth] = useState("auto");
  const [imgHeight, setImgHeight] = useState("auto");
  const canvasRef = useRef(null);
  const imgRef = useRef(null);
  const [startPos, setStartPos] = useState(null);
  const [rectangles, setRectangles] = useState([]); // Store multiple rectangles

  const isImage =
    typeof data.image === "string" &&
    (data.image.startsWith("data:image/jpeg;base64") || data.image.startsWith("data:image/png;base64"));

  const imageSrc = isImage ? data.image : null;

  useEffect(() => {
    if (isImage && imageSrc) {
      const img = new Image();
      img.src = imageSrc;
      img.onload = () => {
        setImgWidth(img.width);
        setImgHeight(img.height);

        // Update canvas dimensions
        if (canvasRef.current) {
          canvasRef.current.width = img.width;
          canvasRef.current.height = img.height;
        }
      };
    }
  }, [imageSrc, isImage]);

  const handleMouseDown = (e) => {
    e.stopPropagation(); // Prevent React Flow from dragging the node
    const rect = canvasRef.current.getBoundingClientRect();
    setStartPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  const handleMouseMove = (e) => {
    e.stopPropagation(); // Prevent React Flow from dragging the node
    if (!startPos) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const width = x - startPos.x;
    const height = y - startPos.y;

    // Draw the current rectangle dynamically
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
      drawAllRectangles(ctx); // Redraw all existing rectangles
      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.strokeRect(startPos.x, startPos.y, width, height); // Draw the current rectangle
    }
  };

  const handleMouseUp = (e) => {
    e.stopPropagation(); // Prevent React Flow from dragging the node
    if (!startPos) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const width = x - startPos.x;
    const height = y - startPos.y;

    // Add the new rectangle to the list
    setRectangles((prev) => [...prev, { x: startPos.x, y: startPos.y, width, height }]);
    setStartPos(null);
  };

  const drawAllRectangles = (ctx) => {
    // Draw all rectangles stored in the state
    rectangles.forEach((rect) => {
      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
    });
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!ctx) return;

    // Clear the canvas and redraw all rectangles
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawAllRectangles(ctx);
  }, [rectangles]);

  return (
    <div className="result-node" style={{ position: "relative", width: imgWidth, height: imgHeight }}>
      <Handle
        type="target"
        position={Position.Left}
        className="custom-handle"
      />
      <div className="node-content">
        <div className="node-label">ROI Input</div>
        {isImage && (
          <>
            <img
              ref={imgRef}
              src={imageSrc}
              alt="ROI Input"
              style={{ width: imgWidth, height: imgHeight, display: "block" }}
            />
            <canvas
              ref={canvasRef}
              width={imgWidth}
              height={imgHeight}
              className="nodrag" // Prevent React Flow from dragging the canvas
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                cursor: "crosshair",
              }}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default RoiInputNode;