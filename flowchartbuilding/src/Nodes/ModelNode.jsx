import { useState } from 'react';
import {
    Handle,
    Position,
    useUpdateNodeInternals,
    useReactFlow,
    getConnectedEdges,
} from "reactflow";
import "./ModelInputNode.css";
import "./HandleStyles.css";

const ModelNode = ({ id, data }) => {
    const [handles, setHandles] = useState([]);
    const updateNodeInternals = useUpdateNodeInternals();
    const { addNodes, addEdges, getNodes, getEdges } = useReactFlow();

    const getInputData = () => {
        const allEdges = getEdges();
        const allNodes = getNodes();

        const inputValues = {};
        const inputHandles = ["model", "image"];

        inputHandles.forEach((handleId) => {
            const edge = allEdges.find(
                (e) => e.target === id && e.targetHandle === handleId
            );
            if (edge) {
                const sourceNode = allNodes.find((node) => node.id === edge.source);
                if (sourceNode?.data?.value) {
                    inputValues[handleId] = sourceNode.data.value;
                }
            }
        });

        return inputValues;
    };

    const handleUpdate = async () => {
        console.log("Update button clicked");
        const inputs = getInputData();
        console.log("ModelNode input values:", inputs);

        if (!inputs.model || !inputs.image) {
            console.error("Missing model name or image input");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/update", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model_name: inputs.model,
                    image: inputs.image
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const detectedCakes = await response.json();
            console.log("Detected cakes:", detectedCakes);

            const newHandles = Object.entries(detectedCakes).map(([key, value], index) => ({
                id: `output-${key}`,
                position: Position.Right,
                type: "source",
                data: value,
            }));

            setHandles(newHandles);
            updateNodeInternals(id);

            newHandles.forEach((handle, index) => {
                const resultNodeId = `result-${id}-${handle.id}`;
                const xOffset = 300;
                const yOffset = (index - (newHandles.length / 2)) * 100;

                const resultNode = {
                    id: resultNodeId,
                    type: 'resultNode',
                    position: { x: 700 + xOffset, y: 100 + yOffset },
                    data: { value: handle.data, image: inputs.image },
                };

                const edge = {
                    id: `edge-${id}-${handle.id}`,
                    source: id,
                    sourceHandle: handle.id,
                    target: resultNodeId,
                    type: 'smoothstep',
                };

                addNodes(resultNode);
                addEdges(edge);
            });

        } catch (error) {
            console.error("Error detecting objects:", error);
        }
    };

    return (
        <div className="model-input-node dynamic-node">
            <Handle 
                type="target" 
                position={Position.Left} 
                id="model"
                className="custom-handle"
                style={{ top: '30%' }}
            />
            <Handle 
                type="target" 
                position={Position.Left} 
                id="image"
                className="custom-handle"
                style={{ top: '70%' }}
            />

            <div className="node-header">
                <span className="node-title">YOLO</span>
            </div>

            <button className="upload-button" onClick={handleUpdate}>
                Update
            </button>

            {handles.map((handle, index) => (
                <Handle
                    key={handle.id}
                    type={handle.type}
                    position={handle.position}
                    id={handle.id}
                    className="custom-handle"
                    style={{ top: `${((index + 1) * 100) / (handles.length + 1)}%` }}
                    data={handle.data}
                />
            ))}
        </div>
    );
};

export default ModelNode;
