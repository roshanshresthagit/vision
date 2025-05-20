import React, { useEffect, useState } from "react";
import { Handle, Position } from "reactflow";
import "./HandleStyles.css";

const DetectionResultNode = ({ data }) => {
    const [croppedDetections, setCroppedDetections] = useState([]);

    const isImage =
        typeof data.image === "string" &&
        (data.image.startsWith("data:image/jpeg;base64") || data.image.startsWith("data:image/png;base64"));

    const imageSrc = isImage ? data.image : null;

    const rawCoords = Array.isArray(data.value?.coordinates) ? data.value.coordinates : [];
    const coordinates = [];

    if (rawCoords.length === 4 && typeof rawCoords[0] === "number") {
        coordinates.push({
            x: rawCoords[0],
            y: rawCoords[1],
            width: rawCoords[2],
            height: rawCoords[3]
        });
    }

    const confidence = typeof data.value?.confidence === "number" ? data.value.confidence : null;

    useEffect(() => {
        if (!imageSrc || coordinates.length === 0) return;

        const img = new Image();
        img.src = imageSrc;

        img.onload = () => {
            const crops = coordinates.map((coord) => {
                const { x, y, width, height } = coord;

                const cropCanvas = document.createElement("canvas");
                cropCanvas.width = width;
                cropCanvas.height = height;

                const ctx = cropCanvas.getContext("2d");
                ctx.drawImage(img, x, y, width, height, 0, 0, width, height);

                return {
                    src: cropCanvas.toDataURL("image/png"),
                    confidence: confidence ?? null
                };
            });

            setCroppedDetections(crops);
        };
    }, [imageSrc, coordinates, confidence]);

    return (
        <div className="result-node" style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <Handle type="target" position={Position.Left} className="custom-handle" />
            <div className="node-label">Detected Crops</div>

            <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                {croppedDetections.map(({ src, confidence }, idx) => (
                    <div key={idx} style={{ textAlign: "center" }}>
                        <img
                            src={src}
                            alt={`Detection ${idx}`}
                            style={{
                                border: "1px solid #aaa",
                                maxWidth: "120px",
                                maxHeight: "120px",
                                objectFit: "contain",
                            }}
                        />
                        {confidence !== null && (
                            <div style={{ fontSize: "0.8em", color: "#555" }}>
                                Conf: {confidence.toFixed(2)}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DetectionResultNode;
