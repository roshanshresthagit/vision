import { useCallback } from "react";
import { addEdge, MarkerType } from "reactflow";

export const useNodeDrop = ({
  nodeId,
  inputNodeCount,
  functionDict, 
  setInputs,
  setNodes,
  setEdges,
  setNodeId,
  setInputNodeCount,
}) => {
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const reactFlowBounds = event.target.getBoundingClientRect();
      const func = JSON.parse(event.dataTransfer.getData("application/reactflow"));
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      const newNodeId = `${nodeId}`;
      const isInput = func.id === "input";
      const isImageInput = func.id === "imageinput";
      const isModelInput = func.id === "modelinput";
      const isModelNode = func.id === "modelnode";
      const isRoiInput = func.id === "roiinput";

      // Find the specific function metadata from functionDict
      const findFunctionMetadata = (funcName, dict) => {
        for (const category in dict) {
          if (dict[category].methods?.[funcName]) {
            return {
              [funcName]: dict[category].methods[funcName]
            };
          }
          if (dict[category].children) {
            const result = findFunctionMetadata(funcName, dict[category].children);
            if (result) return result;
          }
        }
        return null;
      };

      const functionMetadata = func.func ? findFunctionMetadata(func.func, functionDict) : null;
      console.log("functionMetadata", functionMetadata);

      const newNode = {
        id: newNodeId,
        type: isInput
          ? "inputNode"
          : isImageInput
          ? "imageInputNode"
          : isModelInput
          ? "modelInputNode"
          : isModelNode
          ? "modelNode"
          : isRoiInput
          ? "roiInputNode"
          : func.id === "result"
          ? "resultNode"
          : "functionNode",
        position,
        data: {
          label: isInput || isImageInput || isModelInput || isModelNode || isRoiInput  
            ? `${func.label}${inputNodeCount}` 
            : func.label,
          func: func.func,
          // Only include the matched function metadata
          functionDict: functionMetadata || null,
          value: isInput || isImageInput || isModelInput || isModelNode || isRoiInput ? 0 : undefined,
          setValue:
            isInput || isImageInput || isModelInput || isModelNode || isRoiInput
              ? (val) =>
                  setInputs((prev) => {
                    const updated = { ...prev, [newNodeId]: val };
                    setNodes((nds) =>
                      nds.map((node) =>
                        node.id === newNodeId ? { ...node, data: { ...node.data, value: val } } : node
                      )
                    );
                    return updated;
                  })
              : undefined,
              // functionDict
        },
        
      };

      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);

      if (isInput || isImageInput) {
        setInputNodeCount((count) => count + 1);
      }

      if (!isInput && !isImageInput && !isModelInput && !isModelNode && !isRoiInput && func.func && functionMetadata) {
        const methodConfig = functionMetadata[func.func];
        if (methodConfig?.inputNames) {
          Object.entries(methodConfig.inputNames).forEach(([key, value], index) => {
            if (typeof value === "number" || typeof value === "string") {
              const inputNodeId = `${nodeId +index+ 1}`;
              const inputNode = {
                id: inputNodeId,
                type: "inputNode",
                position: {
                  x: position.x - 200,
                  y: position.y + index * 80,
                },
                data: {
                  label: `Input${inputNodeCount + index}`,
                  func:'input',
                  value,
                  setValue: (val) =>
                    setInputs((prev) => {
                      const updated = { ...prev, [inputNodeId]: val };
                      setNodes((nds) =>
                        nds.map((node) =>
                          node.id === inputNodeId ? { ...node, data: { ...node.data, value: val } } : node
                        )
                      );
                      return updated;
                    }),
                },
              };

              setEdges(els => addEdge({
                        id: `e${inputNodeId}-${newNodeId}`,
                        source: inputNodeId,
                        target: newNodeId,
                        targetHandle: key,  
                        sourceHandle: null,
                        animated: true,
                        style: { stroke: 'green' },
                        type: "straight",
                        markerEnd: { type: MarkerType.ArrowClosed, color: 'green' }
                      }, els));
              setNodes((nds) => [...nds, inputNode]);
              setInputs((prev) => ({ ...prev, [inputNodeId]: value }));
            }
          });

          setInputNodeCount((count) => count + Object.keys(methodConfig.inputNames).length);
          setNodeId((id) => id + Object.keys(methodConfig.inputNames).length);
        }
      }
    },
    [setNodes, setEdges, nodeId, inputNodeCount, functionDict, setInputs, setInputNodeCount, setNodeId]
  );

  return { onDrop };
};