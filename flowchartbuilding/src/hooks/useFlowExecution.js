import { useState } from "react";

export const useFlowExecution = (nodes, edges, inputs, setNodes) => {
  const [generatedCode, setGeneratedCode] = useState("");
  const executeFlow = async () => {
    const nodeValues = {};

    nodes.forEach(({ id, type }) => {
      const value = inputs[id];
      console.log("this is valuie",value)
      
    
      if (type === "imageInputNode" && typeof value === "string" && value.startsWith("data:image")) {
        nodeValues[id] = value;
        return;
      }
    
      if (type === "modelInputNode" && typeof value === "string") {
        nodeValues[id] = value;
        return;
      }
    
      if (type === "inputNode") {
        try {
          let parsedValue;

          if (typeof value === 'string') {
            const trimmed = value.trim();

            if (
              trimmed.startsWith('(') &&
              trimmed.endsWith(')') &&
              /^(\(\s*\d+(\s*,\s*\d+)*\s*\))$/.test(trimmed)
            ) {
              parsedValue = trimmed;
            }

            else if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
              parsedValue = JSON.parse(trimmed);
            }

            else if (!isNaN(trimmed)) {
              parsedValue = parseFloat(trimmed);
            }

            else {
              parsedValue = trimmed;
            }
          } else {
            parsedValue = value;
          }

          if (
            parsedValue === undefined ||
            parsedValue === null ||
            Number.isNaN(parsedValue)
          ) {
            nodeValues[id] = 0;
          } else {
            nodeValues[id] = parsedValue;
          }
        } catch (e) {
          nodeValues[id] = 0;
        }
      }


        
      if (type === "detectionResultNode" && typeof value==="string" && value.startsWith("data:image")){
        console.log("this is valueeeeeeeeeeee ",value)
      }
    });
    
    
    console.log("this is input check",nodeValues)
    try {
      const response = await fetch("http://localhost:8000/execute_flow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nodes, edges, inputValues: nodeValues }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        let newlineIndex;
        while ((newlineIndex = buffer.indexOf("\n")) >= 0) {
          const line = buffer.slice(0, newlineIndex).trim();
          buffer = buffer.slice(newlineIndex + 1);

          if (line) {
           
            const data = JSON.parse(line);
            if (data.resultNode) {
              setNodes((nds) =>
                nds.map((node) =>
                  node.id === data.resultNode ? { ...node, data: { ...node.data, value: data.value } } : node
                )
              );
            }
            if (data.roiInputNode) {
              setNodes((nds) =>
                nds.map((node) =>
                  node.id === data.roiInputNode ? { ...node, data: { ...node.data, value: data.value } } : node
                )
              );
            }
          }
        }
      }
    } catch (error) {
      console.error("Error executing flow:", error);
    }
  };

  return { executeFlow, generatedCode, setGeneratedCode }; 
};
