import { useState } from "react";

export const useFlowExecution = (nodes, edges, inputs, setNodes) => {
  const [generatedCode, setGeneratedCode] = useState("");

  const executeFlow = async () => {

    const nodeValues = {};

    nodes.forEach(({ id, type }) => {
      const value = inputs[id];
    
      if (type === "imageInputNode" && typeof value === "string" && value.startsWith("data:image")) {
        nodeValues[id] = value;
        return;
      }
    
      if (type === "modelInputNode" && typeof value === "string") {
        nodeValues[id] = value;
        return;
      }
    
      if (type === "inputNode") {
        const parsed = parseFloat(value);
        nodeValues[id] = isNaN(parsed) ? 0 : parsed;
      }
    });
    
    

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
          }
        }
      }
    } catch (error) {
      console.error("Error executing flow:", error);
    }
  };

  return { executeFlow, generatedCode, setGeneratedCode }; 
};
