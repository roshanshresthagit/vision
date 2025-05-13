import { useCallback } from "react";

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
          label: isInput || isImageInput || isModelInput || isModelNode || isRoiInput  ? `${func.label}${inputNodeCount}` : func.label,
          func: func.func,
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
          functionDict,
        },
      };

      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);

      if (isInput || isImageInput) {
        setInputNodeCount((count) => count + 1);
      }

      if (!isInput && !isImageInput && !isModelInput && !isModelNode && !isRoiInput && func.func) {
        const getFunctionConfig = (func, dict) => {
          for (const category in dict) {
            if (dict[category].methods?.[func]) return dict[category].methods[func];
            if (dict[category].children) {
              const result = getFunctionConfig(func, dict[category].children);
              if (result) return result;
            }
          }
          return null;
        };

        const methodConfig = getFunctionConfig(func.func, functionDict);
        if (methodConfig?.inputNames) {
          Object.entries(methodConfig.inputNames).forEach(([key, value], index) => {
            if (typeof value === "number" || typeof value === "string") {
              const inputNodeId = `${nodeId + index + 1}`;
              const inputNode = {
                id: inputNodeId,
                type: "inputNode",
                position: {
                  x: position.x - 200,
                  y: position.y + index * 80,
                },
                data: {
                  label: `Input${inputNodeCount + index}`,
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
                  functionDict,
                },
              };

              const newEdge = {
                id: `e${inputNodeId}-${newNodeId}`,
                source: inputNodeId,
                animated: true,
                style:{stroke:'green'},
                target: newNodeId,
                targetHandle: key,
                type: "straight",
              };

              setNodes((nds) => [...nds, inputNode]);
              setEdges((eds) => [...eds, newEdge]);
              setInputs((prev) => ({ ...prev, [inputNodeId]: value }));
            }
          });

          setInputNodeCount((count) => count + Object.keys(methodConfig.inputNames).length);
          setNodeId((id) => id + Object.keys(methodConfig.inputNames).length);
        }
      }
    },
    [setNodes, setEdges, nodeId, inputNodeCount, functionDict, setInputs,setInputNodeCount, setNodeId]
  );

  return { onDrop };
};
